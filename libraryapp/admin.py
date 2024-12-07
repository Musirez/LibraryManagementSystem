
from django.contrib import admin
from libraryapp.models import User, Book, Authors, BookAuthors, Borrower, BookLoans, Fines

# Register your models here.

admin.site.register(User)
admin.site.register(Authors)
admin.site.register(Book)
admin.site.register(BookAuthors)
admin.site.register(Borrower)
admin.site.register(BookLoans)
admin.site.register(Fines)

