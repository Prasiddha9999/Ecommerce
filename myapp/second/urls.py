from django.urls import path
from . import views
from django.http import request
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name="index"),
    path('add_to_cart/<int:item_id>/', views.AddToCartView, name='add_to_cart'),
    path('cart/', views.CartView, name='cart'),
    path('remove_from_cart/<int:item_id>/', views.RemoveFromCartView, name='remove_from_cart'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('logout/', views.logout_view, name='logout'),
    path('order/', views.process_order, name='process_order'),
    path('myorder/', views.order_view, name='order_view'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)