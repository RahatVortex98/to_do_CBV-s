from django.urls import path
from .views import  TaskList,TaskDetail,TaskCreate,TaskUpdate,Taskdelete,TaskLogin,Registration
from django.contrib.auth.views import LogoutView


urlpatterns = [
    
    path('login/',TaskLogin.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/',Registration.as_view(),name="register"),

    
    path('',TaskList.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
    path('create/', TaskCreate.as_view(),name='create'),
    path('update/<int:pk>/',TaskUpdate.as_view(),name='update'),
    path('delete/<int:pk>/',Taskdelete.as_view(),name='delete'),
    
    
    
]
