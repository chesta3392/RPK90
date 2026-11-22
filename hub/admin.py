from django.contrib import admin
from .models import DemoWallet, WalletTransaction, Game, DemoGameEntry, Result, Notice
admin.site.register([DemoWallet, WalletTransaction, Game, DemoGameEntry, Result, Notice])
