import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.contrib.sessions.backends.db import SessionStore
from django import forms

from utils.jsonutils import *

from pastey.models import *
from pastey.pretty import * 
from pastey.choices import *
from pastey.pdf import *


def list_page(request, code_id = 1):
    """List all public pastebin submissions
    """
    entries_per_page = 5
    char_limit = 1200    

    #handle form requests for searching
    if request.method == 'POST':
        if request.POST.get("search", None):
            form = SearchForm(request.POST)
            if form.is_valid():
                keyword = request.POST.get('keyword')
                field = request.POST.get('field')
                paste_list = make_query(field, keyword)               
                
    #default page load or invalid form
    else:
        form = SearchForm()
        #obtain the list of public pastes from the database, arrange by most recent
        paste_list = list(Code.objects.exclude(private = True).order_by('-pub_date'))
    
    #use the pretty module (which uses Pygments) to format text. Return text with HTML tags and CSS
    text_output = tersify(paste_list, char_limit)
    paste_list = pretty_pastes(text_output)
       
    #use Paginator to spread entries across multiple pages
    pages = Paginator(paste_list, entries_per_page) 
    thispage = pages.page(code_id)
    
    
    last_paste_link = cookie_checker(request)       
    
    return render_to_response('pastey/list.html',{
        'form': form,
        'results': len(paste_list),
        'pastes': thispage.object_list,
        'page': thispage, 
        'page_display': str(thispage)[1:-1], 
        'last_page': pages.num_pages,
        'last_paste': last_paste_link,
        }, context_instance=RequestContext(request))
	
def index(request, edit_id = None): 
    """Provide the pastebin submission form as well as a link to the list view
    """   
    
    #If cookies don't work, or the form doesn't validate a default value is needed
    last_paste_link = "/pastey" 
    
    #by default there is no error message
    err_msg = False
    
    #form handling for making a new paste
    if request.method == 'POST':         
        form = CodeForm(request.POST, request.FILES)
        code_paste = request.POST.get('code_paste')  
        
        #check form validation, and the user must type the code or upload a file   
        if form.is_valid() and (request.FILES or code_paste):    
            #save to db and save the uploaded file or create own
            a = form.save()              
            #store paste in a cookie
            request.session['member_id'] = a.id
            
            return redirect(a)
        
        #if form is submitted without code or an upload
        else:
      	    form = CodeForm()
      	    err_msg = True
	  
    else:
        #initial page load
        if not edit_id: 
            form = CodeForm() 
        
        #loading with data from a previous paste
        if edit_id:
            data = Code.objects.get(pk = edit_id)
            form = CodeForm(instance=data)
   
    last_paste_link = cookie_checker(request)    
    
    return render_to_response('pastey/index.html', {
        'form': form,          
        'last_paste': last_paste_link,
        'err_msg': err_msg,
        'editing': edit_id,
        }, context_instance=RequestContext(request))	

def detail(request, code_id):
    """Provide a detail view of pasted code

    This view provides pasted code with syntax highlighting, line numbers, 
    and header information such as the author if it was provided. File 
    download, highlighting style choices, and alternate views such as plain 
    text are also provided.
    """
    paste = get_object_or_404(Code, pk = code_id)	

    style_menu = StyleForm()	#To display the style menu for the user to choose from
    style_choice = Style()
  
    #handle form requests 
    if request.method == 'POST':
                
        #request to delete the most recent paste
        if request.POST.get("delete", None):
            this_paste = Code.objects.get(pk = code_id)            
            this_paste.txt_file.delete()
            this_paste.delete()
            
            request.session['member_id'] = 0
            request.session.set_test_cookie()
            return redirect('pastey.views.index')            
            
    if request.method == 'GET':
        form = StyleForm(request.GET)
        if form.is_valid():
            style_choice.highlight = form.cleaned_data['highlight']
            
    
    pretty_code, css_style = pretty_print(paste, style_choice)    
    
    last_paste_link = cookie_checker(request)      
      
    return render_to_response('pastey/detail.html',{
        'paste': paste, 
        'code': pretty_code, 
        'css_style': css_style, 
        'style_chooser': style_menu,
        'current_style': style_choice.highlight,
        'last_paste': last_paste_link,
        }, context_instance=RequestContext(request))
        
def pdf(request, code_id, style_id):

    paste = get_object_or_404(Code, pk = code_id)	
    style_choice = Style()		#To hold the user's chosen highlight style     

    style_choice.highlight = style_id
    pretty_code, css_style = pretty_print(paste, style_choice, "inline", False)
    last_paste_link = cookie_checker(request)    
        
    return render_to_pdf('pastey/pdf.html',
        {
        'pagesize':'A4',
        'paste': paste,
        'code': pretty_code,
        'css_style': css_style,
        })

def plain(request, code_id):
    """An HTML document with only the plain text of a paste
    """
    
    paste = get_object_or_404(Code, pk = code_id)	
    
    last_paste_link = cookie_checker(request)    
        
    return render_to_response('pastey/plain.html',{
    'paste': paste,
    },context_instance=RequestContext(request))

def html(request, code_id, style_id):
    """An HTML document showing the source code for a paste with highlighting        
    """
    
    paste = get_object_or_404(Code, pk = code_id)	
    style_choice = Style()		#To hold the user's chosen highlight style     

    style_choice.highlight = style_id
    pretty_code, css_style = pretty_print(paste, style_choice, "table", True)
    last_paste_link = cookie_checker(request)    
        
    return render_to_response('pastey/html.html',{
    'paste': paste,
    'code': pretty_code,
    'css_style': css_style,
    },context_instance=RequestContext(request))

def copy(request, code_id, style_id):
    """Link to the new paste form that copies the data in the current paste
    """
    
    paste = get_object_or_404(Code, pk = code_id)	
    style_choice = Style()		#To hold the user's chosen highlight style
         
    style_choice.highlight = style_id
    pretty_code, css_style = pretty_print(paste, style_choice, False)
    last_paste_link = cookie_checker(request)    
        
    return render_to_response('pastey/copy.html',{
    'paste': paste,
    'code': pretty_code,
    'css_style': css_style,
    },context_instance=RequestContext(request))

#not views!
def make_query(field, keyword):
    """Provide search capabilities for the list view    
    """
    
    if field == "title": 
        paste_list = list(Code.objects.exclude(private = True
        ).order_by('-pub_date'
        ).filter(title__icontains=keyword
        ))
    if field == "author": 
        paste_list = list(Code.objects.exclude(private = True
        ).order_by('-pub_date'
        ).filter(author__icontains=keyword
        ))
    if field == "email": 
        paste_list = list(Code.objects.exclude(private = True
        ).order_by('-pub_date'
        ).filter(email__icontains=keyword
        ))
    if field == "language": 
        for choice in LANG_CHOICES:
            if keyword.lower() == choice[1].lower(): keyword = choice[0]
        paste_list = list(Code.objects.exclude(private = True
        ).order_by('-pub_date'
        ).filter(language__iexact=keyword
        ))
    return paste_list


def cookie_checker(request):
    """Fetch cookie if possible and provide a link to the most recent paste 
    
    If cookies are disabled or the user has not made a paste, set the link to 
    the main page.    
    """
    
    try:        
        if request.session.test_cookie_worked(): 
                request.session.delete_test_cookie() 
                last_paste_link = request.session.get('member_id')
                if not last_paste_link: last_paste_link = None
                            	
        else:                
            last_paste_link = None   

        #test if a cookie works. If so, the next page will link to the user's last paste
        request.session.set_test_cookie()    
    except:
        last_paste_link = None
    return last_paste_link

