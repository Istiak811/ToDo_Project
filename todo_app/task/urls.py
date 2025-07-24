from django.urls import path
from . import views
urlpatterns = [
    path('', views.TaskList.as_view(), name="tasks"),
    path('task-create/', views.TaskCreate.as_view(), name="task-create"),
    path('task-detail/<int:pk>', views.TaskDetail.as_view(), name="task-detail"),
    path('task-update/<int:pk>', views.TaskUpdate.as_view(), name="task-update"),
    # path('', views.home, name="home"),
]