from cgi import escape

from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect
from django.http import HttpResponse

from pastey.tasks import create_pdf


def render_to_pdf(template_src, context_dict):
    pdf, result, html = create_pdf(template_src, context_dict)    
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    else:
        return HttpResponse('Error processing PDF file<pre>%s</pre>' % escape(html))
        

