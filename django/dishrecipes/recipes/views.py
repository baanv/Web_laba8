from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.defaultfilters import slugify

menu = [{'title': "Поиск рецептов", 'url_name': 'find'},
        {'title': "Войти", 'url_name': 'login'},
        {'title': "Добавить свой рецепт", 'url_name': 'add'},
        {'title': "О сайте", 'url_name': 'about'},
        ]

data_db = [
    {'id': 1, 'title': 'Котлета по-киевски', 'content':
        '<b>Котлета по-киевски</b> — блюдо русской и украинской кухонь, представляющее собой панированное отбивное куриное филе, в которое завёрнут кусочек сливочного масла. '
        'Изначально масло вбивалось в котлету кулинарным молотком, что делало вкус филе сливочным, при поточном производстве масло стали просто заворачивать. '
        'Получившаяся котлета имеет эллипсоидную форму. '
        'Жарят во фритюре, предварительно дважды панируют с льезоном. '
        'В масло можно добавлять тёртый сыр, грибы, зелень, яичный желток и пр. '
        'Блюдо подают на гренке (крутоне). Часто при разделке филе сохраняют косточку, на которую при подаче на стол надевается папильотка. ',
     'is_published': True, 'category': 1},
    {'id': 2, 'title': 'Гуляш', 'content':
        '<b>Гуля́ш</b> — национальное блюдо венгров и чехов: кусочки говядины или телятины, тушенные с копчёным шпиком, луком, перцем (паприкой) и картофелем. '
        'Блюдо относится к категории густых супов. '
        'Изначально суп с различными добавками был традиционной едой венгерских пастухов и готовился в котлах на костре, но обрёл международное признание благодаря 39-му венгерскому пехотному полку, переведённому в конце XIX века из Дебрецена в Вену. '
        'Полевая кухня на немецком языке носит ироническое название «гуляшная пушка».', 'is_published': True,
     'category': 1},
    {'id': 3, 'title': 'Плов', 'content':
        '<b>Плов</b> — блюдо восточной кухни, основу которого составляет варёный рис (в исключительных случаях — другая крупа или мелкие макаронные изделия). '
        'Отличительным свойством плова является его рассыпчатость, достигаемая соблюдением технологии приготовления риса и добавлением в плов животного или растительного жира, препятствующего слипанию крупинок.'
        'Посуда для подачи плова на стол называется пловница, в Средней Азии — ляган или табак/тавак/товок.',
     'is_published': True, 'category': 1},
    {'id': 4, 'title': 'Тарталетки', 'content':
        '<b>Тарталетки</b> Тарталетки с отварным куриным филе, вареными яйцами и обжаренными шампиньонами с луком - очень вкусная и сытная закуска. '
        'Тарталетки с курицей и грибами отлично подойдут для любого праздничного стола.',
     'is_published': True, 'category': 2},
    {'id': 5, 'title': 'Торт Наполеон', 'content':
        '<b>Торт Наоплеон</b> — многослойный торт из слоёного теста с масляным (или заварным) кремом.',
     'is_published': True, 'category': 3},
]

cats_db = [
    {'id': 1, 'name': 'Горячее'},
    {'id': 2, 'name': 'Закуски'},
    {'id': 3, 'name': 'Десерты'},
]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'recipes/index.html',
                  context=data)


def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'recipes/cats.html',
                  context=data)


def archive(request, year):
    if year > 2024:
        return redirect('home', permanent=True)

    return HttpResponse(f"<h1>Архив рецептов по годам</h1><p >{year}</p>")


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def add_recipe(request):
    return render(request, 'recipes/add.html',
                  {'title': 'Добавить свой рецепт', 'menu': menu})

def about(request):
    return render(request, 'recipes/about.html',
                  {'title': 'О сайте', 'menu': menu})


def find(request):
    data = {
        'title': 'Поиск рецептов',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'recipes/find.html',
                  context=data)


def login(request):
    return render(request, 'recipes/login.html',
                  {'title': 'Вход', 'menu': menu})


