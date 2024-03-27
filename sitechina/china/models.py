from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=China.Status.PUBLISHED)


class China(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(blank=True)
    annotation = models.TextField(blank=True)
    # cat_id = models.IntegerField(default=1, null=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    # cat = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedModel()
    image = models.ImageField(upload_to='photos/', null=True)
    translate = models.OneToOneField('Translate', on_delete=models.SET_NULL, null=True, blank=True, related_name='title_in_rus')

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create']), ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug':
                                           self.slug})

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100,
                            db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug':
                                               self.slug})

    def __str__(self):
        return self.name


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


