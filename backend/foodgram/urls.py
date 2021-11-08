from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

api_patterns = [
    path('', include('recipes.urls')),
    path('', include('users.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    # path('redoc/', TemplateView.as_view(template_name='data/redoc.html'),
    #      name='redoc')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
