import simplejson as json
from django.http import HttpResponseForbidden, HttpResponse
from django.utils.encoding import force_unicode
from django.db.models.base import ModelBase
 
class DJ_JSONEncoder(json.JSONEncoder):
    """ Encode Django Querysets, Models, or lists into JSON """
    
    def default(self,o):
        # for iterables (and querysets)
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
 
        # for models
        try:
            isinstance(o.__class__,ModelBase)
        except Exception:
            pass
        else:
            return force_unicode(o)
 
        return super(DJ_JSONEncoder,self).default(obj)
        
def serialize_to_json(obj,*args,**kwargs):
    """ A wrapper for json.dumps() with default cls=DJ_JSONEncoder:"""
    
    kwargs['cls'] = kwargs.get('cls',DJ_JSONEncoder)
 
    return json.dumps(obj,*args,**kwargs)

    
class JSONResponse(HttpResponse):
    """ JSON response class """
    
    def __init__(self,content='',json_opts={},mimetype="application/json",*args,**kwargs):        
        if content:
            content = serialize_to_json(content,**json_opts)
        else:
            content = serialize_to_json([],**json_opts)
            
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs) 
