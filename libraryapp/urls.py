
from django.contrib import admin
from django.urls import path
from libraryapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.home,name='home'),
    path('addborrowers/', views.addborrowers,name='addborrowers'),
    path('booksearch/', views.booksearch,name='booksearch'),
    path('payfine/', views.payfine,name='payfine'),
    path('checkinbooks/', views.checkinbooks,name='checkinbooks'),
    path('', views.register,name='register'),
    path('login/', views.login,name='login'),

]
