from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('aboutus/', views.AboutPageView, name='about'),
    path('contactus/', views.ContactPageView, name='contact'),
    path('new_post/', views.NewPostView.as_view() , name='new_post'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.EditPostView.as_view() , name='edit_post'),
    path('<int:pk>/delete', views.DeletePostView.as_view() , name='delete_post'),

]
