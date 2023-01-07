from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import AuthTelegramUser, UserViewSet
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

auth_patterns = (
    [
        path('auth/telegram/', AuthTelegramUser.as_view(),
             name='telegram-auth'),
    ],
    'auth'
)

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
    path('v1/', include(auth_patterns)),
]
