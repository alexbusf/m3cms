from django.contrib import admin
from django import forms
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Post, Category

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'created')
    fields = ['description', 'title', 'category', 'content']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        super(PostAdmin, self).save_model(
            request=request,
            obj=obj,
            form=form,
            change=change
        )


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    fields = ['title', 'parent']
