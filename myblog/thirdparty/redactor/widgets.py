from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from redactor.utils import json_dumps


GLOBAL_OPTIONS = getattr(settings, 'REDACTOR_OPTIONS', {})


class RedactorEditor(widgets.Textarea):
    init_js = '''<script type="text/javascript">
                    jQuery(document).ready(function(jQuery){
                        var $field = jQuery("#%s");
                        options = %s;
                        options.imageUploadErrorCallback = function(json){
                            alert(json.error);
                        };
                        $field.redactor(options);
                    });
                 </script>
              '''

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.custom_options = kwargs.pop('redactor_options', {})
        self.allow_file_upload = kwargs.pop('allow_file_upload', True)
        self.allow_image_upload = kwargs.pop('allow_image_upload', True)
        super(RedactorEditor, self).__init__(*args, **kwargs)

    @property
    def options(self):
        options = GLOBAL_OPTIONS.copy()
        options.update(self.custom_options)
        if self.allow_file_upload:
            options['fileUpload'] = reverse_lazy(
                'redactor_upload_file',
                kwargs={'upload_to': self.upload_to}
            )
        if self.allow_image_upload:
            options['imageUpload'] = reverse_lazy(
                'redactor_upload_image',
                kwargs={'upload_to': self.upload_to}
            )
        return options

    def render(self, name, value, attrs=None):
        html = super(RedactorEditor, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        json_options = json_dumps(self.options)
        html += self.init_js % (id_, json_options)
        return mark_safe(html)

    def _media(self):
        js = (
            'redactor/jquery.redactor.init.js',
            'redactor/redactor.js',
            'redactor/langs/{0}.js'.format(GLOBAL_OPTIONS.get('lang', 'en')),
        )

        if 'plugins' in self.options:
            plugins = self.options.get('plugins')
            for plugin in plugins:
                js = js + (
                    'redactor/plugins/{0}.js'.format(plugin),
                )

        js = js + (
            'redactor/langs/{0}.js'.format(GLOBAL_OPTIONS.get('lang', 'en')),
        )

        css = {
            'all': (
                'redactor/css/redactor.css',
                'redactor/css/django_admin.css',
            )
        }
        return forms.Media(css=css, js=js)
    media = property(_media)
