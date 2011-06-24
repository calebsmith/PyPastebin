import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
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
    return render_to_response('pastey/detail.html',{'paste': paste, 'code': pretty_code, 'css_style': css_style, 'style_chooser': style_menu}, context_instance=RequestContext(request))

def list_page(request):
    """List all public pastebin submissions
    """
    paste_list = list(Code.objects.exclude(private = True).order_by('-pub_date'))
    pastes = tersify(paste_list, 400)
    pastes = pretty_pastes(paste_list)    
 
    return render_to_response('pastey/list.html',{'pastes': pastes})
	
def index(request): 
    """Provide the pastebin submission form as well as links detail and list views
    """
    pastes = list(Code.objects.exclude(private = True).order_by('-pub_date'))  
    
    #limit to 5 entries
    pastes = pastes[:5]
    #limit each code paste to 400
    pastes = tersify(pastes, 400)       
    #highlight text 
    pastes = pretty_pastes(pastes)
    
    #form handling for making a new paste
    if request.method == 'POST': 
        form = CodeForm(request.POST)
        if form.is_valid():
            a = form.save()
            return redirect(a)      
	   
    else: #maintain form data and redirect
            form = CodeForm()        	
    
    return render_to_response('pastey/index.html', 
        {'form': form, 'pastes': pastes}, context_instance=RequestContext(request))	

