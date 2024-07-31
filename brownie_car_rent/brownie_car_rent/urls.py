"""car_rental_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(r'', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(r'', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import path, include
    3. Add a URL to urlpatterns:  path(r'blog/', include(blog_urls))
"""
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from system.views import admin_car_list, admin_msg, order_list, car_created, order_update, order_delete, msg_delete, base_dash
from account.views import (register_view,  admin_register_view, login_view, logout_view)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_dash/', base_dash, name='base_dash'),
    path('', admin_car_list, name='adminIndex'),
    path('listOrder/', order_list, name="order_list"),
    path('<int:id>/editOrder/', order_update, name="order_edit"),
    path('<int:id>/deleteOrder/', order_delete, name="order_delete"),
    path('create/', car_created, name="car_create"),
    path('message/', admin_msg, name='message'),
    path('<int:id>/deletemsg/', msg_delete, name="msg_delete"),
    path('car/', include('system.urls')),
    path('register/', register_view, name='register'),
    # path('verify_email/', verify_email_view, name='verify_email'),
    path('admin_register/', admin_register_view, name='admin_register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)