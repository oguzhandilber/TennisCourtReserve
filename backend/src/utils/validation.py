"""
Validation utilities for the TennisCourtReserve application.

This module provides functions for validating user input, request data,
and business rules throughout the application.
"""

from typing import Dict, Any, List, Optional, Tuple
import re
from datetime import datetime, timedelta
from src.utils.datetime_utils import is_valid_booking_time, parse_datetime_from_string
from src.utils.error_handlers import APIError

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """
    Validate that all required fields are present in the data.
    
    Args:
        data (Dict): The data to validate
        required_fields (List): List of required field names
        
    Raises:
        APIError: If any required field is missing
    """
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        if len(missing_fields) == 1:
            error_message = f"Missing required field: {missing_fields[0]}"
        else:
            error_message = f"Missing required fields: {', '.join(missing_fields)}"
        
        raise APIError(error_message, status_code=400)

def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email (str): The email to validate
        
    Returns:
        bool: True if email is valid, False otherwise
        
    Raises:
        APIError: If email format is invalid
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        raise APIError("Invalid email format", status_code=400)
    
    return True

def validate_password(password: str) -> bool:
    """
    Validate password strength.
    
    Args:
        password (str): The password to validate
        
    Returns:
        bool: True if password is valid, False otherwise
        
    Raises:
        APIError: If password doesn't meet requirements
    """
    if len(password) < 8:
        raise APIError("Password must be at least 8 characters long", status_code=400)
    
    if not any(char.isdigit() for char in password):
        raise APIError("Password must contain at least one number", status_code=400)
    
    if not any(char.isupper() for char in password):
        raise APIError("Password must contain at least one uppercase letter", status_code=400)
    
    if not any(char.islower() for char in password):
        raise APIError("Password must contain at least one lowercase letter", status_code=400)
    
    return True

def validate_booking_request(data: Dict[str, Any]) -> Tuple[datetime, datetime]:
    """
    Validate booking request data.
    
    Args:
        data (Dict): The booking request data
        
    Returns:
        Tuple: Validated start_time and end_time as datetime objects
        
    Raises:
        APIError: If booking data is invalid
    """
    # Check required fields
    validate_required_fields(data, ['court_id', 'start_time', 'end_time'])
    
    # Parse datetime strings
    start_time = parse_datetime_from_string(data['start_time'])
    end_time = parse_datetime_from_string(data['end_time'])
    
    if not start_time or not end_time:
        raise APIError("Invalid datetime format", status_code=400)
    
    # Validate booking time
    if not is_valid_booking_time(start_time, end_time):
        raise APIError(
            "Invalid booking time. Bookings must be between 30 minutes and 2 hours, "
            "start and end on the hour or half-hour, and be within operating hours (8:00 AM to 10:00 PM).",
            status_code=400
        )
    
    # Validate booking is in the future
    if start_time < datetime.utcnow():
        raise APIError("Booking must be in the future", status_code=400)
    
    # Validate booking is not too far in the future (e.g., 30 days)
    max_future_date = datetime.utcnow() + timedelta(days=30)
    if start_time > max_future_date:
        raise APIError("Booking cannot be more than 30 days in the future", status_code=400)
    
    return start_time, end_time

def validate_user_role(role: str) -> bool:
    """
    Validate user role.
    
    Args:
        role (str): The role to validate
        
    Returns:
        bool: True if role is valid, False otherwise
        
    Raises:
        APIError: If role is invalid
    """
    valid_roles = ['player', 'trainer', 'court_responsible']
    
    if role not in valid_roles:
        raise APIError(f"Invalid role. Must be one of: {', '.join(valid_roles)}", status_code=400)
    
    return True

def sanitize_string(input_string: str) -> str:
    """
    Sanitize a string input to prevent injection attacks.
    
    Args:
        input_string (str): The string to sanitize
        
    Returns:
        str: Sanitized string
    """
    # Remove HTML tags
    sanitized = re.sub(r'<[^>]*>', '', input_string)
    
    # Limit length
    max_length = 1000
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized
