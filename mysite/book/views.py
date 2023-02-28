

import datetime 
#from datetime import datetime
from msilib.schema import ListView
from multiprocessing import context



from django.shortcuts import get_object_or_404, render
from django.views import generic


from django.http import HttpResponseRedirect
from django.urls import reverse



 # as a function
from django.contrib.auth.decorators import login_required             #  برای محدودیت به روش دکوریتور
from django.contrib.auth.decorators import permission_required        # برای محدودیت به پرمیشن 
from django.contrib.auth.decorators import user_passes_test           # محدودیت سفارشی

from .serializer import BookSerializer
from .serializer import BookDetailSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view



#as a generic
from django.contrib.auth.mixins import LoginRequiredMixin             #  برای محدودیت به روش دکوریتور
from django.contrib.auth.mixins import PermissionRequiredMixin            # برای محدودیت به پرمیشن 
from django.contrib.auth.mixins import UserPassesTestMixin             # محدودیت سفارشی 

from .forms import RenewBookForm           


from .models import Author
from .models import Book
from .models import BookInstance
from .models import Genre
from .forms import RenewBookForm


# Create your views 



#@login_required                         #لاگین چک میشود
#@permission_required('book.can_read_private_section')    # پرمیشن چک میشود
#@permission_required('book.user_watcher')  
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(statuse__exact = 'a').count()
    num_author = Author.objects.all().count()
    context ={
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_author': num_author,

    
    }
     
    return render(request, 'book/index.html',context)

#کتاب های قرض گرفته شده

class BookBorrowListView(LoginRequiredMixin ,PermissionRequiredMixin ,generic.ListView):
    model = BookInstance
    paginate_by = 2
    permission_required = "book.librarian"
    template_name ="book/book_borrows.html"

    def get_queryset(self):
        return BookInstance.objects.filter(statuse__exact = 'o')


# لیست کتاب ها
class BookListView(LoginRequiredMixin,PermissionRequiredMixin , generic.ListView):   #لاگین چک میشود بعد پرمیشن
    model = Book
    paginate_by = 2
    permission_required = "book.can_read_private_section"
    permission_required = "book.user_watcher"


    



   #است django آنهاشامل title کتاب هایی که
    #
    #def get_queryset(self):
    #    return Book.objects.filter(title__icontains = 'django')

   
    #def get_context_data(self, **kwargs):
    #    context = super(BookListView, self).get_context_data(**kwargs) 
    #    context['my_book_list'] = Book.objects.all()
    #    return context


class BookDetailView(generic.DetailView):
    model = Book





class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'book/bookinstance_list_borrower_user.html.'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(statuse__exact = 'o').order_by('due_back')



#تمدید تاریخ

@login_required
@permission_required('book.librarian')
def renew_book_librarian(request,pk):
    book_inst = get_object_or_404(BookInstance, pk = pk) 

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('book:allBorrowed'))
    else:
        proposed_renewal_data = datetime.date.today() + datetime.timedelta(weeks = 3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_data})

    context = {
        'form': form,
        'book_inst': book_inst
        } 
        

    return render(request,
     'book/book_renew_librarian.html',
      context
      )


      
#تابع آرشیو روز بازگشت کتابها
def archive_day(request , day):
    day_archive_books = BookInstance.objects.filter(due_back__day = day)
    context={
        "day_archive_books" : day_archive_books,
    }
    return render(request, 'book/archive.html', context )




#API

class APIListCreateBook(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    #permission_classes = [IsAuthenticated]                #post,get
    permission_classes = [IsAuthenticatedOrReadOnly]     # only get

 
class APIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    #permission_classes = [IsAuthenticated]                #post,get
    permission_classes = [IsAuthenticatedOrReadOnly]     # only get

#@api_view(["GET"])
#def book_Detail(request,pk):
#    book = Book.objects.get(pk = pk)
#    book_serialize  = BookDetailSerializer(book)
#    return Response(book_serialize.data)

class BookDetail(generics.ListCreateAPIView):
    queryset =BookInstance.objects.all()
    serializer_class = BookDetailSerializer


    