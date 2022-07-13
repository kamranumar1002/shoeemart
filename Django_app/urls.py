from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('products', views.products, name='products'),
    path('register', views.register, name='register'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('useraddress', views.useraddress, name='useraddress'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    # path('addaddress', views.addaddress, name='addaddress'),
    path('editaddress', views.editaddress, name='editaddress'),
    path('editaddress2', views.editaddress2, name='editaddress2'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('viewproduct/<int:id>', views.viewProduct, name='viewproduct'),
    path('ok', views.ok, name='ok'),
    path('ok2', views.ok2, name='ok2'),
    path('ok3', views.ok3, name='ok3'),
    path('ok4', views.ok4, name='ok4'),
    path('ok5', views.ok5, name='ok5'),
    path('sai', views.sai, name='sai'),
    
]
