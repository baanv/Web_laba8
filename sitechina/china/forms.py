from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import uuid
from .models import Category, Translate, China, TagPost
from django.core.validators import MinLengthValidator, MaxLengthValidator


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")


@deconstructible
class AddPostForm(forms.ModelForm):
    class Meta:
        model = China
        fields = ['title', 'slug', 'content', 'annotation', 'is_published', 'cat', 'tags', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'annotation': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        }

    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label="Категория не выбрана", label="Категории")
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), widget=forms.SelectMultiple, label="Теги")

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title



