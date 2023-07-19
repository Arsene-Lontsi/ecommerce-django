from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('dashboard', views.dashboard, name="dashboard"),
	path('product/<int:pk>/', views.detail, name="detail"),
	path('product/<int:pk>/delete', views.delete_product, name="delete"),
	path('product/<int:pk>/edit/', views.edit_product, name="edit"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('signup/', views.signup, name="signup"),
	path('login/', auth_views.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name="login"),

	path('new/', views.new_product, name="new"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]