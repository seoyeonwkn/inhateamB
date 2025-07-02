from django.contrib import admin

# Register your models here.
from .models import Question, Bookmark

admin.site.register(Question)
admin.site.register(Bookmark)
