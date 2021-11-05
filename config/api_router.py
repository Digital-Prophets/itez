from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from itez.users.api.views import UserViewSet
from itez.beneficiary.api.views import ProvinceList, DistrictList

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("provinces", ProvinceList)
router.register("districts", DistrictList)


app_name = "api"
urlpatterns = router.urls
