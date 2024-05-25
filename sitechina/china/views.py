from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
import uuid

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, ListView, DetailView, FormView, UpdateView, DeleteView

from china.forms import AddPostForm, UploadFileForm
from china.models import China, Category, TagPost, UploadFiles
from django.views import View

from china.templatetags.utils import DataMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name':
            'add_page'},
        {'title': "Обратная связь", 'url_name':
            'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

cats_db = [
    {'id': 1, 'name': 'История'},
    {'id': 2, 'name': 'Города'},
    {'id': 3, 'name': 'Провинции'},
    {'id': 4, 'name': 'Личности'},
    {'id': 5, 'name': 'Праздники'},
]

# Create your views here.

'''def index(request):
    posts = China.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'china/index.html',
                  context=data)'''


class ChinaHome(DataMixin, ListView):
    template_name = 'china/index.html'
    context_object_name = 'posts'


    def get_queryset(self):
        return China.published.all().select_related('cat')
    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs), title='Главная страница', cat_selected=0)


class ChinaCategory(DataMixin, ListView):
    template_name = 'china/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected = cat.id,)

    def get_queryset(self):
        return China.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


class TagPostList(DataMixin, ListView):
    template_name = 'china/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                  title='Тег: ' + tag.tag)
    def get_queryset(self):
        return China.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = China
    template_name = 'china/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=context['post'])

    def get_object(self, queryset=None):
        return get_object_or_404(China.published, slug=self.kwargs[self.slug_url_kwarg])


def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):

    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()

    else:
        form = UploadFileForm()
    return render(request, 'china/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def find_information(request):
    posts = China.published.all()
    data = {
        'title': 'Поиск статьи',
        'menu': menu,
        'posts': posts,

    }
    return render(request, 'china/find.html',
                  context=data)


'''
def show_post(request, post_slug):
    post = get_object_or_404(China, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,

    }
    return render(request, 'China/post.html',
                  context=data)

'''

'''
def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'china/addpage.html',
                  {'menu': menu, 'title': 'Добавление статьи', 'form':
                      form})


class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'china/addpage.html'
    success_url = reverse_lazy('home')

    def get(self, request):
        form = AddPostForm()
        return render(request, 'china/addpage.html',
                      {'menu': menu, 'title': 'Добавление статьи', 'form':
                          form})

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'china/addpage.html',
                      {'menu': menu, 'title': 'Добавление статьи', 'form':
                          form})
'''


class AddPage(DataMixin, CreateView):
    model = China
    fields = ['title', 'slug', 'content',
              'is_published', 'cat']
    # form_class = AddPostForm
    template_name = 'china/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):
    model = China
    fields = ['title', 'content', 'annotation', 'photo', 'is_published', 'cat']
    template_name = 'china/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
class DeletePost(DataMixin, DeleteView):
    model = China
    template_name = 'china/delete.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'


'''def contact(request):
    return render(request, 'china/contact.html',
                  {'title': 'Обратная связь', 'menu': menu})

'''
def login(request):
    return render(request, 'china/login.html',
                  {'title': 'Вход', 'menu': menu})




def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = China.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'china/index.html',
                  context=data)


'''def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=China.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'china/index.html', context=data)
'''
