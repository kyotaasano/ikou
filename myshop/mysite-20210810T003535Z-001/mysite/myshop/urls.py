from django.urls import path
from . import views

app_name = 'myshop'

urlpatterns = [
        path('',views.index,name='index'),
        path('',views.index,name='base'),
        path('detail/', views.IndexView.as_view(), name='index'),
        path('detail/<str:itemCode>', views.DetailView.as_view(), name='detail'),
        path('create/', views.create, name='create'),
        path('edit/<int:id>', views.edit, name='edit'),
        path('delete/<int:id>', views.delete, name='delete'),
        path('accounts/signup/', views.SignUp.as_view(), name='signup'),
]
