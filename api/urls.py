from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from wireguard.views import AllowedIpApiView, DnsApiView, PeerViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'peers', PeerViewSet, basename='peers')
router_v1.register(r'dns', DnsApiView, basename='dns')
router_v1.register(r'allowed-ips', AllowedIpApiView, basename='allowed-ips')

v1_urlpatterns = (
    [
        path('', include(router_v1.urls)),
    ],
    'v1'
)

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
