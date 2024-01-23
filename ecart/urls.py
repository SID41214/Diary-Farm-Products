
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings # new
from  django.conf.urls.static import static #new


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    # path('',include('customadmin.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)

admin.site.site_header="Diary Products"
admin.site.site_title="Diary Products"
admin.site.site_index_title=" Welcome to Diary Products"