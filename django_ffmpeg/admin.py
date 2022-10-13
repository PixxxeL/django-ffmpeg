from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ConvertingCommand, Video


def reconvert_video(modeladmin, request, queryset):
    queryset.update(convert_status='pending', last_convert_msg='')
reconvert_video.short_description = _('Convert again')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title_repr', 'created_at', 'convert_status', 'converted_at')
    list_display_links = ('title_repr',)
    readonly_fields = ('convert_status', 'last_convert_msg', 'convert_extension')
    actions = [reconvert_video]

    def title_repr(self, obj):
        return str(obj)
    title_repr.short_description = _('Title')

    def save_model(self, request, obj, form, change):
        if 'video' in form.changed_data and change:
            obj.convert_status = 'pending'
        if not change:
            obj.user = request.user
        super(VideoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Video, VideoAdmin)


class ConvertingCommandAdmin(admin.ModelAdmin): pass

admin.site.register(ConvertingCommand, ConvertingCommandAdmin)
