import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from django.contrib.sessions.backends.db import SessionStore

from django import forms

from pastey.models import *
from pastey.pretty import * 

def detail(request, code_id):
    """Provide a detail view of pasted code

    This view provides pasted code with syntax highlighting, line numbers, 
    and header information such as the author if it was provided upon submittal. 
    """
    paste = get_object_or_404(Code, pk = code_id)	
    style_choice = Style()		#To hold the user's chosen highlight style 
    style_menu = StyleForm()	#To display the menu for the user to choose from
    
    #handle form request for user changing the highlighting style
    if request.method == 'POST':
        form = StyleForm(request.POST)
        if form.is_valid():
            style_choice.highlight = form.cleaned_data['highlight']	    

    pretty_code, css_style = pretty_print(paste, style_choice)
    
    #fetch cookie if possible, otherwise set link to main page.
    if request.session.test_cookie_worked(): 
            last_paste_link = request.session.get('member_id')
            if not last_paste_link:
                last_paste_link = "/pastey"
            request.session.delete_test_cookie() 	
    else:                
        last_paste_link = "/pastey"   

    #test if a cookie works. If so, another page will link to the user's last paste
    request.session.set_test_cookie()
    

    
    return render_to_response('pastey/detail.html',{
        'paste': paste, 
        'code': pretty_code, 
        'css_style': css_style, 
        'style_chooser': style_menu,
        'last_paste': last_paste_link,
        }, context_instance=RequestContext(request))

def list_page(request, code_id):
    """List all public pastebin submissions
    """
    entries_per_page = 5
    char_limit = 1200
    
    #use the pretty module (which uses Pygments) to format text. Return text with HTML tags and CSS
    paste_list = list(Code.objects.exclude(private = True).order_by('-pub_date'))
    text_output = tersify(paste_list, char_limit)
    paste_list = pretty_pastes(text_output)
       
    #use Paginator to spread entries across multiple pages
    pages = Paginator(paste_list, entries_per_page) 
    thispage = pages.page(code_id)
    
    #fetch cookie if possible, otherwise set link to main page.
    if request.session.test_cookie_worked(): 
            last_paste_link = request.session.get('member_id')
            if not last_paste_link:
                last_paste_link = "/pastey"
            request.session.delete_test_cookie() 	
    else:                
        last_paste_link = "/pastey"   

    #test if a cookie works. If so, another page will link to the user's last paste
    request.session.set_test_cookie()
    
    
    return render_to_response('pastey/list.html',{
        'pastes': thispage.object_list,
        'page': thispage, 
        'page_display': str(thispage)[1:-1], 
        'last_page': pages.num_pages,
        'last_paste': last_paste_link,
        }, context_instance=RequestContext(request))
	
def index(request): 
    """Provide the pastebin submission form as well as links detail and list views
    """
    #obtain the 5 most recent pastes
    show_entries = 3
    pastes = list(Code.objects.exclude(private = True).order_by('-pub_date'))[:show_entries]

    #limit each code paste to 400
    char_limit = 400
    text_output = tersify(pastes, char_limit)       

    #highlight text 
    pastes = pretty_pastes(text_output)    
    
    #If cookies don't work, or the form doesn't validate a default value is needed
    last_paste_link = "/pastey" 
    
    #form handling for making a new paste
    if request.method == 'POST':         
        form = CodeForm(request.POST)        
        if form.is_valid():            
            a = form.save()              
            #store paste in a cookie
            request.session['member_id'] = a.id
            return redirect(a)      
	
	#maintain form data and redirect if not valid (also initial page load)   
    else: 
        form = CodeForm() 
        if request.session.test_cookie_worked(): 
            last_paste_link = request.session.get('member_id')
            if not last_paste_link:
                last_paste_link = "/pastey"
            request.session.delete_test_cookie() 	
        else:                
            last_paste_link = "/pastey"   
            
    #test if a cookie works. If so, another page will link to the user's last paste
    request.session.set_test_cookie()
                 
    return render_to_response('pastey/index.html', {
        'form': form, 
        'pastes': pastes, 
        'last_paste': last_paste_link,
        }, context_instance=RequestContext(request))	

