from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(db_column='Username', max_length=100)
    email = models.EmailField(db_column='email', max_length=100)
    password = models.CharField(db_column='password', max_length=50)

    def __str__(self):
        return self.username

class Authors(models.Model):
    author_id = models.OneToOneField('BookAuthors', models.DO_NOTHING, db_column='Author', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'authors'


class Book(models.Model):
    isbn = models.CharField(db_column='Isbn', primary_key=True, max_length=10)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    availability = models.IntegerField(db_column='Availability')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book'


class BookAuthors(models.Model):
    author = models.AutoField(db_column='Author', primary_key=True)  # Field name made lowercase.
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='Isbn', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book_authors'



class Borrower(models.Model):
    card_id = models.AutoField(db_column='Card_id', primary_key=True)  # Field name made lowercase.
    ssn = models.CharField(db_column='Ssn', unique=True, max_length=50, null=True)  # Field name made lowercase.
    bname = models.CharField(db_column='Bname', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'borrower'

class BookLoans(models.Model):
    loan_id = models.AutoField(db_column='Loan_id', primary_key=True)  # Field name made lowercase.
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='Isbn', blank=True, null=True)  # Field name made lowercase.
    card = models.ForeignKey('Borrower', models.DO_NOTHING, db_column='Card_id', blank=True, null=True)  # Field name made lowercase.
    date_out = models.DateField(db_column='Date_out', blank=True, null=True)  # Field name made lowercase.
    due_date = models.DateField(db_column='Due_date', blank=True, null=True)  # Field name made lowercase.
    date_in = models.DateField(db_column='Date_in', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book_loans'

class Fines(models.Model):
    loan = models.OneToOneField(BookLoans, models.DO_NOTHING, db_column='Loan_id', primary_key=True)  # Field name made lowercase.
    fine_amt = models.FloatField(db_column='Fine_amt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fines'