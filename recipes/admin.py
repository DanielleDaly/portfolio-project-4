from django.contrib import admin
from .models import Recipe, Comment
# from .models import Recipe, Category
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'created_on', 'status')
    search_fields = ['title', 'cooking_time', 'serves', 'ingredients', 'method', 'created_on']
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('status', 'created_on')
    summernote_fields = ('ingredients', 'method',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'name', 'body', 'created_on', 'approved')
    search_fields = ['name', 'email', 'body']
    list_filter = ('approved', 'created_on')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

# @admin.register(Category)
# class CategoryAdmin(SummernoteModelAdmin):

#     prepopulated_fields = {"slug": ("category_name",)}





