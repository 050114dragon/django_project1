"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

import user_agents
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path

from rest_framework import permissions
from rest_framework.decorators import api_view

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


from django.urls import re_path
from django.views.static import serve
from django.conf import settings


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



    


swagger_info = openapi.Info(
    title="Snippets API",
    default_version='v1',
    description="""This is a demo project for the [drf-yasg](https://github.com/axnsan12/drf-yasg) Django Rest Framework library.

The `swagger-ui` view can be found [here](/cached/swagger).
The `ReDoc` view can be found [here](/cached/redoc).
The swagger YAML document can be found [here](/cached/swagger.yaml).

You can log in using the pre-existing `admin` user with password `passwordadmin`.""",  # noqa
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="BSD License"),
)

SchemaView = get_schema_view(
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=[permissions.AllowAny],
)


def root_redirect(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = user_agents.parse(user_agent_string)

    if user_agent.is_mobile:
        schema_view = 'cschema-redoc'
    else:
        schema_view = 'cschema-swagger-ui'

    return redirect(schema_view, permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("app01/",include("app01.urls")),
    #  re_path(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0),
    #             name='schema-json'),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('redoc-old/', SchemaView.with_ui('redoc-old', cache_timeout=0), name='schema-redoc-old'),
    re_path(r'^cached/swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=None),
            name='cschema-json'),
    path('cached/swagger/', SchemaView.with_ui('swagger', cache_timeout=None), name='cschema-swagger-ui'),
    path('cached/redoc/', SchemaView.with_ui('redoc', cache_timeout=None), name='cschema-redoc'),
    path('', root_redirect),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT},name='media'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

