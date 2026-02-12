import datetime
import threading
from .styles import STYLES

bookings = []
booking_lock = threading.Lock()

def check_availability(requested_time, duration=60):
    requested_start = requested_time
    requested_end = requested_time + datetime.timedelta(minutes=duration)
    for booking in bookings:
        booked_start = booking['time']
        booked_end = booked_start + datetime.timedelta(minutes=booking['duration'])
        if (requested_start < booked_end and requested_end > booked_start):
            return False
    return True

def book_session(name, mobile, style, time_str):
    with booking_lock:
        if style not in STYLES:
            return f"Sorry, we don't offer '{style}'."
        try:
            requested_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return "Invalid date/time format. Please use YYYY-MM-DD HH:MM."
        duration = 60
        if not check_availability(requested_time, duration):
            return "Sorry, that time slot is already booked. Please choose another time."
        bookings.append({
            "name": name,
            "mobile": mobile,
            "style": style,
            "time": requested_time,
            "duration": duration
        })
        return f"Session booked for {name} - {style.title()} on {requested_time.strftime('%Y-%m-%d %H:%M')}."