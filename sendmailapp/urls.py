from django.urls import path
from .views import *

urlpatterns = [
    path('',GroupListView.as_view(),name='group-list'),
    path('<int:id>/',groupdetail,name='group-details'),
    path('<int:pk>/edit/',UpdateGroup.as_view(),name='group-update'),
    path('create/',CreateGroup.as_view(),name='group-create'),
    path('<int:pk>/delete/',DeleteGroup.as_view(),name='group-delete'),

]