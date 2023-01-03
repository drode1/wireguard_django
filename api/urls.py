from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router_v1 = DefaultRouter()

v1_urlpatterns = (
    [
        path('', include(router_v1.urls)),
    ],
    'v1'
)

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
