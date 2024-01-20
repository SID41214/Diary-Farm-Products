from django.urls import path,re_path
from app import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm

urlpatterns = [
    #Home and Static Pages
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
   
   
    #Category views
    path('category/', views.Categoryview.as_view(), name='category'),  # For category without a slug
    path('category/<slug:val>/', views.Categoryview.as_view(), name='category_with_slug'),
    path('category-title/<val>/', views.CategoryTitle.as_view(),name='category-title'),
    path('product-detail/<int:pk>/',views.ProductDetail.as_view(),name='product-detail'),
    
    #User registration and authentication
    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm) ,name='login'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    # path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    # path('activate/<str:uidb64>/<slug:token>/', views.activate, name='activate'),
#    re_path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),  

    
    
    
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),    
    # path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
   
   
    #Cart and wishlist 
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
   
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    
    path('pluswishlist/',views.plus_wishlist,name='pluswishlist'),
    path('minuswishlist/',views.minus_wishlist,name='minuswishlist'),
    
    
    #orders and Search
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('orders/',views.orders,name='orders'),
    
    path('search/',views.search,name='search'),
    path('showwishlist/',views.show_wishlist,name='showwishlist'),
    
   
    #cart actions
    path('pluscart/',views.plus_cart,name='pluscart'),
    path('minuscart/',views.minus_cart,name='minuscart'),
    path('removecart/',views.remove_cart,name='removecart'),
    
   
   
   
   
    #password reset and change
    path('password_reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    
    #user profile and address
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('accounts/profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('updateaddress/<int:pk>',views.updateAddress.as_view(),name='updateaddress'),
   
    #pssword change
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=MyPasswordChangeForm,success_url='passwordchangedone/'),name='passwordchange'),
    path('passwordchange/passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    
    #password change
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    
    
    
    
    
]