from turtle import title
from django.test import TestCase
from django.urls import reverse
from .models import Book
from .models import Author


# Create your tests here.

class BlogTest(TestCase):
    def setUp(self):
        
        self.author = Author.objects.create(
            first_name = "ali",
            last_name ="pardel"
        )
        self.book = Book.objects.create(
            title = "book title",
            summary ="description",
            isbn ="9874356705643",
            author = self.author
        )

    def test_string_model(self):
        book = Book(title = "hello")
        self.assertEquals(str(book),book.title)  



    def test_book_model(self):
        self.assertEqual(f'{self.book.title}',"book title")
        self.assertEqual(f'{self.book.summary}',"description")
        self.assertEqual(f'{self.book.isbn}',"9874356705643")
        self.assertEqual(f'{self.book.author}',"pardel,ali")

    
    def test_book_list(self):
        response = self.client.get(reverse('book_List'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"book/book_list.html")
