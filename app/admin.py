# cards/admin.py

from django.contrib import admin
from .models import MetroCard, CardHolder

@admin.register(CardHolder)
class CardHolderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'age', 'national_id_number')
    search_fields = ('user__username', 'phone_number', 'national_id_number')

@admin.register(MetroCard)
class MetroCardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'balance', 'expiry_date', 'holder')
    search_fields = ('card_number', 'holder__user__username')
    list_filter = ('expiry_date', 'holder')
