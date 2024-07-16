from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from datetime import datetime
from django.urls import reverse
from django.conf import settings
from .forms import CheckInForm
import razorpay
from BookMyFlight.utils import createticket, render_to_pdf
from .constant import FEE
import logging
from django.contrib.auth import authenticate, login, logout
import math
from .models import *


logger = logging.getLogger(__name__)

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 
def index(request):
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month + 3 <= 12) else datetime.now().date().year + 1}-{(datetime.now().date().month + 3) if (datetime.now().date().month + 3 <= 12) else (datetime.now().date().month + 3 - 12)}-{datetime.now().date().day}"

    context = {
        'min_date': min_date, 
        'max_date': max_date
    }

    if request.method == 'POST':
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        depart_date = request.POST.get('DepartDate')
        seat = request.POST.get('SeatClass')
        trip_type = request.POST.get('TripType')

        if not all([origin, destination, depart_date, seat, trip_type]):
            context['error'] = "All fields are required."
            return render(request, 'flight/index.html', context)

        if trip_type == '1': 
            index_context = {
                'origin' : origin, 
                'destination': destination, 
                'depart_date' : depart_date, 
                'seat': seat.lower(), 
                'trip_type': trip_type
            }
            return render(request, 'flight/index.html', index_context)
        
        elif trip_type == '2': 
            return_date = request.POST.get('ReturnDate')
            if not return_date:
                context['error'] = "Return date is required for a round trip."
                return render(request, 'flight/index.html', context)
                
            context.update({
                'origin' : origin, 
                'destination': destination, 
                'depart_date' : depart_date, 
                'seat': seat.lower(), 
                'trip_type': trip_type, 
                'return_date': return_date
            })
            return render(request, 'flight/index.html', context)
    
    return render(request, 'flight/index.html', context)

def query(request, q):
    """
    The function `query` filters a list of Place objects based on a search query and returns a JSON
    response with specific attributes of the filtered results.
    
    :param request: The `request` parameter in the `query` function is typically used to represent the
    incoming HTTP request made to the server. It contains information such as the request method,
    headers, and data sent by the client. In the provided code snippet, the `request` parameter is not
    being used directly in
    :param q: The `q` parameter in the `query` function is used to search for a specific query string in
    the attributes of the `Place` objects. The function searches for the query string in the `city`,
    `airport`, `code`, and `country` attributes of each `Place` object and
    :return: The `query` function takes a request and a query string `q`, then searches for matching
    results in the `Place` model based on the city, airport, code, and country fields. It then returns a
    JSON response containing the code, city, and country of the filtered results.
    """
    places = Place.objects.all()
    filtered_results = []
    q = q.lower()

    for place in places: 
        if(q in place.city.lower()) or (q in place.airport.lower()) or (q in places.code.lower()) or (q in places.country.lower()): 
            filtered_results.append(place)

    return JsonResponse([{'code': place.code, 'city': place.city, 'country': place.country} for place in filtered_results], safe=False)
 


