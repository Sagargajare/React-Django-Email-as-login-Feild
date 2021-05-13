from django.urls import path, re_path

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r'', TemplateView.as_view(template_name="frontend/index.html")),
    # match all other pages

]
