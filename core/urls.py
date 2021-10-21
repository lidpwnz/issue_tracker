"""core URL Configuration

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
from django.urls import path, include
from django.conf import settings
from issue_tracker.views.issues_views import IssuesRedirect
from core.errors import error_404
from django.conf.urls.static import static


handler404 = error_404

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', IssuesRedirect.as_view(), name='main_page'),
    path('issues/', include('issue_tracker.urls.issues_urls', namespace='issues')),
    path('projects/', include('issue_tracker.urls.projects_urls', namespace='projects')),
    path('accounts/', include('accounts.urls', namespace='acc')),
    path('', include('django.contrib.auth.urls')),
    path('api/v1/', include('api_v1.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
