from pygments import highlight
from pygments.lexers import PythonLexer,  get_lexer_by_name, guess_lexer, get_all_lexers
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

from pastey.models import Style

DEFAULT_STYLE = 'emacs'

def tersify(pastes, charlimit=400):
    """returns a list of Code objects with a truncated code field.
    
    The function takes a list of Code objects as its first argument and returns
    this list. Thee character limit defaults to 400 and can be set by calling 
    the function with a second argument. 
    
    The truncated text will contain ... concatenated at the end.
    """
    
    for paste in pastes:
        if len(paste.code_paste) > charlimit or charlimit == 0:
            paste.code_paste = paste.code_paste[:charlimit]
            paste.code_paste += '...'
    return pastes

def pretty_print(paste, style_choice, linenos = "inline", full = False):	
    """Use Pygments library to highlight a TextField       

    returns str1, str2
        where str1 is the formatted text, and str2 is the css style block
        
    Syntax:
        code_str, style_str = pretty_print(code_str)
        
    Ex:
        Views:
        pretty_text_output, style_output = pretty_print(source_code)
        
        Template:
        <style> {{style_output|safe}} </style>
        {{pretty_text_output|safe}}
    """
    if paste.language:lexer = get_lexer_by_name(paste.language, stripall=True)
    if not paste.language: lexer = guess_lexer(paste.code_paste, stripall=True)		
    if not style_choice.highlight: style_choice.highlight = DEFAULT_STYLE	
    
    
    
    formatter = HtmlFormatter(linenos = linenos, full = full, cssclass="source", style= style_choice.highlight)
    result = highlight(paste.code_paste, lexer, formatter)		
    css_style = formatter.get_style_defs()		

    return result, css_style

def pretty_pastes(paste_list):
    """Applies pretty_print and enumerates every object in a list
    
    Use: paste_list = pretty_pastes(paste_list)
    where paste_list contains the Code objects to be listed
    
    The function returns a list of two tuples in which the first variable 
    contains the paste object while the second contains the style text to be 
    used in the template. The style used is the default value DEFAULT_STYLE.
    """
   
    item_index = []
    for i in range(1, len(paste_list) + 1):
        item_index.append(i)
    
    style_choice = Style()  
    css_styles = []
    
    for paste in paste_list:
        paste.code_paste, temp_style = pretty_print(paste, style_choice)
        css_styles.append(temp_style)
    
    paste_list = zip(item_index, css_styles, paste_list)
    
    return paste_list

