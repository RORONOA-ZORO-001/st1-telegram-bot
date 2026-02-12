import unittest
from salon.bookings import book_session, bookings

class TestBooking(unittest.TestCase):
    def setUp(self):
        bookings.clear()

    def test_successful_booking(self):
        result = book_session("Alice", "haircut", "2024-07-01 10:00")
        self.assertIn("Session booked for Alice", result)

    def test_invalid_style(self):
        result = book_session("Bob", "massage", "2024-07-01 11:00")
        self.assertIn("don't offer", result)

    def test_invalid_time_format(self):
        result = book_session("Carol", "haircut", "07/01/2024 10:00")
        self.assertIn("Invalid date/time format", result)

    def test_double_booking(self):
        book_session("Dave", "haircut", "2024-07-01 12:00")
        result = book_session("Eve", "haircut", "2024-07-01 12:00")
        self.assertIn("already booked", result)

if __name__ == "__main__":
    unittest.main()