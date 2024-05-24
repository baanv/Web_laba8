from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import China, Category
class TranslateFilter(admin.SimpleListFilter):
    title = 'Наличие перевода'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('translate', 'Переведено'),
            ('no_translate', 'Не переведено'),
        ]
    def queryset(self, request, queryset):
        if self.value() == 'translate':
            return queryset.filter(translate__isnull=False)
        elif self.value() == 'no_translate':
            return queryset.filter(translate__isnull=True)
@admin.register(China)
class ChinaAdmin(admin.ModelAdmin):
    #exclude = ['tags', 'is_published']
    fields = ['title', 'content','annotation', 'slug', 'cat', 'tags', 'photo']
    list_display = ('title', 'post_photo', 'annotation',
                    'is_published', 'cat')
    readonly_fields = ['slug']
    filter_horizontal = ['tags']
   # list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info', 'brief_content')
    list_display_links = ('title',)
    list_editable = ('is_published', 'cat',)
    ordering = ['-time_create', 'title']
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [TranslateFilter, 'cat__name', 'is_published']
    # list_per_page = 5
    save_on_top = True

    @admin.display(description="Изображение")
    def post_photo(self, china: China):
        if china.photo:
            return mark_safe(f"<img src='{china.photo.url}'width=50>")
        return "Без фото"


    @admin.display(description="Краткое содержание")
    def brief_content(self, china: China):
        return china.annotation

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=China.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=China.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

# admin.site.register(China, ChinaAdmin)
# Register your models here.
# manage.py migrate
