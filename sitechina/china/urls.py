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
    path('add/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<int:post_id>/', views.show_post,
         name='post'),
    path('category/<int:cat_id>/', views.show_category,
         name='category'),
]
