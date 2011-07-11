from datetime import datetime, timedelta

from celery.task import task
from celery.decorators import periodic_task

from pastey.models import Code, CodeForm

    
@periodic_task(run_every=timedelta(seconds= 10))
def delete_old():
    message = "Checked for old entries to delete: "
    deletebool = False
    paste_list = Code.objects.all()
    for paste in paste_list:
        if datetime.now() > paste.del_date:
            deletebool = True
            if paste.txt_file: paste.txt_file.delete()            
            paste.delete()
            message += "Entry " + paste.id + " was deleted"
            
    if not deletebool: message += "None found"
    return message
