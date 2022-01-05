from django.utils.html import format_html
from django.contrib.admin.widgets import AdminFileWidget

class AdminImageWidget(AdminFileWidget):
    """Admin widget for showing clickable thumbnail of Image file fields"""

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and getattr(value, 'url', None):
            html = format_html('<a href="{0}" target="_blank"><img src="{0}" alt="{1}" style="object-fit: contain;height:150px;width:auto"/></a>', value.url, str(value)) + html
        return html
