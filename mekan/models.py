from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, TextInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from home.models import UserProfile


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    CategoryImage = models.ImageField(blank=True, upload_to='assets/images/')  # py -m pip install --upgrade Pillow
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        # level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.CategoryImage.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Place(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    detail = RichTextUploadingField(blank=True)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(upload_to='images/', max_length=255)  # py -m pip install --upgrade Pillow
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'slug': self.slug})


class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ['category', 'title', 'slug', 'keywords', 'description', 'country', 'city', 'image', 'detail']
        widgets = {
            'Başlık': TextInput(attrs={'class': 'input', 'placeholder': 'Başlık'}),
            'Keywords': TextInput(attrs={'class': 'input', 'placeholder': 'Keywords'}),
            'Tanım': TextInput(attrs={'class': 'input', 'placeholder': 'Tanım'}),
            'Ülke': TextInput(attrs={'class': 'input', 'placeholder': 'Ülke'}),
            'Şehir': TextInput(attrs={'class': 'input', 'placeholder': 'Şehir'}),
            'Kategori': Select(attrs={'class': 'input', 'placeholder': 'Kategori'}, choices=(
                Category.objects.all()
            )),
            'Resim': FileInput(attrs={'class': 'input', 'placeholder': 'Resim'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'Detay': CKEditorWidget(),
        }


class Images(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/', max_length=255)  # py -m pip install --upgrade Pillow

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'


class ImagesForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']


class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    userprofil = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=200, blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
