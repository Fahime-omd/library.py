
from django.urls import path , re_path , register_converter
from .import views



#convert برای تاریخ آرشیو
class TwoDigitDayConverter:
    regex = '[0-9]{2}'
    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%02d' % value





register_converter(TwoDigitDayConverter,'dd')

app_name = 'book'
urlpatterns = [
    path('', views.index , name = 'index'),
    path('list/', views.BookListView.as_view() , name = 'bookList'),
    path('mybooks/', views.LoanedBookByUserListView.as_view() , name = 'mybooks'),
    path('detail/<uuid:pk>/renew/',views.renew_book_librarian, name = 'renewBooklibrarian'),
    path('borrows/',views.BookBorrowListView.as_view(), name = 'allBorrowed'),
    # path('detail/<int:pk>/', views.BookDetailView.as_view() , name = 'bookDetail')
    re_path(r'^detail/(?P<pk>\d+)/$', views.BookDetailView.as_view() , name = 'bookDetail'),
    path('archive/<dd:day>/', views.archive_day , name = 'archive'),

    # API URL
    re_path(r'^get/$', views.APIListCreateBook.as_view() , name = 'apiBookList'),
    re_path(r'^update/(?P<pk>\d+)/$', views.APIRetrieveUpdateDestroy.as_view() , name = 'apiBookUpdate'),
    re_path(r'^getdetail/(?P<pk>\d+)/$', views.BookDetail.as_view() , name = 'apiBookDetail'),
]