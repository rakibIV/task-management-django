from django.urls import path
from users.views import activate_user,GroupList,CustomLoginView,ProfileView,CreateGroup, CustomPasswordChangeView,CustomPasswordResetView, CustomPasswordResetConfirmView, EditProfileView, SignUpView, AdminDashboard, AssignRole
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    path("sign_up/",SignUpView.as_view(),name="sign-up"),
    # path("sign_in/",sign_in,name="sign-in"),
    path("sign_in/",CustomLoginView.as_view(),name="sign-in"),
    # path("logout/",sign_out,name="logout"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("activate/<int:user_id>/<str:token>",activate_user),
    path("admin/dashboard/",AdminDashboard.as_view(),name="admin-dashboard"),
    path("admin/<int:id>/assign-role/",AssignRole.as_view(),name="assign-role"),
    path("admin/create-group/",CreateGroup.as_view(),name="create-group"),
    path("admin/group-list/",GroupList.as_view(),name="group-list",),
    path("profile/",ProfileView.as_view(),name = "profile"),
    path("password_change/",CustomPasswordChangeView.as_view(),name="password-change"),
    path("password_change_done/",PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name="password_change_done"),
    path("password_reset/",CustomPasswordResetView.as_view(), name = "password-reset"),
    path("password_reset/confirm/<uidb64>/<token>/",CustomPasswordResetConfirmView.as_view(), name= "password_reset_confirm"),
    path("edit_profile/",EditProfileView.as_view(), name="edit-profile"),
    
]
