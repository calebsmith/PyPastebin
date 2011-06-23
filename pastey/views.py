import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django import forms

from pastey.models import *
from pastey.pretty import pretty_print, pretty_pastes

def detail(request, code_id):
    """Provide a detail view of pasted code

    This view provides pasted code with syntax highlighting, line numbers, 
    and header information such as the author if it was provided upon submittal. 
    """
    paste = get_object_or_404(Code, pk = code_id)	
    style_choice = Style()		#To hold the user's chosen highlight style
    style_menu = StyleForm()	#To display the menu for the user to choose from
	
    #handle form request(user changing the highlight)
    if request.method == 'POST':
        form = StyleForm(request.POST)
        if form.is_valid():
            style_choice.highlight = form.cleaned_data['highlight']	    
		
    pretty_code, css_style = pretty_print(paste, style_choice)
    return render_to_response('pastey/detail.html',{'paste': paste, 'code': pretty_code, 'css_style': css_style, 'style_chooser': style_menu}, context_instance=RequestContext(request))

def list_page(request, list_id):
    paste_list = Code.objects.all().order_by('-pub_date')
    pastes = pretty_pastes(paste_list)    
 
    return render_to_response('pastey/list.html',{'pastes': pastes})
	
def index(request): 

    paste_list = Code.objects.all().order_by('-pub_date')[:10]
    pastes = pretty_pastes(paste_list)
    
    #form handling	
    if request.method == 'POST': 
        form = CodeForm(request.POST)
        if form.is_valid():
            a = form.save()
            return redirect(a)      
	   
    else: #maintain form data and redirect
        form = CodeForm() 
        
	
    
    return render_to_response('pastey/index.html', {'form': form, 'pastes': pastes}, context_instance=RequestContext(request))	
    
    

