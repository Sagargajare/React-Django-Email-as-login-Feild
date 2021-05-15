from djoser import views

from django.urls import path
from . import views

urlpatterns = [

    path('signup/students/', views.StudentsRegisterView.as_view()),
    path('signup/mentor/', views.MentorsRegisterView.as_view()),

]


# router = DefaultRouter()
# router.register("sregister", views.UserViewSet)

# User = get_user_model()

# urlpatterns += router.urls
