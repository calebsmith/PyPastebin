import datetime

from django.db import models
from django.forms import ModelForm
from django import forms

from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile

from dateutil.relativedelta import relativedelta

from pygments.lexers import get_lexer_for_filename

from pastey.choices import *

class Code(models.Model):
    code_paste = models.TextField('Code', blank=True, null=True)
    language = models.CharField(max_length = 25, choices=(LANG_CHOICES), blank=True,null=True, default="python")

    #file upload option
    txt_file = models.FileField("From File", upload_to="user_file/", blank=True, null=True)

    title = models.CharField(max_length = 50, blank=True, null=True)	
    author = models.CharField(max_length = 50, blank=True,null=True)
    email = models.EmailField(max_length = 50, blank=True,null=True)

    private = models.BooleanField()
    pub_date = models.DateTimeField()
    del_date = models.DateTimeField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/pastey/detail/%i' % self.id
	
			
class CodeForm(ModelForm):

    class Meta:
        model = Code
        exclude = ('pub_date','del_date')     
        
    def save(self):
        code = super(CodeForm, self).save(commit=False)
        
        code.pub_date = datetime.datetime.now()
        code.del_date = datetime.datetime.now() + relativedelta(days=+7)

        if code.txt_file:
            #Use the filename as the title if the user does not choose a title
            if not code.title: code.title = code.txt_file.name
            
            #find the lexer based on file extension before we add the timestamp
            code.language = find_file_lexer(code.txt_file.name)
            
            #add a unique timestamp
            name = str(code.pub_date.strftime('%f')) + "-" + code.txt_file.name
            content = code.txt_file
            
            #save file content
            code.txt_file.save(name, content)
            
            #set code_paste to match file content
            f = File(code.txt_file)
            code.code_paste = ""
            for chunk in f.chunks():
                code.code_paste += chunk
            f.close()          
            
        else:
            ext = find_lang_ext(code.language)            
            if not code.title: code.title = 'file'          
            name = code.title + str(code.pub_date.strftime('%f')) + ext
            if code.title == 'file': code.title = "Untitled Submission"
            
            content = ContentFile(str(code.code_paste))
            code.txt_file.save(name, content)
            code.txt_file.close()
            
        if not code.author:code.author = 'an unknown author'
        
        code.save()
        return code


class Style(models.Model):

    highlight = models.CharField('Style',max_length = 50, blank=True,null=True, choices=(STYLE_CHOICES))
	
    def __unicode__(self):
        return self.highlight


class StyleForm(ModelForm):
	
    class Meta:
        model = Style
        
        
        
class Search(models.Model):
    
    field_choices = [('title', 'Title') ,('author', 'Author'),('email', 'Email'),('language','Language')]
    keyword = models.TextField('Search')
    field = models.CharField(max_length = 25, choices=field_choices, default="title")
    
    def __unicode__(self):
        return self.keyword

class SearchForm(ModelForm):
    
    class Meta:
        model = Search


def find_lang_ext(language):
    """Find an appropriate file extension based on the choice of language
    """
    
    x = [x[0] for x in LANG_EXTS]
    try:
        extension = LEX_EXTS[x.index(language)]
    except:
        extension = "*.txt"
    ext = str(extension)[1:]        
    return ext

def find_file_lexer(filename):
    """Use Pygments get_lexer_for_filename to set the language for file uploads
    """
    
    try:
        lex = get_lexer_for_filename(filename)
        name = lex.aliases[0]
    except:
        name = ""     
    return name
         
