from django.contrib import messages
from django.db import connection
from django.shortcuts import render,redirect
from libraryapp.models import User

# Create your views here.
def home(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['username'],
                               password=request.POST['password']
                               ).exists():
            return render(request,'index.html')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')

cursor = connection.cursor()
def addborrowers(request):
        ssnexist = False
        message = ""
        if (request.method == "POST"):
            fname = request.POST['fname']
            ssn = request.POST['ssn']
            phone = request.POST['phone']

            query = "SELECT Ssn FROM Borrower WHERE Ssn = '" + ssn + "'"
            cursor.execute(query)

            if (cursor.fetchone() != None):
                ssnexist = True
                messages.error(request, "You have already registered.")
            else:
                query = 'INSERT INTO Borrower(Ssn,Bname,Phone) VALUES("' + ssn + '","' + fname + '","' + phone + '");'
                cursor.execute(query)
                messages.success(request, "Borrower Registered Successfully!")
            return redirect('addborrowers')
        else:
            return render(request, 'addborrowers.html', {'ssnexist': ssnexist, 'message': message})

def booksearch(request):
        books = ""
        message = ""
        get = True
        if (request.method == "POST"):
            if ('search' in request.POST):
                get = False
                keywords = request.POST['search'].split(',')
                comparision = ""
                for keyword in keywords:
                    keyword = keyword.strip()
                    keyword = "%" + keyword + "%"
                    if (comparision != ""):
                        comparision += " AND "
                    comparision += "(BkAthr.Isbn LIKE '" + keyword + "' OR BkAthr.Title LIKE '" + keyword + "' OR BkAthr.authors LIKE '" + keyword + "')"

                query = "SELECT BkAthr.Isbn, BkAthr.Title, BkAthr.authors, BkAthr.Availability FROM (SELECT Book.Isbn, Book.Title, GROUP_CONCAT(Authors.Name) authors, Book.Availability FROM Book,Book_Authors,Authors WHERE Book.Isbn = Book_Authors.Isbn AND Book_Authors.Author_id = Authors.Author_id GROUP BY Book.Isbn) AS BkAthr WHERE " + comparision
                cursor.execute(query)
                books = cursor.fetchall()
                return render(request, 'booksearch.html', {'books': books, 'message': "", 'get': get})

            elif ('cardno' in request.POST):
                keywords = request.POST['cardno'].split(',')
                print(keywords)
                cardno = keywords[0]
                isbn = keywords[1]
                print(cardno, isbn)
                query = "SELECT COUNT(Card_id) FROM Borrower WHERE Card_id = '" + cardno + "' GROUP BY Card_id"
                cursor.execute(query)

                if (cursor.fetchone() != None):
                    query = "SELECT COUNT(Loan_id) FROM Book_Loans WHERE Book_Loans.Card_id = '" + str(
                        cardno) + "' AND Book_Loans.Date_in IS NULL GROUP BY Book_Loans.Card_id"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if (result == None):
                        query = "SELECT Book.Availability FROM Book WHERE Book.Isbn = '" + isbn + "'"
                        cursor.execute(query)
                        availability = cursor.fetchone()
                        if (availability[0] == 1):
                            query = 'INSERT INTO Book_Loans(Isbn, Card_id, Date_out, Due_date, Date_in) VALUES("' + isbn + '","' + str(
                                cardno) + '",CURDATE(),DATE_ADD(Date_out,INTERVAL 14 DAY),NULL)'
                            cursor.execute(query)
                            query = 'UPDATE Book SET Book.Availability = "0" WHERE Book.isbn = "' + isbn + '"'
                            cursor.execute(query)
                            message = "Successfully checked out book. Return within 14 days to avoid fine"
                        else:
                            message = "Book is not available"
                    else:
                        query = "SELECT Book.Availability FROM Book WHERE Book.Isbn = '" + isbn + "'"
                        cursor.execute(query)
                        if (result[0] < 3):
                            query = 'INSERT INTO Book_Loans(Isbn, Card_id, Date_out, Due_date, Date_in) VALUES("' + isbn + '","' + str(
                                cardno) + '",CURDATE(),DATE_ADD(Date_out,INTERVAL 14 DAY),NULL)'
                            cursor.execute(query)
                            query = 'UPDATE Book SET Book.Availability = "0" WHERE Book.isbn = "' + isbn + '"'
                            cursor.execute(query)
                            message = "Successfully checked out book. Return within 14 days to avoid fine"
                        else:
                            message = "Maximum of only 3 books can be checked out"
                else:
                    message = "Invalid Card Number."

                return render(request, 'booksearch.html', {'books': books, 'message': message, 'get': get})

            else:
                print(request.POST)
                return render(request, 'booksearch.html', {'books': books, 'message': message, 'get': get})

        else:
            return render(request, 'booksearch.html', {'books': books, 'message': message, 'get': get})


