
'''from django.contrib import admin
from bookdetails.models import bookdetails

class BookDetailsAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_title', 'book_name', 'book_desc', 'book_price', 'book_category')  

admin.site.register(bookdetails, BookDetailsAdmin)
class BookDetailsAdmin(admin.ModelAdmin):
    list_display = ('cat_id','cat_name')'''

    
from django.contrib import admin
from .models import Bookdetails, Category,Book,Purchase,Wishlist,ContactInformation,Contactform

class BookDetailsAdmin(admin.ModelAdmin):
    exclude = ('book_id',)  # Exclude the book_id field
    list_display = ('book_title', 'book_name', 'book_desc', 'book_price', 'book_category')  # Fields to display in the admin list



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_id', 'cat_name')
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','barcode')  
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('email','phone','address')      
class PurchaseAdmin(admin.ModelAdmin):
    list_display =('user','book','purchase_date')
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book','user','rating','comment','created_at')  
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user','book','added_on') 
class ContactformAdmin(admin.ModelAdmin):
    list_display = ('email', 'mobile_number', 'name','subject','message') 
admin.site.register(Bookdetails, BookDetailsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(ContactInformation, ContactInformationAdmin)
admin.site.register(Contactform, ContactformAdmin)

