from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    error=False
    #print(request.POST)
    if len(request.POST['full_name'])<1:
        messages.error(request,"Please enter a first name!", extra_tags='name')
        error=True
    if len(request.POST['alias'])<1:
        messages.error(request,"Please enter a last name!", extra_tags='alias')
        error=True
    if len(request.POST['password'])<2:
        messages.error(request,"Please enter a better password!", extra_tags='password')
        error=True
    if request.POST['password'] != request.POST['confirm']:
        messages.error(request,"Passwords do not match" , extra_tags='confirm')
        error=True

    matching_users = User.objects.filter(email=request.POST['email'])
    if len(matching_users) > 0:
        messages.error(request, "Sorry, email already taken", extra_tags='email')
        error=True

    if error:
        return redirect('/')
    
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    user = User.objects.create(full_name=request.POST['full_name'], alias= request.POST['alias'], email=request.POST['email'], password = hashed)
    
    request.session['user_id'] = user.id
    print(user)
    print(request.session['user_id'])
    return redirect('/books')

def login(request):
    print(request.POST)
    matching_users = User.objects.filter(email=request.POST['log_email'])
    if len(matching_users) > 0:
        #email matched now check pw
        user = matching_users[0]
        if bcrypt.checkpw(request.POST['log_password'].encode() , user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/books')
        else:
            messages.error(request,"Invalid Credentials!")   
    else:
        messages.error(request,"Invalid Credentials!")  
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


def main(request):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        print(request.session['user_id'])
        context = {
            "users" : User.objects.filter(id = request.session['user_id']),
            "book" : Book.objects.all(),
            "reviews" : Review.objects.all().order_by("-id"),
        }
        return render(request,'main.html', context)

def new_book(request):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        context = {
            "all_authors" : Author.objects.all().values(),
        }
        return render(request,'newBook.html',context)

def add_book(request):
    if not 'user_id' in request.session:
        return redirect('/')        
    else:
        print (request.POST)
        print (request.POST.getlist('choose')[0])
        if len(request.POST['book_title']) and len(request.POST['review']) > 1:
            if(request.POST['new_author']):
                author = Author.objects.create(full_name=request.POST['new_author'])
                book = Book.objects.create(title=request.POST['book_title'], description=request.POST['review'], rating = request.POST['rating'])
                book.authors.add(author)
                return redirect('/new_book')
            else:
                book = Book.objects.create(title=request.POST['book_title'], description=request.POST['review'], rating = request.POST['rating'])
                for i in range(0,len(request.POST.getlist('choose')),1):      
                    author = Author.objects.get(id=request.POST.getlist('choose')[i])
                    book.authors.add(author)
                return redirect(f'/display_book/{book.id}')
        else:
            messages.error(request,'Book must have a title AND review!')
            return redirect('/new_book')

def display_book(request,id):
    user = User.objects.get(id = request.session['user_id'])
    if request.method == "GET" :
        book = Book.objects.get(id=id)
        context = {
            "user" : user,
            "this_book" : Book.objects.get(id=id),
            "authors" : book.authors.all(), 
            "reviews" : book.reviews.all(),
        }
        return render(request,'display.html', context)
    
    if request.method == "POST":
        book = Book.objects.get(id=id)
        review = Review.objects.create(review = request.POST['bookreview'] , rating = request.POST['rev_rating'] , creator = user.alias, creator_id = user.id)
        book.reviews.add(review)
        return redirect(f'/display_book/{id}')

# def display_home(request):

