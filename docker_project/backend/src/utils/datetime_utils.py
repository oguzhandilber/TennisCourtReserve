"""
Utility functions for date and time operations in the TennisCourtReserve application.

This module provides helper functions for handling date and time operations,
including validation, formatting, and calculations specific to court bookings.
"""

import datetime
from typing import List, Tuple, Optional

def is_valid_booking_time(start_time: datetime.datetime, end_time: datetime.datetime) -> bool:
    """
    Validate if the booking time is valid according to business rules.
    
    Args:
        start_time (datetime): The booking start time
        end_time (datetime): The booking end time
        
    Returns:
        bool: True if the booking time is valid, False otherwise
    """
    # Check if end time is after start time
    if end_time <= start_time:
        return False
    
    # Check if booking is within the same day
    if start_time.date() != end_time.date():
        return False
    
    # Check if booking duration is valid (minimum 30 minutes, maximum 2 hours)
    duration = (end_time - start_time).total_seconds() / 60
    if duration < 30 or duration > 120:
        return False
    
    # Check if booking starts and ends on the hour or half-hour
    if start_time.minute not in (0, 30) or end_time.minute not in (0, 30):
        return False
    
    # Check if booking is within operating hours (8:00 AM to 10:00 PM)
    opening_time = datetime.time(8, 0)
    closing_time = datetime.time(22, 0)
    if start_time.time() < opening_time or end_time.time() > closing_time:
        return False
    
    return True

def get_available_slots(
    court_id: int, 
    date: datetime.date,
    existing_bookings: List[Tuple[datetime.datetime, datetime.datetime]]
) -> List[Tuple[datetime.datetime, datetime.datetime]]:
    """
    Calculate available time slots for a court on a specific date.
    
    Args:
        court_id (int): The ID of the court
        date (datetime.date): The date to check availability for
        existing_bookings (List[Tuple]): List of (start_time, end_time) tuples for existing bookings
        
    Returns:
        List[Tuple]: List of available (start_time, end_time) slots
    """
    # Define operating hours
    opening_time = datetime.time(8, 0)
    closing_time = datetime.time(22, 0)
    
    # Create datetime objects for opening and closing times on the specified date
    start_datetime = datetime.datetime.combine(date, opening_time)
    end_datetime = datetime.datetime.combine(date, closing_time)
    
    # Generate all possible 30-minute slots
    all_slots = []
    current = start_datetime
    while current < end_datetime:
        slot_end = current + datetime.timedelta(minutes=30)
        all_slots.append((current, slot_end))
        current = slot_end
    
    # Remove slots that overlap with existing bookings
    available_slots = []
    for slot_start, slot_end in all_slots:
        is_available = True
        for booking_start, booking_end in existing_bookings:
            # Check if slot overlaps with booking
            if (slot_start < booking_end and slot_end > booking_start):
                is_available = False
                break
        
        if is_available:
            available_slots.append((slot_start, slot_end))
    
    # Merge consecutive available slots into longer slots
    merged_slots = []
    if available_slots:
        current_start, current_end = available_slots[0]
        
        for i in range(1, len(available_slots)):
            next_start, next_end = available_slots[i]
            
            # If slots are consecutive, extend the current slot
            if current_end == next_start:
                current_end = next_end
            else:
                # Add the current slot to merged slots and start a new one
                merged_slots.append((current_start, current_end))
                current_start, current_end = next_start, next_end
        
        # Add the last slot
        merged_slots.append((current_start, current_end))
    
    return merged_slots

def is_within_cancellation_window(booking_time: datetime.datetime) -> bool:
    """
    Check if a booking is within the cancellation window (more than 1 hour before start time).
    
    Args:
        booking_time (datetime): The booking start time
        
    Returns:
        bool: True if booking can be cancelled, False otherwise
    """
    now = datetime.datetime.utcnow()
    cancellation_deadline = booking_time - datetime.timedelta(hours=1)
    return now < cancellation_deadline

def format_datetime_for_display(dt: datetime.datetime) -> str:
    """
    Format a datetime object for display in the UI.
    
    Args:
        dt (datetime): The datetime to format
        
    Returns:
        str: Formatted datetime string
    """
    return dt.strftime("%B %d, %Y at %I:%M %p")

def format_date_for_api(date: datetime.date) -> str:
    """
    Format a date object for API requests.
    
    Args:
        date (datetime.date): The date to format
        
    Returns:
        str: Formatted date string (YYYY-MM-DD)
    """
    return date.strftime("%Y-%m-%d")

def parse_datetime_from_string(datetime_str: str) -> Optional[datetime.datetime]:
    """
    Parse a datetime string into a datetime object.
    
    Args:
        datetime_str (str): The datetime string to parse
        
    Returns:
        datetime or None: Parsed datetime object or None if parsing fails
    """
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M"
    ]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    
    return None
