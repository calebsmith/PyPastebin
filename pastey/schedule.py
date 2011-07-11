from datetime import datetime, timedelta

from celery.decorators import periodic_task

from models import Code, CodeForm


@periodic_task(run_every=timedelta(seconds=10))
def delete_old():
    paste_list = Code.objects.all()
    for paste in paste_list:
        if datetime.datetime.now() > paste.del_date:
            if paste.txt_file: paste.txt_file.delete()
            paste.delete()
            return "Old entry deleted"
    return
    
    
