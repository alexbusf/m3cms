from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField

#Category model
class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            db_index=True)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    def get_absolute_url(self):
        return reverse('post-by-category', args=[str(self.slug)])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

#Post model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    category = TreeForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    #content = models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Posts'
        verbose_name = 'Post'
        permissions = (("can_post_create_edit", "Set post create and edit"), ("can_post_delete", "Set post delete"),)

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.slug)])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