def register_view(request): 
    """
    The `register_view` function handles user registration by creating a new user account if the
    provided information is valid.
    
    :param request: The `request` parameter in the `register_view` function is an object that contains
    information about the current HTTP request. It includes details such as the request method (GET,
    POST, etc.), request headers, request data (POST parameters), user session information, and more. In
    this context, the
    :return: If the password matches, the code will return a successful registration message
    "Registration successful ✅💯" and redirect the user to the "index" page. If the username is already
    taken, it will return a message "Username already taken" and render the registration page again with
    the error message.
    """
    if request.method == "POST": 
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']

        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation: 
            context = {
                "message": "Password must match."
            }
            return render(request, "flight/register.html", context)

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
            print('Registration successful ✅💯')
        except: 
            context = {
                "message": "Username already taken."
            }
            return render(request, "flight/register.html", context)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flight/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Debug: Print received username and password
        print(f"Received username: {username}")
        print(f"Received password: {password}")

        # Check if user exists
        try:
            user_exists = User.objects.get(username=username)
            print(f"User exists: {user_exists.username}")
        except User.DoesNotExist:
            print("User does not exist.")
            return render(request, "flight/login.html", {
                "message": "Invalid username and/or password."
            })

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("Login successful")
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            print("Login failed due to invalid username or password")
            return render(request, "flight/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "flight/login.html")

        

def logout_view(request): 
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def flight(request): 
    """
    This Python function retrieves flight information based on user input parameters like origin,
    destination, trip type, seat class, and dates.
    
    :param request: The code you provided is a Django view function for handling flight search requests.
    It takes various parameters from the request such as origin, destination, trip type, departure date,
    return date, and seat class to search for available flights and their prices
    :return: The code is returning a context dictionary containing flight information such as flights,
    origin, destination, seat class, trip type, departure date, return date, and price ranges. This
    context is then rendered in the 'flight/search.html' template based on the conditions specified in
    the code.
    """
    origin_place = request.GET.get('Origin')
    destination_place = request.GET.get('Destination')
    trip_type = request.GET.get('TripType')
    departure_date = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departure_date, "%Y-%m-%d")
    return_date = None

    if trip_type == '2': 
        returndate = request.GET.get('ReturnDate')
        return_date = datetime.strptime(returndate, "%Y-%m-%d")
        flightday2 = Week.objects.get(week_id=return_date.weekday())
        origin2 = Place.objects.get(code=destination_place.upper())
        destination2 = Place.objects.get(code=origin_place.upper())

    seat = request.GET.get('SeatClass')
    flightday = Week.objects.get(number=depart_date.weekday())
    destination = Place.objects.get(code=destination_place.upper())
    origin = Place.objects.get(code=origin_place.upper())

    if seat == 'economy': 
        flights = Flight.objects.filter(depart_day = flightday, origin=origin, destination=destination).exclude(economy_fare=0).order_by('economy_fare')
        print(flights.count())
        try: 
            min_price = flights.first().economy_fare
            max_price = flights.last().economy_fare
        except: 
            min_price = 0
            max_price = 0

        if trip_type == '2': 
            flights2 = Flight.objects.filter(depart_day = flightday2, origin=origin2, destination=destination2).exclude(economy_fare=0).order_by('economy_fare')
            try:
                max_price2 = flights2.last().economy_fare
                min_price2 = flights2.first().economy_fare 

            except:
                max_price2 = 0
                min_price2 = 0

        elif seat == 'business': 
            flights = Flight.objects.filter(depart_day = flightday, origin=origin, destination=destination).exclude(business_fare=0).order_by('business_fare')
            try: 
                min_price = flights.first().business_fare
                max_price = flights.last().business_fare

            except: 
                min_price = 0
                max_price = 0

            if trip_type == '2': 
                flights2 = Flight.objects.filter(depart_day = flightday2, origin=origin2, destination=destination2).exclude(business_fare=0).order_by('busniess_fare')
                try: 
                    min_price2 = flights2.first().business_fare
                    max_price = flights2.last().business_fare
                except: 
                    min_price2 = 0
                    max_price2 = 0

        elif seat == 'first': 
            flights = Flight.object.filter(depart_day = flightday, origin=origin, destination = destination).exclude(first_fare=0).order_by('first_fare')
            try: 
                min_price = flights.first().first_fare
                max_price = flights.last().first_fare
            except: 
                min_price = 0
                max_price = 0

            if trip_type == '2': 
                flights2 = Flight.objects.filter(depart_day = flightday2, origin=origin2, destination=destination2).exclude(first_fare=0).order_by('first_fare')
                try: 
                    min_price2 = flights2.first().first_fare
                    max_price2 = flights2.last().first_fare
                except: 
                    min_price2 = 0
                    max_price2 = 0

        if trip_type == '2': 
            context = {
                'flights': flights, 
                'origin': origin, 
                'destination': destination, 
                'flights2': flights2, 
                'origin2': origin2, 
                'destination2': destination2, 
                'seat': seat.capitalize(), 
                'trip_type': trip_type, 
                'depart_date': depart_date, 
                'return_date': return_date, 
                'max_price': math.ceil(max_price/100)*100,
                'min_price': math.floor(min_price/100)*100,
                'max_price2': math.ceil(max_price2/100)*100,    ##
                'min_price2': math.floor(min_price2/100)*100
            }

            return render(request, 'flight/search.html', context)
        
        else: 
            context = {
                'flights': flights, 
                'origin': origin, 
                'destination': destination, 
                'seat': seat.capitalize(), 
                'trip_type': trip_type, 
                'depart_date': depart_date, 
                'return_date': return_date,
                'max_price': math.ceil(max_price/100)*100,
                'min_price': math.floor(min_price/100)*100
            }

            return render(request, 'flight/search.html', context)
        

