from django.contrib import admin
from .models import *

admin.site.register(Transaction)
admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(AccountType)
admin.site.register(Account)

