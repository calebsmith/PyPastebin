from pygments import highlight
from pygments.lexers import PythonLexer,  get_lexer_by_name, guess_lexer, get_all_lexers
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

from pastey.models import Style

def pretty_pastes(paste_list):
    """
    """
    style_choice = Style()  
    css_styles = []

    for paste in paste_list:
        paste.code_paste, temp_style = pretty_print(paste, style_choice)
        css_styles.append(temp_style)

    return zip(paste_list, css_styles)

def pretty_print(paste, style_choice):	
    """Use Pygments library to highlight a TextField       

    returns str1, str2
        where str1 is the formatted text, and str2 is the css style block
        
    Syntax:
        str, str = pretty_print(str)
        
    Ex:
        Views:
        pretty_text_output, style_output = pretty_print(source_code)
        
        Template:
        <style> {{style_output|safe}} </style>
        {{pretty_text_output|safe}}
    """
    if paste.language:lexer = get_lexer_by_name(paste.language, stripall=True)
    if not paste.language: lexer = guess_lexer(paste.code_paste, stripall=True)		
    if not style_choice.highlight: style_choice.highlight = 'colorful'	

    formatter = HtmlFormatter(linenos="table", cssclass="source", style= style_choice.highlight)
    result = highlight(paste.code_paste, lexer, formatter)		
    css_style = formatter.get_style_defs()		
    
    return result, css_style

