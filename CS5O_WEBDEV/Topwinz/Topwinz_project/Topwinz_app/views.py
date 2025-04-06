from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserSignUpForm
from django.urls import reverse 
from .models import Raffle, RaffleEntry
from .utils import calculate_time_left




# Create your views here.
def index(request):
    # Fetch all raffle objects (baskets)
    raffles = Raffle.objects.all()

    # Loop through each basket to calculate tickets_percentage (optional)
    for raffle in raffles:
        raffle.tickets_percentage = (raffle.tickets_left / raffle.total_tickets) * 100 if raffle.total_tickets else 0

    # Pass the list of raffle baskets to the template
    return render(request, 'Topwinz/index.html', {'raffles': raffles})
    

@login_required(login_url='Topwinz_app:login')
def details(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(("login"))
    show_alert = request.session.pop("show_login_alert", False)
    return render(request, "Topwinz/user.html", {
        "show_alert": show_alert
    })
    
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not request.session.get("first_login_shown", False):
                request.session["show_login_alert"] = True
                request.session["first_login_shown"] = True
            return redirect("Topwinz_app:details")
        else:
            messages.error(request, "Invalid credentials")
            return render(request, "Topwinz/login.html")
            # Fall through to re-render the login page with error message
    elif request.user.is_authenticated:
        return redirect("Topwinz_app:details")
    
    return render(request, "Topwinz/login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Logged Out")
    return redirect(reverse('Topwinz_app:login')
    )


def about(request):
    return render(request, "Topwinz/about.html")

def sign_up(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            # Log the user in automatically after sign up
            login(request, user)

            return redirect('Topwinz_app:index')  # Redirect to home or any other page

    else:
        form = UserSignUpForm()

    return render(request, 'Topwinz/signup.html', {'form': form})



def raffle_list(request):
    # Active raffles: those that are still selling tickets or in the countdown phase.
    active_raffles = Raffle.objects.filter(tickets_left__gt=0) | Raffle.objects.filter(tickets_left=0, ended=False)
    # Completed raffles: those where the winner has been revealed.
    completed_raffles = Raffle.objects.filter(ended=True)

    user_tickets = RaffleEntry.objects.filter(user=request.user, raffle__in=active_raffles)

    return render(request, 'Topwinz/raffle_list.html', {
        'active_raffles': active_raffles,
        'completed_raffles': completed_raffles,
        'user_tickets': user_tickets
    })



@login_required
def buy_ticket(request, raffle_id):
    raffle = get_object_or_404(Raffle, id=raffle_id)

    if raffle.tickets_left > 0:
        # Register user in raffle
        RaffleEntry.objects.create(user=request.user, raffle=raffle)
        raffle.tickets_left -= 1
        raffle.save()

        # Check if raffle is full and start the raffle
        if raffle.tickets_left == 0:
            raffle.starting_time()

        response_data = {
            "success": True,
            "message": "Ticket purchased successfully!",
            "raffle_status": {
                "started": raffle.started,
                "tickets_left": raffle.tickets_left,
                "total_tickets": raffle.total_tickets,
                "winner_name": raffle.winner.username if raffle.winner else None
            }
        }
        return JsonResponse(response_data)

    return JsonResponse({"success": False, "message": "Tickets are sold out!"}, status=400)

# API endpoint to fetch raffle countdown and status
@csrf_exempt
def get_raffle_status(request, raffle_id):
    try:
        raffle = Raffle.objects.get(id=raffle_id)
    except Raffle.DoesNotExist:
        return JsonResponse({'status': {'error': 'Raffle not found'}}, status=404)
    
    # If raffle is already complete, return the winner
    if raffle.ended:
        return JsonResponse({
            'status': {
                'raffle_name': raffle.name,
                'started': raffle.started,
                'ended': raffle.ended,
                'tickets_left': raffle.tickets_left,
                'total_tickets': raffle.total_tickets,
                'tickets_percentage': ((raffle.total_tickets - raffle.tickets_left) * 100 / raffle.total_tickets) 
                                    if raffle.total_tickets else 0,
                'winner_name': raffle.winner.username if raffle.winner else None,
                'countdown': 0
            }
        })
    
    # If raffle has started but not ended, check the countdown
    if raffle.started:
        time_left = calculate_time_left(raffle)
        
        # If countdown has finished, pick a winner, end the reffle
        if time_left <= 0 and not raffle.ended:
            raffle.pick_winner()
            raffle.ended = True
            raffle.refresh_from_db()  # Refresh to get updated values
            
            return JsonResponse({
                'status': {
                    'raffle_name': raffle.name,
                    'started': raffle.started,
                    'ended': raffle.ended,
                    'tickets_left': raffle.tickets_left,
                    'total_tickets': raffle.total_tickets,
                    'tickets_percentage': ((raffle.total_tickets - raffle.tickets_left) * 100 / raffle.total_tickets) 
                                        if raffle.total_tickets else 0,
                    'winner_name': raffle.winner.username if raffle.winner else None,
                    'countdown': 0
                }
            })
        
        # Countdown still running
        return JsonResponse({
            'status': {
                'raffle_name': raffle.name,
                'started': raffle.started,
                'ended': raffle.ended,
                'tickets_left': raffle.tickets_left,
                'total_tickets': raffle.total_tickets,
                'tickets_percentage': ((raffle.total_tickets - raffle.tickets_left) * 100 / raffle.total_tickets) 
                                    if raffle.total_tickets else 0,
                'winner_name': None,
                'countdown': time_left
            }
        })
    
    # Raffle not started yet
    return JsonResponse({
        'status': {
            'raffle_name': raffle.name,
            'started': raffle.started,
            'ended': raffle.ended,
            'tickets_left': raffle.tickets_left,
            'total_tickets': raffle.total_tickets,
            'tickets_percentage': ((raffle.total_tickets - raffle.tickets_left) * 100 / raffle.total_tickets) 
                                if raffle.total_tickets else 0,
            'winner_name': None,
            'countdown': 0
        }
    })
