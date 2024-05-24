from django.urls import path, register_converter

from china import views, converters

register_converter(converters.FourDigitYearConverter, "year4")
urlpatterns = [
    path('', views.index, name='home'),
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    path('cats/<int:cat_id>/', views.categories, name='cats_id'),
    path('archive/<year4:year>/', views.archive),
    path('dict/', views.dictionary, name='dict'),
    path('find/', views.find_information, name='find'),
    path('about/', views.about, name='about'),
    path('add/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post,
         name='post'),

    path('category/<slug:cat_slug>/', views.show_category,
         name='category'),
    path('tag/<slug:tag_slug>/',
         views.show_tag_postlist, name='tag'),

   # path('process_add/', views.process_add, name='process_add'),
]
