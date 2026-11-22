from django.conf import settings
from django.db import models

class DemoWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    def __str__(self): return f"{self.user.username}: {self.points} demo points"

class WalletTransaction(models.Model):
    wallet = models.ForeignKey(DemoWallet, on_delete=models.CASCADE, related_name="transactions")
    kind = models.CharField(max_length=40, default="Demo adjustment")
    points = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=180, blank=True)
    def __str__(self): return f"{self.kind} - {self.points}"

class Game(models.Model):
    name = models.CharField(max_length=80)
    is_available = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name

class DemoGameEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    selection = models.CharField(max_length=30)
    demo_points = models.PositiveIntegerField(default=0)
    outcome = models.CharField(max_length=40, default="Sample")
    created_at = models.DateTimeField(auto_now_add=True)

class Result(models.Model):
    game_name = models.CharField(max_length=80)
    result_value = models.CharField(max_length=30)
    result_date = models.DateField()
    def __str__(self): return f"{self.game_name} {self.result_date}"

class Notice(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.title
