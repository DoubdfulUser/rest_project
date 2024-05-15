


from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView
from rest_framework.schemas import get_schema_view
from converter import settings
from users.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('converter_app.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('api/v1/users/', UserAPIList.as_view(), name='user-list'),
    path('api/v1/users/<int:pk>/', UserAPIUpdate.as_view(), name='user-update'),
    path('api/v1/userdelete/<int:pk>/', UserAPIDestroy.as_view(), name='user-delete'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('payments/', include('payments.urls')),
    path('payments/', include('mypaymentapp.urls')),
    path('api_schema', get_schema_view(title='API Schema'), name='api_schema'),
    path('swagger-ui/', SwaggerUIView.as_view(), name='swagger-ui')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


