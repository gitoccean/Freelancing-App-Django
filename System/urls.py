from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("fake/", views.fake_data, name='fake'),
    path("delete/<int:id>", views.delete, name='delete'),
    path("edit/<int:id>", views.edit, name='edit'),
    path("my_login/", views.my_login, name='my_login'),
    path("my_logout/", views.my_logout, name='my_logout'),
    path("my_signup", views.my_signup, name='my_signup'),
    path("activation/<str:id>/", views.activation, name='activation')
]