def payfine(request):
        fines = ""
        message = ""
        get = True
        if (request.method == 'POST'):
            if ('searchfines' in request.POST):
                get = False
                keywords = request.POST['searchfines'].split(',')
                comparision = ""
                for keyword in keywords:
                    keyword = keyword.strip()
                    keyword = "%" + keyword + "%"
                    if (comparision != ""):
                        comparision += " AND "
                    comparision += "(BrrFine.Card_id LIKE '" + keyword + "' OR BrrFine.Ssn LIKE '" + keyword + "' OR BrrFine.Bname LIKE '" + keyword + "')"

                query = "SELECT BrrFine.Card_id, BrrFine.Ssn, BrrFine.Bname, BrrFine.Totalfine, BrrFine.Loan_id FROM (SELECT Borrower.Card_id, Borrower.Ssn, Borrower.Bname, SUM(Fines.Fine_amt) Totalfine, Book_Loans.Loan_id FROM Borrower,Book_Loans,Fines WHERE Borrower.Card_id = Book_Loans.Card_id AND Book_Loans.Loan_id = Fines.Loan_id AND Fines.Paid = '0' AND Book_Loans.Date_in IS NOT NULL GROUP BY Borrower.Card_id) AS BrrFine WHERE " + comparision
                cursor.execute(query)
                print(query)
                fines = cursor.fetchall()
                return render(request, 'payfine.html', {'fines': fines, 'message': message, 'get': get})

            elif ('refreshfines' in request.POST):
                query = "SELECT Loan_id, DATEDIFF(CURDATE(),Due_date)*0.25 difference FROM Book_Loans WHERE DATEDIFF(CURDATE(),Due_date)*0.25 > '0'"
                cursor.execute(query)
                results = cursor.fetchall()
                for result in results:
                    query = "SELECT Loan_id FROM Fines WHERE Loan_id = '" + str(result[0]) + "'"
                    cursor.execute(query)
                    if (cursor.fetchone() == None):
                        query = "INSERT INTO Fines(Loan_id,Fine_amt,Paid) VALUES('" + str(result[0]) + "', '" + str(
                            result[1]) + "', '0')"
                        cursor.execute(query)
                    else:
                        query = "UPDATE Fines SET Fines.Fine_amt = '" + str(
                            result[1]) + "' WHERE Fines.Loan_id = '" + str(result[0]) + "' AND Fines.Paid = '0'"
                        cursor.execute(query)

                message = "Successfully Refreshed Fines"
                return render(request, 'payfine.html', {'fines': fines, 'message': message, 'get': get})

            elif ('cardnumber' in request.POST):
                cardnumber = request.POST['cardnumber']
                query = "SELECT Loan_id FROM Book_Loans WHERE Date_in IS NOT NULL AND Card_id = '" + str(
                    cardnumber) + "'"
                cursor.execute(query)
                loanids = cursor.fetchall();
                for loanid in loanids:
                    query = "UPDATE Fines SET Fines.Paid = '1' WHERE Fines.Loan_id = '" + str(
                        loanid[0]) + "' AND Fines.Paid = '0'"
                    cursor.execute(query)
                message = "Payment Successful."
                return render(request, 'payfine.html', {'fines': fines, 'message': message, 'get': get})

            else:
                message = "Something went wrong please try again."
                return render(request, 'payfine.html', {'fines': fines, 'message': message, 'get': get})
        else:
            return render(request, 'payfine.html', {'fines': fines, 'message': message, 'get': get})

