from django.urls import path
from accounts.views import signup,userLogin,userLogout,verify_email
                             
urlpatterns = [
    path('signup', signup, name='signup'),
    path('verify-email', verify_email, name='verify_email'),
    path('login', userLogin, name='login'), 
    path('logout', userLogout, name='logout'),    
]
