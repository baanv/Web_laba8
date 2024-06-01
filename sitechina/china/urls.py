from django.contrib.auth.decorators import login_required
from django.template.defaulttags import url
from django.urls import path, register_converter

from china import views, converters

from china.views import ChinaCategory

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [

    #path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    #path('cats/<int:cat_id>/', views.categories, name='cats_id'),

    path('find/', views.find_information, name='find'),
    path('about/', views.about, name='about'),
    path('add/', views.AddPage.as_view(), name='add_page'),
    path('', views.ChinaHome.as_view(), name='home'),
    path('category/<slug:cat_slug>/', ChinaCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<slug:slug>/', views.DeletePost.as_view(), name='delete'),



    #path('add/', views.addpage, name='add_page'),

    #path('post/<slug:post_slug>/', views.show_post,  name='post'),

    #path('category/<slug:cat_slug>/', views.show_category, name='category'),
    #path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),

   # path('process_add/', views.process_add, name='process_add'),
]
