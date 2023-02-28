from asyncio import streams
from dataclasses import fields
from email import message
from turtle import title
from unicodedata import name
from unittest import result
from urllib import response
from xml.parsers.expat import model
from django.contrib import admin
from django.http import HttpResponse
from django.core import serializers

#from .import serializer
from .models import Author
from .models import Book
from .models import BookInstance
from .models import Genre

# Register your models here.

#admin.site.register(Author)
#admin.site.register(Book)
#admin.site.register(BookInstance)
#admin.site.register(Genre)#




@admin.register (Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name', 'date_of_birth', 'date_of_death')    
    
    fields = [
        'first_name',
        'last_name',
        ('date_of_birth', 'date_of_death'),
    ]


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

    def display_genre(self, obj):  
        return ','.join([genre.name for genre in obj.genre.all()[:3]])

    display_genre.short_description = ('Genre')





#  json  ایجاد اکشن برای تبدیل خروجی به صورت   
def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type = "application/json")
    serializers.serialize("json", queryset, stream = response)
    return response


#ایجاد یک اکشن
def make_reserved(modeladmin, request, queryset):
    result = queryset.update(statuse = 'r')
    if result == 1:
        message_bit ="1 book was"
    else:
        message_bit ="{} book were".format(result) 

    modeladmin.message_user(request,"{} succesfuly marked as reserved.".format(message_bit))   

    
make_reserved.short_description = 'Mark selected books as reserved'
export_as_json.short_description = 'export selected books as json request'

@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display = ('book', 'statuse','borrower', 'due_back','id')
    list_filter = ( 'statuse', 'due_back')
    search_fields = ('due_back',)
    ordering = ('statuse',)

    fieldsets = (
        (None, {
            'fields':('book',
                     'imprint',
                     'id',
                     )
        }

        ),
        ('availablity',{
          'fields':('statuse', 
                    'due_back',
                    'borrower'
            )
            
        }
        )
    )
    actions = [ make_reserved , export_as_json ]
   
  