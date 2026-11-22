import random
from datetime import date
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import DemoWallet, WalletTransaction, Game, DemoGameEntry, Result, Notice

def ensure_wallet(user):
    wallet, _ = DemoWallet.objects.get_or_create(user=user)
    return wallet

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ensure_wallet(user)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def home(request):
    wallet = ensure_wallet(request.user)
    return render(request, "hub/home.html", {"wallet": wallet, "games": Game.objects.order_by("sort_order")[:6], "results": Result.objects.order_by("-result_date")[:8]})

@login_required
def play(request):
    return render(request, "hub/play.html", {"games": Game.objects.order_by("sort_order")})

@login_required
def wallet(request):
    wallet = ensure_wallet(request.user)
    if request.method == "POST":
        try: amount = int(request.POST.get("amount", "0"))
        except ValueError: amount = 0
        if amount < 1 or amount > 50000:
            messages.error(request, "Enter a demo amount between 1 and 50,000.")
        else:
            with transaction.atomic():
                wallet = DemoWallet.objects.select_for_update().get(pk=wallet.pk)
                wallet.points += amount
                wallet.save(update_fields=["points"])
                WalletTransaction.objects.create(wallet=wallet, kind="Demo points added", points=amount, note="Simulated; no payment taken")
            messages.success(request, f"Added {amount} demo points.")
        return redirect("wallet")
    return render(request, "hub/wallet.html", {"wallet": wallet, "transactions": wallet.transactions.order_by("-created_at")[:50]})

@login_required
def history(request):
    return render(request, "hub/history.html", {"entries": DemoGameEntry.objects.filter(user=request.user).order_by("-created_at")[:100]})

@login_required
def results(request):
    return render(request, "hub/results.html", {"results": Result.objects.order_by("-result_date")[:150]})

@login_required
def notifications(request):
    return render(request, "hub/notifications.html", {"notices": Notice.objects.filter(is_active=True).order_by("-created_at")})

@login_required
def app_details(request): return render(request, "hub/simple.html", {"heading":"App Details", "body":"Demo Play Hub — local prototype."})
@login_required
def terms(request): return render(request, "hub/simple.html", {"heading":"Terms and Conditions", "body":"Demo points have no cash value. All game actions and outcomes are simulated. No payments or payouts are supported."})
@login_required
def help_page(request): return render(request, "hub/simple.html", {"heading":"Help", "body":"Use the navigation to explore this local demo prototype."})

@login_required
def demo_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == "POST":
        selection = request.POST.get("selection", "Demo")
        DemoGameEntry.objects.create(user=request.user, game=game, selection=selection, demo_points=0, outcome=random.choice(["Sample A","Sample B","Sample C"]))
        messages.info(request, "Demo action saved. No points were wagered.")
        return redirect("history")
    return render(request, "hub/demo_game.html", {"game": game})
