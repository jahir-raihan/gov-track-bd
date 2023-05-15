from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-file/', views.upload_details, name='upload-details'),
    path('get-details/', views.get_details, name='get-details'),
    path('admin-page/', views.admin, name='admin-page'),
    path('issue-form/', views.issue_form, name='issue form'),
    path('get-admin-vizes/', views.get_admin_vizes, name='get-admin-vizes'),
    path('m-o-p/', views.proposal_approval, name='proposal_approval'),
    path('download-proj-data/', views.get_data_in_csv, name='download-proj-data')

]