cursor = connection.cursor()
def checkinbooks(request):
        books = ""
        message = ""
        get = True
        if (request.method == "POST"):
            if ('checkin' in request.POST):
                get = False
                keywords = request.POST['checkin'].split(',')
                comparision = ""
                for keyword in keywords:
                    keyword = keyword.strip()
                    keyword = "%" + keyword + "%"
                    if (comparision != ""):
                        comparision += " AND "
                    comparision += "(BkAthr.Isbn LIKE '" + keyword + "' OR BkAthr.Title LIKE '" + keyword + "' OR BkAthr.authors LIKE '" + keyword + "' OR BkAthr.Card_id LIKE '" + keyword + "' OR BkAthr.Bname LIKE '" + keyword + "' OR BkAthr.Ssn LIKE '" + keyword + "')"

                query = "SELECT BkAthr.Isbn, BkAthr.Title, BkAthr.authors, BkAthr.Card_id, BkAthr.Bname, BkAthr.Ssn, BkAthr.Loan_id FROM (SELECT Book.Isbn, Book.Title, GROUP_CONCAT(Authors.Name) authors, Borrower.Card_id, Borrower.Bname, Borrower.Ssn, Book_Loans.Loan_id FROM Book,Book_Authors,Authors,Borrower,Book_Loans WHERE Book.Isbn = Book_Authors.Isbn AND Book_Authors.Author_id = Authors.Author_id AND Book.Isbn = Book_Loans.Isbn AND Borrower.Card_id = Book_Loans.Card_id AND Book_Loans.Date_in IS NULL GROUP BY Book.Isbn) AS BkAthr WHERE " + comparision
                cursor.execute(query)
                books = cursor.fetchall()
                return render(request, 'checkinbooks.html', {'books': books, 'message': message, 'get': get})
            elif ('loanid' in request.POST):
                get = False
                loan_id = request.POST['loanid']
                isbn = request.POST['isbnrtbk']
                query = "UPDATE Book_Loans SET Date_in = CURDATE() WHERE Loan_id = '" + loan_id + "'"
                cursor.execute(query)

                query = "SELECT DATEDIFF(Date_in,Due_date) FROM Book_Loans WHERE Book_Loans.Loan_id = '" + loan_id + "'"
                cursor.execute(query)
                days = cursor.fetchone()[0]

                if (days > 0):
                    fine_amt = days * 0.25;
                    message = "Your fine of amount " + str(fine_amt) + " is due "
                    query = "SELECT Paid FROM Fines WHERE Loan_id = '" + loan_id + "' GROUP BY Loan_id"
                    cursor.execute(query)
                    fineExist = cursor.fetchone()
                    print(fineExist)
                    if (fineExist == None):
                        query = "INSERT INTO Fines(Loan_id,Fine_amt,Paid) VALUES('" + loan_id + "','" + str(
                            fine_amt) + "','0')"
                        cursor.execute(query)
                    else:
                        if (fineExist[0] == 0):
                            query = "UPDATE Fines SET Fine_amt = '" + str(
                                fine_amt) + "' WHERE Loan_id = '" + loan_id + "'"
                            cursor.execute(query)

                query = "UPDATE Book SET Availability = '1' WHERE Isbn = '" + isbn + "'"
                cursor.execute(query)
                message += "successfully checked in book."
                return render(request, 'checkinbooks.html', {'Books': books, 'message': message, 'get': get})
            else:
                message = "Please try again."
                return render(request, 'checkinbooks.html', {'Books': books, 'message': message, 'get': get})
        else:
            return render(request, 'checkinbooks.html', {'Books': books, 'message': message, 'get': get})



def register(request):
    if request.method == 'POST':
        member = User(
            username = request.POST['username'],
            email = request.POST['email'],
            password = request.POST['password']
        )
        member.save()
        return redirect('login')
    else:
        return render(request,'register.html')


def login(request):
    return render(request,'login.html')


