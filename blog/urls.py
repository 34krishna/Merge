from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('', views.post_list, name='post_list'),  
    path('post/<str:slug>/', views.post_detail, name='post_detail'),  
    path('post_edit/<slug:slug>/', views.post_edit, name='post_edit'),  
    path('login/', views.login_page, name='login'),  
    path('logout/', views.logout_view, name='logout'),  
    path('signup/', views.signup, name='signup'),  
    path('profile/', views.profile, name='profile_view'), 
    path('edit-profile/', views.edit_profile, name='edit_profile'),  
    path('post_new/', views.post_new, name='post_new'),
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('Tags/', views.Tag, name='Tag'),
    path('profile/', views.profile, name='profile'),
    # path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),  

]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
