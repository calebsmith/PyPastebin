from datetime import datetime, timedelta

from celery.task import task
from celery.decorators import periodic_task

from pastey.models import Code, CodeForm

    
@periodic_task(run_every=timedelta(seconds= 900))
def delete_old():
    message = ""
    deletebool = False
    paste_list = Code.objects.all()
    for paste in paste_list:
        if datetime.now() > paste.del_date:
            deletebool = True
            message += "Entry " + str(paste.id) + " was deleted"
            if paste.txt_file: paste.txt_file.delete()            
            paste.delete()

            
    if not deletebool: message += "No old entries were found"
    return message

