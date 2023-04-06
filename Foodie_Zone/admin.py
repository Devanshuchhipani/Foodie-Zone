from django.contrib import admin
from Foodie_Zone.models import *

# Register your models here.
admin.site.site_header = "Foodie Zone | Admin"

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','subject','added_on','is_approved']

class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id','name','logo','added_on','updated_on']

admin.site.register(Contact, ContactAdmin)
admin.site.register(Restaurant)
admin.site.register(Partner,PartnerAdmin)
admin.site.register(Items)
admin.site.register(Customer)
admin.site.register(Report)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CartItem_Item)
admin.site.register(Order)