# Generated by Django 3.1 on 2024-12-06 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.CharField(db_column='Isbn', max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, db_column='Title', max_length=255, null=True)),
                ('availability', models.IntegerField(db_column='Availability')),
            ],
            options={
                'db_table': 'book',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BookAuthors',
            fields=[
                ('author', models.AutoField(db_column='Author', primary_key=True, serialize=False)),
                ('isbn', models.ForeignKey(blank=True, db_column='Isbn', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='libraryapp.book')),
            ],
            options={
                'db_table': 'book_authors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BookLoans',
            fields=[
                ('loan_id', models.AutoField(db_column='Loan_id', primary_key=True, serialize=False)),
                ('date_out', models.DateField(blank=True, db_column='Date_out', null=True)),
                ('due_date', models.DateField(blank=True, db_column='Due_date', null=True)),
                ('date_in', models.DateField(blank=True, db_column='Date_in', null=True)),
            ],
            options={
                'db_table': 'book_loans',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('card_id', models.AutoField(db_column='Card_id', primary_key=True, serialize=False)),
                ('ssn', models.CharField(db_column='Ssn', max_length=9, unique=True)),
                ('bname', models.CharField(blank=True, db_column='Bname', max_length=255, null=True)),
                ('address', models.CharField(blank=True, db_column='Address', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=14, null=True)),
            ],
            options={
                'db_table': 'borrower',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('author_id', models.OneToOneField(db_column='Author', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='libraryapp.bookauthors')),
                ('name', models.CharField(db_column='Name', max_length=255)),
            ],
            options={
                'db_table': 'authors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Fines',
            fields=[
                ('loan', models.OneToOneField(db_column='Loan_id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='libraryapp.bookloans')),
                ('fine_amt', models.FloatField(db_column='Fine_amt')),
            ],
            options={
                'db_table': 'fines',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='bookloans',
            name='card',
            field=models.ForeignKey(blank=True, db_column='Card_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='libraryapp.borrower'),
        ),
        migrations.AddField(
            model_name='bookloans',
            name='isbn',
            field=models.ForeignKey(blank=True, db_column='Isbn', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='libraryapp.book'),
        ),
    ]
