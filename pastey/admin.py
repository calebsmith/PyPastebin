from django.contrib import admin

from pastey.models import Code

def paste_delete(CodeAdmin, request, queryset):
    for obj in queryset:
        obj.txt_file.delete()        
        obj.delete()        
                
    paste_delete.short_description = "Delete selected pastes"

class CodeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Title',				{'fields': ['title']}),
        ('Author',               {'fields': ['author']}),
        ('Date of Publication', {'fields': ['pub_date']}),
        ('Date of Deletion', {'fields': ['del_date']}),
        ('Email Address',	{'fields': ['email']}),
        ('Programming Language', 	{'fields': ['language']}),
        ('Private', {'fields': ['private']}),
    ] 
    list_display = ('title', 'author', 'email', 'pub_date', 'del_date', 'language', 'private')
    list_filter = ('title', 'author', 'email', 'pub_date', 'del_date', 'language', 'private')
    search_fields = ['title', 'author', 'email', 'pub_date', 'del_date', 'language', 'private']
    actions = [paste_delete]
	
admin.site.register(Code, CodeAdmin)
admin.site.disable_action('delete_selected')
