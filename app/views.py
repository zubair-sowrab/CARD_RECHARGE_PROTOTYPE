from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserSignupForm,CardRequestForm,CardRechargeForm
from django.contrib.auth.decorators import login_required
from .models import CardHolder, MetroCard
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from app.models import CardHolder, MetroCard



def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if the user is logged in
    return render(request, 'app/landingpage.html')  # Show landing page if not logged in


# app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserSignupForm
from .models import CardHolder, MetroCard

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            # Check if the username already exists
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', 'A user with that username already exists.')
                return render(request,'app/signup.html', {'form': form})

            # Create a new user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )

            # Check if a CardHolder already exists for the user before creating one
            if not CardHolder.objects.filter(user=user).exists():
                # Create a new CardHolder linked to the user
                CardHolder.objects.create(
                    user=user,
                    phone_number=form.cleaned_data['phone_number'],
                    age=form.cleaned_data['age'],
                    national_id_number=form.cleaned_data['national_id_number']
                )

            # Log the user in and redirect to home
            login(request, user)
            return redirect('login')
    else:
        form = UserSignupForm()

    return render(request, 'app/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print(f"Attempting to authenticate user: {username}")

            user = authenticate(username=username, password=password)

            if user is not None:
                print(f"Authentication successful for user: {username}")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                print(f"Authentication failed for user: {username}")
                messages.error(request, "Invalid username or password.")
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'app/home.html')  # Create a new template 'home.html'


# app/views.py

# app/views.py

@login_required
def check_balance(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        try:
            # Fetch the CardHolder for the logged-in user
            card_holder = CardHolder.objects.get(user=request.user)
        except CardHolder.DoesNotExist:
            return render(request, 'app/check_balance.html', {'error': 'Card holder not found for the user.'})

        try:
            # Fetch the MetroCard associated with this CardHolder
            card = MetroCard.objects.get(card_number=card_number, holder=card_holder)
            return render(request, 'app/check_balance.html', {'card': card})
        except MetroCard.DoesNotExist:
            # This exception specifically means the card number does not match the holder
            return render(request, 'app/check_balance.html', {'error': 'Card not found for this holder.'})

    return render(request, 'app/check_balance.html')



# app/views.py

@login_required
def card_details(request):
    # Get or create CardHolder for the current user
    card_holder, created = CardHolder.objects.get_or_create(user=request.user)

    # Retrieve MetroCard instances associated with the card_holder
    cards = MetroCard.objects.filter(holder=card_holder)

    return render(request, 'app/card_details.html', {'cards': cards, 'card_holder': card_holder})


# views.py

@login_required
def request_new_card(request):
    if request.method == 'POST':
        form = CardRequestForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)  # Save the form without committing to the database
            # Correctly assign the holder using the CardHolder instance linked to the logged-in user
            card.holder = CardHolder.objects.get(user=request.user)
            card.save()  # Save the card with the correct holder
            return redirect('card_details')
    else:
        form = CardRequestForm()

    return render(request, 'app/request_new_card.html', {'form': form})


@login_required
def recharge_card(request):
    if request.method == 'POST':
        form = CardRechargeForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            amount = form.cleaned_data['amount']
            try:
                card = MetroCard.objects.get(card_number=card_number, holder__user=request.user)

                # SSLCommerz Payment Integration
                store_id = 'your_store_id'
                store_pass = 'your_store_pass'

                post_data = {
                    'store_id': store_id,
                    'store_passwd': store_pass,
                    'total_amount': str(amount),
                    'currency': 'BDT',
                    'tran_id': 'unique_transaction_id',  # Generate a unique transaction ID for each transaction
                    'success_url': request.build_absolute_uri('recharge_success'),
                    'fail_url': request.build_absolute_uri('recharge_fail'),
                    'cancel_url': request.build_absolute_uri('recharge_cancel'),
                    'cus_name': request.user.username,
                    'cus_email': request.user.email,
                    'cus_add1': 'Customer Address',
                    'cus_city': 'Dhaka',
                    'cus_country': 'Bangladesh',
                    'cus_phone': request.user.cardholder.phone_number,
                }

                response = requests.post('https://sandbox.sslcommerz.com/gwprocess/v4/api.php', data=post_data)
                response_data = response.json()

                if response_data['status'] == 'SUCCESS':
                    return redirect(response_data['GatewayPageURL'])
                else:
                    return render(request, 'app/recharge_card.html', {'form': form, 'error': 'Failed to initiate payment.'})

            except MetroCard.DoesNotExist:
                return render(request, 'app/recharge_card.html', {'form': form, 'error': 'Card not found'})
    else:
        form = CardRechargeForm()
    return render(request, 'app/recharge_card.html', {'form': form})


@login_required
def recharge_success(request):
    if request.method == "POST":
        data = request.POST
        tran_id = data.get('tran_id')
        val_id = data.get('val_id')
        amount = data.get('amount')

        # Verify the payment using SSLCOMMERZ verification API
        store_id = 'your_store_id'
        store_pass = 'your_store_pass'
        verification_url = f'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php?val_id={val_id}&store_id={store_id}&store_passwd={store_pass}&v=1&format=json'
        response = requests.get(verification_url)
        response_data = response.json()

        if response_data['status'] == 'VALID':
            # Update the user's card balance
            card_number = response_data['tran_id']
            card = get_object_or_404(MetroCard, card_number=card_number, holder__user=request.user)
            card.balance += Decimal(response_data['amount'])
            card.save()

            return render(request, 'app/recharge_success.html')
        else:
            return redirect('recharge_fail')

    return redirect('recharge_fail')

@login_required
def recharge_fail(request):
    return render(request, 'app/recharge_fail.html')

@login_required
def recharge_cancel(request):
    return render(request, 'app/recharge_cancel.html')
