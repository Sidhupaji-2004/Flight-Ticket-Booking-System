from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("query/places/<str:q>", views.query, name="query"),
    path("flight", views.flight, name="flight"),
    path("review", views.review, name="review"),
    path("seats", views.seatmap, name="seats"),
    path("web_checkin", views.web_checkin, name="web_checkin"),
    path("flight/ticket/book", views.book, name="book"),
    path("paymenthandler", views.paymenthandler, name='paymenthandler'),
    path("flight/ticket/payment", views.payment, name="payment"),
    path("bookings", views.bookings, name="bookings"),
    path("seat_booked", views.seat_confirmation, name="seat_booked"),
    path('flight/ticket/api/<str:ref>', views.ticket_data, name="ticketdata"),
    path('flight/ticket/print',views.get_ticket, name="getticket"),
    path('flight/ticket/cancel', views.cancel_ticket, name="cancelticket"),
    path('flight/ticket/resume', views.resume_booking, name="resumebooking"),
]