from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView
from project_twitter.twitter import views as twitter_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('twitter/', include('project_twitter.twitter.urls')),
    path('login/', LoginView.as_view(template_name="twitter/login.html"), name='login'),
    path('', RedirectView.as_view(url='/twitter/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = twitter_views.custom_404