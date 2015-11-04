from django.conf.urls import url
from frontend import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from django.conf.urls import patterns, url

urlpatterns = format_suffix_patterns([
        url(r'^$', views.user_login),
    url(r'^groups$',
        views.GroupPage.as_view(),
        name='groups'),
    url(r'^show_system/(?P<pk>[0-9]+)/$',
        views.show_system,
        name='show_system'),
    url(r'^edit_news/(?P<pk>[0-9]+)/$',
        views.NewsHTML.as_view(),
        name='edit_news'),
    url(r'^remove_user/(?P<pk>[0-9]+)/$',
        views.ungroup_users,
        name='remove_user'),
    url(r'^ungroup_system/(?P<pk>[0-9]+)/(?P<grp>[0-9]+)/$',
        views.ungroup_system,
        name='ungroup_system'),
    url(r'^system_list$',
        views.SystemList.as_view(),
        name='system_list'),
    url(r'^system_HTML/(?P<pk>[0-9]+)/$',
        views.SystemHTML.as_view(),
        name='system_HTML'),
     url(r'^success$',
        views.RegistrationSuccess.as_view(),
        name='success'),
    url(r'^upload/(?P<pk>[0-9]+)/$',
        views.UploadDetail.as_view(),
        name='upload'),
    url(r'^uploads/(?P<pk>[0-9]+)/$',
        views.uploadlist,
        name='uploads'),
    url(r'^email/(?P<pk>[0-9]+)/$',
        views.email_group,
        name='email'),
    url(r'^newupload$',
        views.CreateUpload.as_view(),
        name='newupload'),
    url(r'^systems$',
        views.create_system,
        name='systems'),
    url(r'^download/(?P<pk>[0-9]+)/$',
        views.download,
        name='download'),
    url(r'^system/(?P<pk>[0-9]+)/$',
        views.SystemDetail.as_view(),
        name='system'),
    url(r'^users$',
        views.ListUser.as_view(),
        name='users'),
    url(r'^user/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user'),
    url(r'^process/(?P<pk>[0-9]+)/$',
        views.process_delete_view,
        name='process'),
    url(r'^grouplist/(?P<pk>[0-9]+)/$',
        views.grouplist,
        name='grouplist'),
    url(r'^system_delete/(?P<pk>[0-9]+)/$',
        views.system_delete,
        name='system_delete'),
  #   url(r'^api-auth/', 
  #     include('rest_framework.urls',
                # namespace='rest_framework')),
        url(r'^login', 
        views.user_login,
        name='login'),
    url(r'^processes', 
        views.ListProcess.as_view(),
        name='processes'),
    url(r'^uploadupdate', 
        views.UpdateUpload.as_view(),
        name='uploadupdate'),
    url(r'^register', 
    views.register,
    name='register'),
     url(r'^account', 
        views.Account.as_view(),
        name='account'),
      url(r'^signout', 
        views.Logout.as_view(),
        name='signout'),

      url(r'^about', 
        views.About.as_view(),
        name='about'),
      url(r'^news', 
        views.News.as_view(),
        name='news'),
      url(r'^conditions', 
        views.Conditions.as_view(),
        name='conditions'),
      url(r'^projects', 
        views.Projects.as_view(),
        name='projects'),
      url(r'^research', 
        views.Research.as_view(),
        name='research'),
      url(r'^publications', 
        views.Publications.as_view(),
        name='publications'),
      url(r'^user_edit', 
        views.user_edit,
        name='user_edit'),
])

# urlpatterns = [
#     url(r'^uploads/$', views.upload_list),
#     url(r'^uploads/(?P<pk>[0-9]+)/$', views.upload_detail),
#     url(r'^systems/$', views.system_list),
#     url(r'^systems/(?P<pk>[0-9]+)/$', views.system_detail