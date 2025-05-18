"""
Error handling utilities for the TennisCourtReserve application.

This module provides standardized error handling functions and decorators
to ensure consistent error responses across the application.
"""

from functools import wraps
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
import logging

# Configure logger
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base exception class for API errors."""
    
    def __init__(self, message, status_code=400, payload=None):
        """
        Initialize APIError with message and optional status code and payload.
        
        Args:
            message (str): Error message
            status_code (int): HTTP status code
            payload (dict): Additional data to include in the response
        """
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """
        Convert error to dictionary format for JSON response.
        
        Returns:
            dict: Error details including message and optional payload
        """
        error_dict = dict(self.payload or ())
        error_dict['error'] = self.message
        error_dict['status_code'] = self.status_code
        return error_dict

def handle_api_error(error):
    """
    Handle APIError exceptions by returning appropriate JSON response.
    
    Args:
        error (APIError): The error that occurred
        
    Returns:
        tuple: JSON response and HTTP status code
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def handle_database_error(error):
    """
    Handle SQLAlchemy database errors.
    
    Args:
        error (SQLAlchemyError): The database error that occurred
        
    Returns:
        tuple: JSON response and HTTP status code
    """
    logger.error(f"Database error: {str(error)}")
    response = jsonify({
        'error': 'Database error occurred',
        'status_code': 500
    })
    response.status_code = 500
    return response

def handle_http_exception(error):
    """
    Handle HTTP exceptions from Flask/Werkzeug.
    
    Args:
        error (HTTPException): The HTTP exception that occurred
        
    Returns:
        tuple: JSON response and HTTP status code
    """
    response = jsonify({
        'error': error.description,
        'status_code': error.code
    })
    response.status_code = error.code
    return response

def handle_generic_error(error):
    """
    Handle any unhandled exceptions.
    
    Args:
        error (Exception): The exception that occurred
        
    Returns:
        tuple: JSON response and HTTP status code
    """
    logger.error(f"Unhandled exception: {str(error)}")
    response = jsonify({
        'error': 'An unexpected error occurred',
        'status_code': 500
    })
    response.status_code = 500
    return response

def register_error_handlers(app):
    """
    Register all error handlers with the Flask application.
    
    Args:
        app (Flask): The Flask application instance
    """
    app.register_error_handler(APIError, handle_api_error)
    app.register_error_handler(SQLAlchemyError, handle_database_error)
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_generic_error)

def api_error_handler(f):
    """
    Decorator to handle exceptions in API routes.
    
    Args:
        f (function): The function to decorate
        
    Returns:
        function: Decorated function with error handling
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIError as e:
            return handle_api_error(e)
        except SQLAlchemyError as e:
            return handle_database_error(e)
        except HTTPException as e:
            return handle_http_exception(e)
        except Exception as e:
            return handle_generic_error(e)
    return decorated
