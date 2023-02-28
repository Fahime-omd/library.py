from dataclasses import fields
from rest_framework import serializers
from .models import Book, BookInstance

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields =(
            'title',
            'summary',
            'isbn',
            'genre',
            'author',
         )

class BookDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
       model = BookInstance
       fields =(
           'due_back',
           'book',
           'imprint',
           'id',
          
           
     )


    



 