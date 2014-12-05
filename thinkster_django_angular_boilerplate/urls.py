from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from rest_framework_nested import routers

from thinkster_django_angular_boilerplate.views import IndexView
from thinkster_django_angular_boilerplate.authentication.views import \
    AccountViewSet


router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(router.urls)),
    url(r'^', TemplateView.as_view(template_name='index.html')),
)
