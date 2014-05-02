from django.forms import Widget
from django.utils.safestring import mark_safe


class LinkWidget(Widget):
    def __init__(self, text, url='%s', *args, **kwargs):
        self.url = url
        self.text = text

        super(LinkWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        output = '<a href="{}">{}</a>'.format(self.url, self.text)
        return mark_safe(output)