from datetime import datetime, timedelta

from celery.task import task
from celery.decorators import periodic_task

from pastey.models import Code, CodeForm

    
@periodic_task(run_every=timedelta(seconds=120))
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
    
