from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Bookdetails, Review, Wishlist, ContactInformation
import qrcode
from io import BytesIO
import base64

def index(request):
    results = Bookdetails.objects.all().prefetch_related('reviews')

    if request.method == 'POST':
        search = request.POST.get('search')
        if search:
            results = Bookdetails.objects.filter(
                Q(book_title__icontains=search) | 
                Q(book_name__icontains=search) | 
                Q(book_desc__icontains=search)
            ).prefetch_related('reviews')

    return render(request, "index.html", {'bookdata': results})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('index')  # Redirect to the index page
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error during registration. Please check the details.')

    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def buybook(request, book_id):
    book = get_object_or_404(Bookdetails, book_id=book_id)
    price = book.book_price  # Get the price for later use
    upi_id = "aashupandit69722@okaxis"  # Your UPI ID

    # Create the UPI URI for the payment
    upi_uri = f"upi://pay?pa={upi_id}&pn=Aashu%20Pandit&am={price}&cu=INR"

    # Generate the QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_uri)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Encode the image to base64
    qr_code_data = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'buybook.html', {'qr_code_data': qr_code_data, 'amount': price})

@login_required
def savereview(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('review')
        user_id = request.user.id

        if book_id and rating and comment:
            Review.objects.create(book_id=book_id, rating=rating, comment=comment, user_id=user_id)
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

def loadReviews(request, book_id):
    book = get_object_or_404(Bookdetails, book_id=book_id)
    reviews = Review.objects.filter(book=book).values('user__username', 'rating', 'comment', 'created_at')
    reviews_list = list(reviews)  # Convert the queryset to a list of dictionaries

    return JsonResponse({'reviews': reviews_list})

@login_required
def add_to_wishlist(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')  # Get the book_id from POST request
        if book_id:
            book = get_object_or_404(Bookdetails, book_id=book_id)

            # Try to get or create the wishlist entry
            wishlist, created = Wishlist.objects.get_or_create(user=request.user, book=book)
            action = 'added' if created else 'removed'
            
            if not created:  # If the item was already in the wishlist, remove it
                wishlist.delete()
                action = 'removed'

            wishlist_items = Wishlist.objects.filter(user=request.user)
            bookdetails = [{'id': item.book.book_id, 'title': item.book.book_title,
                            'desc': item.book.book_desc, 'price': item.book.book_price,
                            'picture': item.book.book_picture.url} for item in wishlist_items]    

            # Return the action performed (added/removed) as a JSON response
            return JsonResponse({'action': action, 'bookdetails': bookdetails})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user_id=request.user.id)
    total_books = wishlist_items.count()
    bookdetails = [item.book for item in wishlist_items] 

    return render(request, 'wishlist.html', {
        'bookdetails': bookdetails,
        'total_books': total_books
    })

@login_required
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Bookdetails, book_id=book_id)
    if request.method == 'POST':
        wishlist_item = get_object_or_404(Wishlist, user=request.user, book=book)
        wishlist_item.delete()  # Remove the item from the wishlist
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

def logout_view(request):
    logout(request)  # Log out the user
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')  # Redirect to the homepage after logging out  

# Contact Information Views
def contact_info_view(request):
    contact_info = {
        'email': 'kaushikaashu982@gmail.com',
        'phone': '9045686018',
        'address': 'Adarsh Nagar, Gulothi, Bulandshahr, India',
    }
    return render(request, 'contact_info.html', {'contact_info': contact_info})

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')
        

        ContactInformation.objects.create(name=name, email=email, mobile=mobile, message=message)

    return render(request, 'contact_us.html', {'contact_us': contact_us})
    return redirect('success.html')  

def success(request):
    return render(request, 'success.html', {'message': 'Your message has been sent successfully!'})
