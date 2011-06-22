from pygments.styles import get_all_styles
from pygments.lexers import get_all_lexers

PYG_LANG_CHOICES = list(get_all_lexers())
PYG_LANG_CHOICES.sort()

LEXER_LIST = [desc[1] for desc in PYG_LANG_CHOICES]
FIRST_LEXERS = [name[0] for name in LEXER_LIST]
READABLE_LANG_CHOICES = FIRST_LEXERS
READABLE_LANG_CHOICES = [str(name).capitalize() for name in READABLE_LANG_CHOICES]

LANG_CHOICES = zip(FIRST_LEXERS, READABLE_LANG_CHOICES)

PYG_STYLE_CHOICES = list(get_all_styles())
PYG_STYLE_CHOICES.sort()

READABLE_STYLE_CHOICES = PYG_STYLE_CHOICES
READABLE_STYLE_CHOICES = [str(name).capitalize() for name in READABLE_STYLE_CHOICES]

STYLE_CHOICES = zip(PYG_STYLE_CHOICES, READABLE_STYLE_CHOICES)
