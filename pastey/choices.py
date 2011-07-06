from pygments.styles import get_all_styles
from pygments.lexers import get_all_lexers

PYG_LANG_CHOICES = list(get_all_lexers())
PYG_LANG_CHOICES.sort()


#db value and internal name of languages and their lexers
LEXER_LIST = [desc[1] for desc in PYG_LANG_CHOICES]
FIRST_LEXERS = [name[0] for name in LEXER_LIST]
#human readable list of these language choices
READABLE_LANG_CHOICES = [desc[0] for desc in PYG_LANG_CHOICES]
#list of file extensions for these languages
PYG_LEXER_EXTS = [desc[2] for desc in PYG_LANG_CHOICES]

LEX_EXTS = []
for EXT_TUPS in PYG_LEXER_EXTS:
    try:       
        LEX_EXTS.append(EXT_TUPS[0])
    except:
        LEX_EXTS.append("*.txt")#use .txt if none provided


LANG_CHOICES = zip(FIRST_LEXERS, READABLE_LANG_CHOICES)
LANG_EXTS = zip(FIRST_LEXERS, LEX_EXTS)

PYG_STYLE_CHOICES = list(get_all_styles())
PYG_STYLE_CHOICES.sort()

READABLE_STYLE_CHOICES = PYG_STYLE_CHOICES
READABLE_STYLE_CHOICES = [str(name).capitalize() for name in READABLE_STYLE_CHOICES]

STYLE_CHOICES = zip(PYG_STYLE_CHOICES, READABLE_STYLE_CHOICES)
