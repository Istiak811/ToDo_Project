from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
urlpatterns = [
    path('', views.TaskList.as_view(), name="tasks"),
    path('task-create/', views.TaskCreate.as_view(), name="task-create"),
    path('task-detail/<int:pk>/', views.TaskDetail.as_view(), name="task-detail"),
    path('task-update/<int:pk>/', views.TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', views.TaskDelete.as_view(), name="task-delete"),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('register/', views.RegisterPage.as_view(), name="register"),
    path('logout/', LogoutView.as_view(next_page = 'login'), name="logout"),
    # path('', views.home, name="home"),
]