from django.contrib import admin

from web.models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'link')


admin.site.register(Content, ContentAdmin)
