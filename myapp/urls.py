
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('service-worker.js', views.service_worker, name='service_worker'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pallifund/', views.pallifund_view, name='pallifund'),
    path('masapirivu/', views.masapirivu_view, name='masapirivu'),
    path('individual_statement/', views.individual_statement, name='individual_statement'),
    path('acc_statement/', views.acc_statement, name='acc_statement'),
    path('add_members/', views.add_members_view, name='add_members'),
    path('list_members/', views.list_members, name='list_members'),
    path('list_masapirivu/', views.list_masapirivu, name='list_masapirivu'),
]
