"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('notes.urls')),
    path('admin/', admin.site.urls),
    path('register/', CreateView.as_view(
            template_name='registration/register.html',
            form_class=UserCreationForm,
            success_url='/'
    )),
    path("accounts/", include("django.contrib.auth.urls")),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static('static/', document_root=settings.BASE_DIR / "static")
urlpatterns += static('assets/', document_root=settings.BASE_DIR / "static")
