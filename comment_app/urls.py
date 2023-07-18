from django.urls import path     
from . import views
urlpatterns = [ path('', views.index),
                         path('register', views.register),
             path('login', views.login),
               path('wall', views.wall),
               path('message', views.post_mes,name='message'), 
               path('comment', views.post_comm,name='comment'), 
               path('logout', views.register,name='logout'),    
               
                 ]