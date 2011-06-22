import datetime

from django.db import models
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from pygments.styles import get_all_styles
from pygments.lexers import get_all_lexers

from pastey.choices import LANG_CHOICES, STYLE_CHOICES

class Code(models.Model):
    code_paste = models.TextField('Code')
    language = models.CharField(max_length = 25, choices=(LANG_CHOICES), blank=True,null=True)
    title = models.CharField(max_length = 50, blank=True, null=True)	
    author = models.CharField(max_length = 50, blank=True,null=True)
    email = models.EmailField(max_length = 50, blank=True,null=True)

    private = models.BooleanField(default=False)
    pub_date = models.DateTimeField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/pastey/%i' % self.id
	
			
class CodeForm(ModelForm):

    class Meta:
        model = Code
        exclude = ('pub_date','private')

    def save(self):
        code = super(CodeForm, self).save(commit=False)
        code.pub_date=datetime.datetime.now()
        if not code.title:code.title = 'Code submission'
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
        
