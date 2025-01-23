"""
URL configuration for nephele project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from ninja_extra import NinjaExtraAPI
from debug_toolbar.toolbar import debug_toolbar_urls
from django.http import HttpResponse
import datetime

api = NinjaExtraAPI(
    title="Nephele API",
    version="1.0.0",
    description="Nephele API",
)


@api.get("/status", tags=["status"])
def add(request):
    """status check for a liveness probe"""
    return {"status": "ok"}


def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html lang="en"><body>Hi!, It is now %s.</body></html>' % now
    return HttpResponse(html)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("", current_datetime),
] + debug_toolbar_urls()
