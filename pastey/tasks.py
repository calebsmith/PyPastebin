from datetime import datetime, timedelta
import cStringIO as StringIO
from cgi import escape

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from celery.task import task
from celery.decorators import periodic_task

import ho.pisa as pisa

from pastey.models import Code, CodeForm


@periodic_task(run_every=timedelta(seconds=900))
def find_old():
    delete_sum = 0
    paste_list = Code.objects.all()
    
    for paste in paste_list:
        if datetime.now() > paste.del_date:
            delete_sum += 1
            delete_old(paste)

    if delete_sum: message = str(delete_sum) + " entries were deleted"            
    else: message = "No old entries were found"
    return message

@task
def delete_old(paste):
    if paste.txt_file: paste.txt_file.delete()            
    paste.delete()
    return 
    
@task
def create_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    return pdf, result
