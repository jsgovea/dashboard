from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from dashboardapp import views, apis


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Restaurant
    re_path(r'^restaurante/iniciar-sesion/$',
            auth_views.LoginView.as_view(template_name = 'restaurant/sign_in.html'),
            name = 'restaurant-sign-in'),
    re_path(r'^restaurante/registro/$',
            views.restaurant_sign_up,
            name='restaurant-sign-up'),
    re_path(r'^restaurante/cerrar-sesion',
            auth_views.LogoutView.as_view(next_page = '/'),
            name = 'restaurant-sign-out'),
    re_path(r'^restaurante/$', views.restaurant_home, name = 'restaurant-home'),

    re_path(r'^restaurante/cuenta/$', views.restaurant_account, name = 'restaurant-account'),
    re_path(r'^restaurante/menu/$', views.restaurant_meal, name = 'restaurant-meal'),
    re_path(r'^restaurante/menu/agregar/$', views.restaurant_add_meal, name = 'restaurant-add-meal'),
    re_path(r'^restaurante/menu/editar/(?P<meal_id>\d+)/$', views.restaurant_edit_meal, name = 'restaurant-edit-meal'),
    re_path(r'^restaurante/reportes/$', views.restaurant_report, name = 'restaurant-report'),
    re_path(r'^restaurante/ordenes/$', views.restaurant_order, name = 'restaurant-order'),



    # Sign in / Sign up / Sign out

    re_path(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # Convert-token sign up / Sign in
    # Revoke token sign out
               
    re_path(r'^api/restaurant/order/notification/(?P<last_request_time>.+)/$', apis.restaurant_order_notification),

                  #Apis for customers
    re_path(r'^api/customers/restaurants/$', apis.customer_get_restaurant),
    re_path(r'^api/customers/meals/(?P<restaurant_id>\d+)/$', apis.customer_get_meals),
    re_path(r'^api/customers/order/add/$', apis.customer_add_order),
    re_path(r'^api/customers/order/latest/$', apis.customer_get_latest_order),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
