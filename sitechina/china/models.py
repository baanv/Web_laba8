from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from transliterate import translit


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=China.Status.PUBLISHED)


class China(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    annotation = models.TextField(blank=True, verbose_name="Аннотация статьи",  null=True)
    models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts',
                               null=True, default=None)
    # cat_id = models.IntegerField(default=1, null=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категории")
    # cat = models.ForeignKey('Category', on_delete=models.CASCADE)

    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Тэги")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    # is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT,verbose_name="Статус")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")
    objects = models.Manager()
    published = PublishedModel()
    #image = models.ImageField(upload_to='photos/', null=True)
    translate = models.OneToOneField('Translate', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='title_in_rus', verbose_name="Перевод")

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create']), ]
        verbose_name = 'Информация о Китае'
        verbose_name_plural = 'Информация о Китае'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug':
                                           self.slug})

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name="Категория")

    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug':
                                               self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Create your models here.
class TagPost(models.Model):
    tag = models.CharField(max_length=100,
                           db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class Translate(models.Model):
    name = models.CharField(max_length=100)
    features = models.IntegerField(null=True)
    parts = models.IntegerField(null=True)
    tones = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

