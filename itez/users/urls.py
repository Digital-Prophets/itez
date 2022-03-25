from django.urls import path


from users.views import (
    update_view,
    # UserUpdateView,
    user_delete,
    user_detail_view,
    user_redirect_view,
    UserCreateView,
    user_profile,
    user_profile_photo_update,
)

app_name = "users"
urlpatterns = [
    path("user/create/", UserCreateView.as_view(), name="user_create"),
    path("user/delete/<int:user_id>", user_delete, name="delete"),
    path("user/profile/photo/upload/", user_profile_photo_update, name="profile_photo"),
    path("user/profile/", user_profile, name="profile"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("update/<int:pk>/", view=UserUpdateView.as_view(), name="update"),
    path("update/<int:pk>/", view=update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
