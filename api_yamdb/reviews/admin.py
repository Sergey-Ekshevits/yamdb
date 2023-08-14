from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    list_editable = ('slug',)
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    list_editable = ('year', 'category')
    search_fields = ('name',)
    list_filter = ('category',)
    filter_horizontal = ('genre',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'score', 'pub_date', 'title')
    search_fields = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'review')
    search_fields = ('text',)


admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