def review(request):
    """
    This Python function processes flight booking information, including details for one-way or
    round-trip flights, and renders a booking page for authenticated users.
    
    :param request: The code snippet you provided is a Python function that handles a flight booking
    review process based on the parameters received in the request. Here's a breakdown of the parameters
    used in the function:
    :return: The `review` function is returning a rendered template for booking a flight. If the user is
    authenticated, it will display flight details including departure and arrival dates, seat class, and
    fee. If it is a round trip, it will also include details for the second flight. If the user is not
    authenticated, it will redirect to the login page.
    """
    flight_1 = request.GET.get('flight1Id')
    date1 = request.GET.get('flight1Date')
    seat = request.GET.get('seatClass')
    round_trip = False
    if request.GET.get('flight2Id'):
        round_trip = True

    if round_trip:
        flight_2 = request.GET.get('flight2Id')
        date2 = request.GET.get('flight2Date')

    if request.user.is_authenticated:
        flight1 = Flight.objects.get(id=flight_1)
        flight1ddate = datetime(int(date1.split('-')[2]),int(date1.split('-')[1]),int(date1.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
        flight1adate = (flight1ddate + flight1.duration)
        flight2 = None
        flight2ddate = None
        flight2adate = None
        if round_trip:
            flight2 = Flight.objects.get(id=flight_2)
            flight2ddate = datetime(int(date2.split('-')[2]),int(date2.split('-')[1]),int(date2.split('-')[0]),flight2.depart_time.hour,flight2.depart_time.minute)
            flight2adate = (flight2ddate + flight2.duration)
        if round_trip:
            return render(request, "flight/book.html", {
                'flight1': flight1,
                'flight2': flight2,
                "flight1ddate": flight1ddate,
                "flight1adate": flight1adate,
                "flight2ddate": flight2ddate,
                "flight2adate": flight2adate,
                "seat": seat,
                "fee": FEE
            })
        return render(request, "flight/book.html", {
            'flight1': flight1,
            "flight1ddate": flight1ddate,
            "flight1adate": flight1adate,
            "seat": seat,
            "fee": FEE
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def book(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            print(type(user))
            flight_1 = request.POST.get('flight1')
            flight_1date = request.POST.get('flight1Date')
            flight_1class = request.POST.get('flight1Class')
            f2 = False
            if request.POST.get('flight2'):
                flight_2 = request.POST.get('flight2')
                flight_2date = request.POST.get('flight2Date')
                flight_2class = request.POST.get('flight2Class')
                f2 = True
            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            flight1 = Flight.objects.get(id=flight_1)
            if f2:
                flight2 = Flight.objects.get(id=flight_2)
            passengerscount = request.POST['passengersCount']
            passengers=[]
            for i in range(1,int(passengerscount)+1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                gender = request.POST[f'passenger{i}Gender']
                passengers.append(Passenger.objects.create(first_name=fname,last_name=lname,gender=gender.lower()))
            coupon = request.POST.get('coupon')
            
            try:
                ticket1 = createticket(request.user,passengers,passengerscount,flight1,flight_1date,flight_1class,coupon,countrycode,email,mobile)
                if f2:
                    ticket2 = createticket(request.user,passengers,passengerscount,flight2,flight_2date,flight_2class,coupon,countrycode,email,mobile)

                if(flight_1class == 'Economy'):
                    if f2:
                        fare = (flight1.economy_fare*int(passengerscount))+(flight2.economy_fare*int(passengerscount))
                    else:
                        fare = flight1.economy_fare*int(passengerscount)
                elif (flight_1class == 'Business'):
                    if f2:
                        fare = (flight1.business_fare*int(passengerscount))+(flight2.business_fare*int(passengerscount))
                    else:
                        fare = flight1.business_fare*int(passengerscount)
                elif (flight_1class == 'First'):
                    if f2:
                        fare = (flight1.first_fare*int(passengerscount))+(flight2.first_fare*int(passengerscount))
                    else:
                        fare = flight1.first_fare*int(passengerscount)
            except Exception as e:
                return HttpResponse(e)
            

            if f2:    ##
                return render(request, "flight/payment.html", { ##
                    'fare': fare+FEE,   ##
                    'ticket': ticket1.id,   ##
                    'ticket2': ticket2.id   ##
                })  ##
            return render(request, "flight/payment.html", {
                'fare': fare+FEE,
                'ticket': ticket1.id
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")


def payment(request):
    """
    The `payment` function processes a payment request, creates a Razorpay order, and renders a payment
    processing page with necessary details.
    
    :param request: The `payment` function is a view function in Django that handles payment processing.
    It checks if the user is authenticated, processes the payment details from a POST request, and then
    creates a Razorpay order for payment processing
    
    :return: The code snippet is a Django view function named `payment`. It handles a POST request for
    processing a payment. If the user is authenticated, it retrieves ticket information and creates a
    Razorpay order for payment processing. If the fare value is missing or invalid, it returns an error
    message. If the payment processing is successful, it renders a payment processing template with the
    necessary context data. If any exceptions occur
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            ticket_id = request.POST.get('ticket')
            t2 = False
            ticket2_id = None
            if request.POST.get('ticket2'):
                ticket2_id = request.POST.get('ticket2')
                t2 = True
            fare = request.POST.get('fare')
            print(fare)

            if not fare:
                return HttpResponse("Fare is required.")
            
            try:
                amount = int(float(fare) * 100)  # Convert fare to paisa
            except ValueError:
                return HttpResponse("Invalid fare value.")

            try:
                ticket = Ticket.objects.get(id=ticket_id)
                print("checkpoint passed")
                razorpay_order = razorpay_client.order.create({
                    "amount": amount,
                    "currency": "INR",
                    "payment_capture": "1"
                })

                if razorpay_order: 
                    print("Success")
                else: 
                    print("I think the credentials are incorrect")

                context = {
                    'ticket1': ticket,
                    'ticket2': ticket2_id if t2 else "",
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
                    'amount': amount,
                    'currency': 'INR',
                    'callback_url': reverse('paymenthandler')
                }
                return render(request, 'flight/payment_process.html', context)
            except Exception as e:
                print("Here it failed")
                return HttpResponse(str(e))
        else:
            return HttpResponse("Method must be POST.")
    else:
        return HttpResponseRedirect(reverse('login'))

def paymenthandler(request):
    """
    The `paymenthandler` function processes a payment request, verifies the payment signature, captures
    the payment amount, updates ticket status, and renders success or failure pages accordingly.
    
    :param request: The `request` parameter in the `paymenthandler` function is typically an HttpRequest
    object that represents the HTTP request made by a user. It contains information about the request,
    such as the method used (GET, POST, etc.), request headers, request data, and more
    :return: The `paymenthandler` function returns different responses based on the conditions met
    during the processing of a POST request. Here are the possible return scenarios:
    """
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result:
                try:
                    # Retrieve the fare amount from the hidden form field
                    amount = int(float(request.POST.get('amount')))

                    razorpay_client.payment.capture(payment_id, amount)

                    # Update the ticket status
                    ticket_id = request.POST.get('ticket')
                    ticket = Ticket.objects.get(id=ticket_id)
                    ticket.status = 'CONFIRMED'
                    ticket.booking_date = datetime.now()
                    ticket.save()

                    # Update the second ticket status if exists
                    if request.POST.get('ticket2'):
                        ticket2_id = request.POST.get('ticket2')
                        ticket2 = Ticket.objects.get(id=ticket2_id)
                        ticket2.status = 'CONFIRMED'
                        ticket2.save()

                    # Render success page on successful capture of payment
                    return render(request, 'paymentsuccess.html')
                except Exception as e:
                    print("host details not matching")
                    return render(request, 'paymentfail.html', {'error': str(e)})
            else:
                return render(request, 'paymentfail.html')
        except Exception as e:
            return render(request, 'paymentfail.html', {'error': str(e)})
    else:
        return HttpResponse("Method must be POST.")

def ticket_data(request, ref):
    ticket = Ticket.objects.get(ref_no=ref)
    return JsonResponse({
        'ref': ticket.ref_no,
        'from': ticket.flight.origin.code,
        'to': ticket.flight.destination.code,
        'flight_date': ticket.flight_ddate,
        'status': ticket.status
    })


    """
    The `get_ticket` function retrieves a ticket object based on a reference number from the request and
    generates a PDF ticket using a template.
    
    :param request: The `request` parameter in the `get_ticket` function is an HttpRequest object that
    represents the HTTP request made by the client. It contains information about the request, such as
    the request method, headers, GET and POST parameters, and more. In this context, the function is
    retrieving a ticket object
    :return: The code snippet is returning a PDF file generated from a ticket template using the data
    retrieved from the Ticket model in the Django application. The PDF file is generated using the
    render_to_pdf function with the ticket data and then returned as an HttpResponse with the content
    type 'application/pdf'.
    """
@csrf_exempt
def get_ticket(request): 
    ref = request.GET.get("ref")
    ticket1 = Ticket.objects.get(ref_no = ref)
    data = {
        'ticket1':ticket1,
        'current_year': datetime.now().year
    }
    pdf = render_to_pdf('flight/ticket.html', data)
    return HttpResponse(pdf, content_type='application/pdf')



def bookings(request): 
    """
    The `bookings` function checks if a user is authenticated, retrieves their tickets if so, and
    renders a bookings page, otherwise redirects to the login page.
    
    :param request: The `request` parameter in the `bookings` function is typically an HttpRequest
    object that represents the current web request. It contains information about the request made by
    the user, such as user authentication status, user data, request method (GET, POST, etc.), and other
    metadata related to the request
    :return: The `bookings` function is returning a response based on the user's authentication status.
    If the user is authenticated, it retrieves the tickets associated with the authenticated user and
    renders the 'flight/bookings.html' template with the 'tickets' context. If the user is not
    authenticated, it redirects to the 'login' page.
    """
    if request.user.is_authenticated: 
        tickets = Ticket.objects.filter(user=request.user).order_by('-booking_date')
        return render(request, 'flight/bookings.html',{
            'page': 'bookings', 
            'tickets': tickets
        })
    
    else: 
        return HttpResponseRedirect(reverse('login'))
    

    """
    This function checks if a user is authenticated and if so, retrieves ticket information for payment
    processing.
    
    :param request: The `request` parameter in the `resume_booking` function is an object that contains
    information about the current HTTP request. It includes details such as the request method (GET,
    POST, etc.), user authentication status, and any data sent with the request (such as form data or
    URL parameters). The
    :return: If the request method is POST and the user is authenticated, the function will return a
    rendered payment.html template with the ticket's total fare and ID. If the ticket's user does not
    match the request user, it will return "User unauthorised". If the user is not authenticated, it
    will redirect to the login page. If the request method is not POST, it will return "Method must
    """
def resume_booking(request): 
    if request.method == 'POST': 
        if request.user.is_authenticated:
            ref = request.POST.get('ref')
            ticket = Ticket.objects.get(ref_no=ref)
            if ticket.user == request.user: 
                return render(request, 'flight/payment.html', {
                    'fare': ticket.total_fare, 
                    'ticket': ticket.id
                }) 
            else: 
                return HttpResponse("User unauthorised")
        else: 
            return HttpResponseRedirect(reverse('login'))
    else: 
        return HttpResponse("Method must be post.")
    
@csrf_exempt
def cancel_ticket(request): 
    if request.method == 'POST': 
        if request.user.is_authenticated: 
            ref = request.POST.get('ref')
            try: 
                ticket = Ticket.objects.get(ref_no = ref)
                if ticket.user == request.user: 
                    ticket.status = "CANCELLED"
                    ticket.save()
                    return JsonResponse({
                        'success': True
                    })
                else: 
                    return JsonResponse({
                        'success': False, 
                        'error': "User unauthorized"
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False, 
                    'error': e
                }) 
        else:
            return HttpResponse("User unauthorized") 
    else: 
        return HttpResponse("Method must be POST.")



def seatmap(request):
    return render(request, 'flight/seatmap.html')


def web_checkin(request): 
    """
    The `web_checkin` function handles the web check-in process by validating a form submission and
    checking if a ticket with the provided reference number exists before rendering the seat map or
    displaying an error message.
    
    :param request: The `request` parameter in the `web_checkin` function is typically an HttpRequest
    object that represents the HTTP request made by a user. It contains information about the request,
    such as the method used (GET, POST, etc.), any data sent in the request, user session information,
    and more
    :return: The `web_checkin` function returns either the 'flight/seatmap.html' template if the ticket
    is verified and found, or an HttpResponse with the message "Ticket not found" if the ticket is not
    found.
    """
    if request.method == "POST": 
        form = CheckInForm(request.POST)
        if form.is_valid(): 

            ref = form.cleaned_data["ref"]

            #check-in logic
            ticket = Ticket.objects.get(ref_no=ref)
            if ticket: 
                print("Ticket verified and found")
                return render(request, 'flight/seatmap.html')
            else: 
                return HttpResponse("Ticket not found")
            

    else: 
        form = CheckInForm()

    return render(request, 'flight/web-checkin.html', {'form': form})

def seat_confirmation(request): 
    if request.method == "POST": 
        if request.user.is_authenticated: 
            seat_numbers = request.POST.get('seat')
            if seat_numbers:
                print(request.user.email)
                send_mail(
                    'Web Checkin confirmation', 
                    f'You have selected seat numbers {seat_numbers}.',
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False
                )
                return render(request, 'flight/mail.html')
            else: 
                return HttpResponse("No seat numbers selected")
        else: 
            return HttpResponse("User unauthorized")
    else: 
        return HttpResponse("Method has to be POST")