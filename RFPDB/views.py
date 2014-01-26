from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from RFPDBApp.models import RFPQuestion, RFPAnswer
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from djorm_pgfulltext.models import SearchManager
import sys, csv, datetime, string
from docx import opendocx, getdocumenttext
from django.views.decorators.csrf import csrf_exempt
from StringIO import StringIO

#return render_to_response('my_template.html', locals()) #locals() passes the local variables to the template, names must match

def hello(request):
    return HttpResponse("Hello world")

def add(request):
    errors = []
    if request.method == 'POST':
        new_question = RFPQuestion.objects.create(question = request.POST['question'], answer = request.POST['answer'],
                                                      date_added = datetime.datetime.now(), last_used = datetime.datetime.now())
        return render_to_response('add.html', context_instance=RequestContext(request))

    else:
        return render_to_response('add.html', context_instance=RequestContext(request))
@csrf_exempt    
def ans_search(request):
    errors = []
    if request.method == 'POST':
        print '"' + request.POST['query'] + '"'
        questions = RFPQuestion.search_manager.search(request.POST['query'], rank_field='Search Rank')
        for quest in questions:
            print list(questions.__dict__['query'].__dict__['extra']['Search Rank'])
        
        return render_to_response('search.html', {'questions': questions}, context_instance=RequestContext(request))
    else:
        return render_to_response('search.html', context_instance=RequestContext(request))

def loaddoc(request):

    try:
        doc = StringIO()
        doc.write(request.FILES['file'].read())
        document = opendocx(doc)        

    except Exception, e: #fix this later
        print e
    
    paratextlist = getdocumenttext(document)

    newparatextlist = []
    for paratext in paratextlist:
        newparatextlist.append(paratext.encode("utf-8"))

    document = '<br><br>'.join(newparatextlist)

    return render_to_response('loaddoc.html', {'document': document}, context_instance=RequestContext(request))

def loadcsv(request):
    doc = StringIO()
    doc.write(request.FILES['file'].read())

    for row in doc:
        if len(row) != 2:
            print 'Bad Data!'
        else:
            #print row[0], row[1]
            new_question = RFPQuestion.objects.create(question = unicode(row[0], errors='ignore'), answer = unicode(row[1], errors='ignore'),
                                                      date_added = datetime.datetime.now(), last_used = datetime.datetime.now())
            

    return render_to_response('uploadfile.html', context_instance=RequestContext(request))
        
def upload_file(request):
    if request.method == 'POST':
        if '.docx' in request.FILES['file'].name:
            return loaddoc(request)
        elif '.csv' in request.FILES['file'].name or '.xlsx' in request.FILES['file'].name:
            return loadcsv(request)
        '''spamreader = csv.reader(request.FILES['file'].read())'''

    else:
        return render_to_response('uploadfile.html', context_instance=RequestContext(request))
