from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('login/', LoginView.as_view(template_name='accounts/login.html' ,form_class=LoginForm), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
]