import uuid
from datetime import date
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
#تعریف کلاس ژانر
class Genre(models.Model):
    name = models.CharField(max_length=200 , help_text = 'enter a book genre(e.g sciense fiction , frenchpoetry etc.)')


    def __str__(self):
        return self.name


#تعریف کلاس کتاب
class Book(models.Model):
    title = models.CharField(max_length = 200,verbose_name='عنوان')
    #توضیحات کتاب
    summary = models.TextField(max_length =1000, help_text = 'enter a brif description of the book',verbose_name='توضیحات')
    isbn = models.CharField(max_length = 13, help_text = '13 character <a href="http://www.isbn-international.org/content/what-isbn">ISBN number</a>',verbose_name='isbn کد')
    #ارتباط چند به چند (هر کتاب میتواند چندژانر داشته باشدو هر ژانر میتواند برای چند کتاب باشد )
    genre = models.ManyToManyField(Genre, help_text = 'select a genrefor this book',verbose_name='ژانر')
    #ارتباط یک به چند (هر نویسنده میتواند چند کتاب داشته باشند)
    author = models.ForeignKey('Author', on_delete =models.SET_NULL , null = True,verbose_name='نویسنده')


    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
    
    def __str__(self):
        return self.title

    def get_absolute_url():
        return 


#تعریف کلاس نویسنده
class Author(models.Model):
    first_name = models.CharField(max_length =100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField(null = True, blank = True)
    date_of_death = models.DateField(null = True, blank = True)


    class Meta:
        ordering = ['last_name', 'first_name']


    def __str__(self):
        return '{0},{1}'.format(self.last_name,self.first_name)


#تعریف کلاس کپی های کتاب       
class BookInstance(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4,
                        help_text = 'unique ID for this paticular book across whole library')                
    #ارتباط یک به چند (یک کتاب میتواند چند کپی داشته باشد )
    book = models.ForeignKey('Book', on_delete = models.SET_NULL, null = True, blank = True)
    #جزییات نسخه ها
    imprint = models.CharField(max_length =200)
    #کتاب های پس داده شده
    due_back = models.DateField(null = True, blank = True)
    #کسانی  که کتاب قرض گرفته اند
    borrower = models.ForeignKey(User,on_delete = models.SET_NULL, null = True, blank = True)
    #حالت های قرض کتابها
    LOAN_STATUSE = (
        ('m','Maintenance'),   #قرض گرفته نگه دارد
        ('o','On loan'),       #قرض گرفته برمیگرداند
        ('a','Available'),     #موجود است
        ('r','Reserved')       #رزرو شده است
    )

    statuse = models.CharField(max_length = 1, choices = LOAN_STATUSE, blank = True, default = 'a',help_text = 'Book Availablity')


    class Meta:
        ordering = ['due_back']
        permissions = (
            ("can_read_private_section","VIP_User"),
            ("user_watcher","UserWatcher"),
            ("librarian","Librarian"),
        )

   
 #محاسبه تاریخ کتاب که تاریخ برگشت  گذشته است

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False    
    
    def __str__(self):
        return '{0},{1}'.format(self.id,self.book.title)
         