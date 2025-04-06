from .views import raffle_list, get_raffle_status
from .views import buy_ticket
from django.urls import path
from . import views

app_name = 'Topwinz_app'

urlpatterns = [
    path('', views.index, name='index'),
    path("about/", views.about, name="about"),
    path("details", views.details, name="details"),
    path("login/", views.login_view, name="login"),
    path('signup/', views.sign_up, name='signup'),
    path("logout/", views.logout_view, name="logout"),
    path('buy-ticket/<int:raffle_id>/', buy_ticket, name='buy_ticket'),
    path('raffles/', raffle_list, name='raffle_list'),
    path('raffle/status/<int:raffle_id>/', get_raffle_status, name='get_raffle_status'),
]

