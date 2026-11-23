
import random

from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.validators import RegexValidator
from django.db import transaction
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import (
    DemoWallet,
    WalletTransaction,
    Game,
    DemoGameEntry,
    Result,
    Notice,
)


# ==========================================
# WALLET CREATION
# ==========================================

def ensure_wallet(user):
    wallet, _ = DemoWallet.objects.get_or_create(
        user=user
    )
    return wallet


# ==========================================
# CREATE ACCOUNT FORM
# ==========================================

class RegistrationForm(forms.Form):

    full_name = forms.CharField(
        max_length=150
    )

    mobile = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^[6-9][0-9]{9}$",
                message=(
                    "Enter a valid 10-digit mobile number."
                ),
            )
        ],
    )

    mpin = forms.CharField(
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput
    )

    confirm_mpin = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]

        User = get_user_model()

        if User.objects.filter(
            username=mobile
        ).exists():
            raise forms.ValidationError(
                "This mobile number is already registered."
            )

        return mobile

    def clean(self):
        cleaned_data = super().clean()

        mpin = cleaned_data.get("mpin")
        confirm_mpin = cleaned_data.get(
            "confirm_mpin"
        )

        if mpin and confirm_mpin:
            if mpin != confirm_mpin:
                self.add_error(
                    "confirm_mpin",
                    "MPIN and Confirm MPIN do not match."
                )

        return cleaned_data


# ==========================================
# CREATE ACCOUNT VIEW
# ==========================================

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = RegistrationForm(
        request.POST or None
    )

    if (
        request.method == "POST"
        and form.is_valid()
    ):

        with transaction.atomic():

            User = get_user_model()

            user = User.objects.create_user(
                username=form.cleaned_data[
                    "mobile"
                ],
                password=form.cleaned_data[
                    "mpin"
                ],
                first_name=form.cleaned_data[
                    "full_name"
                ],
            )

            ensure_wallet(user)

        login(request, user)

        messages.success(
            request,
            "Your account has been created successfully."
        )

        return redirect("home")

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )


# ==========================================
# HOME PAGE
# ==========================================

@login_required
def home(request):

    wallet = ensure_wallet(
        request.user
    )

    games = Game.objects.order_by(
        "sort_order"
    )[:6]

    results = Result.objects.order_by(
        "-result_date"
    )[:8]

    return render(
        request,
        "hub/home.html",
        {
            "wallet": wallet,
            "games": games,
            "results": results,
        }
    )


# ==========================================
# PLAY PAGE
# ==========================================

@login_required
def play(request):

    games = Game.objects.order_by(
        "sort_order"
    )

    return render(
        request,
        "hub/play.html",
        {
            "games": games
        }
    )


# ==========================================
# DEMO WALLET
# ==========================================

@login_required
def wallet(request):

    user_wallet = ensure_wallet(
        request.user
    )

    if request.method == "POST":

        try:
            amount = int(
                request.POST.get(
                    "amount",
                    "0"
                )
            )
        except (ValueError, TypeError):
            amount = 0

        if amount < 1 or amount > 50000:

            messages.error(
                request,
                "Enter a demo amount between 1 and 50,000."
            )

        else:

            with transaction.atomic():

                user_wallet = (
                    DemoWallet.objects
                    .select_for_update()
                    .get(pk=user_wallet.pk)
                )

                user_wallet.points += amount

                user_wallet.save(
                    update_fields=["points"]
                )

                WalletTransaction.objects.create(
                    wallet=user_wallet,
                    kind="Demo points added",
                    points=amount,
                    note=(
                        "Simulated; no payment taken"
                    ),
                )

            messages.success(
                request,
                f"Added {amount} demo points."
            )

        return redirect("wallet")

    transactions = (
        user_wallet.transactions
        .order_by("-created_at")[:50]
    )

    return render(
        request,
        "hub/wallet.html",
        {
            "wallet": user_wallet,
            "transactions": transactions,
        }
    )


# ==========================================
# GAME HISTORY
# ==========================================

@login_required
def history(request):

    entries = (
        DemoGameEntry.objects
        .filter(user=request.user)
        .order_by("-created_at")[:100]
    )

    return render(
        request,
        "hub/history.html",
        {
            "entries": entries
        }
    )


# ==========================================
# RESULTS PAGE
# ==========================================

@login_required
def results(request):

    all_results = (
        Result.objects
        .order_by("-result_date")[:150]
    )

    return render(
        request,
        "hub/results.html",
        {
            "results": all_results
        }
    )


# ==========================================
# NOTIFICATIONS
# ==========================================

@login_required
def notifications(request):

    notices = (
        Notice.objects
        .filter(is_active=True)
        .order_by("-created_at")
    )

    return render(
        request,
        "hub/notifications.html",
        {
            "notices": notices
        }
    )


# ==========================================
# APP DETAILS
# ==========================================

@login_required
def app_details(request):

    return render(
        request,
        "hub/simple.html",
        {
            "heading": "App Details",
            "body": (
                "Demo Play Hub — local prototype."
            ),
        }
    )


# ==========================================
# TERMS AND CONDITIONS
# ==========================================

@login_required
def terms(request):

    return render(
        request,
        "hub/simple.html",
        {
            "heading": "Terms and Conditions",
            "body": (
                "Demo points have no cash value. "
                "All game actions and outcomes "
                "are simulated. No payments or "
                "payouts are supported."
            ),
        }
    )


# ==========================================
# HELP PAGE
# ==========================================

@login_required
def help_page(request):

    return render(
        request,
        "hub/simple.html",
        {
            "heading": "Help",
            "body": (
                "Use the navigation to explore "
                "this local demo prototype."
            ),
        }
    )


# ==========================================
# DEMO GAME
# ==========================================

@login_required
def demo_game(request, game_id):

    game = get_object_or_404(
        Game,
        pk=game_id
    )

    if request.method == "POST":

        selection = request.POST.get(
            "selection",
            "Demo"
        )

        outcome = random.choice([
            "Sample A",
            "Sample B",
            "Sample C",
        ])

        DemoGameEntry.objects.create(
            user=request.user,
            game=game,
            selection=selection,
            demo_points=0,
            outcome=outcome,
        )

        messages.info(
            request,
            "Demo action saved. No points were wagered."
        )

        return redirect("history")

    return render(
        request,
        "hub/demo_game.html",
        {
            "game": game
        }
    )

