# TennisCourtReserve Project Documentation

## Overview
TennisCourtReserve is a comprehensive tennis court reservation system that allows players to book courts, trainers to manage sessions, and court administrators to oversee bookings. The system features real-time notifications, court following, and a robust booking approval workflow.

## System Architecture

### Backend
- **Framework**: Flask with SQLAlchemy ORM
- **Authentication**: JWT-based authentication
- **Real-time Communication**: Socket.IO for WebSockets
- **Database**: SQLite (development), PostgreSQL (production-ready)

### Frontend
- **Technology**: HTML, CSS, JavaScript
- **Responsive Design**: Mobile and desktop compatible
- **Real-time Updates**: WebSocket integration

## Features

### User Management
- Multiple user roles (player, trainer, court responsible)
- Secure authentication and authorization
- Profile management

### Court Management
- Court listing and details
- Court availability calendar
- Court following for updates

### Booking System
- Real-time availability checking
- Booking request submission
- Booking approval workflow
- Cancellation with time policy enforcement

### Notifications
- Real-time notifications via WebSockets
- Booking status updates
- Court availability alerts
- Notification management (read/unread)

## Installation Guide

### Prerequisites
- Python 3.8+
- Node.js 14+ (for development tools)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/oguzhandilber/TennisCourtReserve.git
   cd TennisCourtReserve
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   cd src
   export FLASK_APP=main.py
   flask db init
   flask db migrate
   flask db upgrade
   flask seed-db  # Optional: seed with sample data
   ```

5. **Start the backend server**
   ```bash
   python main.py
   ```

6. **Serve the frontend**
   ```bash
   # In a new terminal
   cd frontend
   python -m http.server 8080
   ```

7. **Access the application**
   - Backend API: http://localhost:5000/api
   - Frontend: http://localhost:8080

## API Documentation

### Authentication Endpoints

#### POST /api/auth/register
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "name": "John Doe",
  "role": "player"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### POST /api/auth/login
Authenticate a user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user_id": 1,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Court Endpoints

#### GET /api/courts
Get all available courts.

**Response:**
```json
{
  "courts": [
    {
      "id": 1,
      "name": "Center Court",
      "surface_type": "clay",
      "is_indoor": false,
      "status": "active"
    }
  ]
}
```

#### GET /api/courts/{court_id}
Get details for a specific court.

**Response:**
```json
{
  "id": 1,
  "name": "Center Court",
  "surface_type": "clay",
  "is_indoor": false,
  "status": "active",
  "description": "Our premier clay court with stadium seating."
}
```

#### GET /api/courts/{court_id}/availability
Get availability for a specific court.

**Query Parameters:**
- `date`: Date in YYYY-MM-DD format

**Response:**
```json
{
  "court_id": 1,
  "date": "2025-05-18",
  "available_slots": [
    {
      "start_time": "2025-05-18T08:00:00",
      "end_time": "2025-05-18T08:30:00"
    }
  ]
}
```

### Booking Endpoints

#### POST /api/bookings
Create a new booking request.

**Request Body:**
```json
{
  "court_id": 1,
  "start_time": "2025-05-18T14:00:00",
  "end_time": "2025-05-18T15:00:00",
  "user_note": "Friendly match with Alex"
}
```

**Response:**
```json
{
  "message": "Booking request submitted successfully",
  "booking_id": 1,
  "status": "pending_approval"
}
```

#### GET /api/bookings
Get bookings for the current user.

**Query Parameters:**
- `period`: "upcoming" or "past"
- `status`: Filter by status (optional)
- `date`: Filter by date (optional)

**Response:**
```json
{
  "bookings": [
    {
      "id": 1,
      "court_id": 1,
      "court_name": "Center Court",
      "start_time": "2025-05-18T14:00:00",
      "end_time": "2025-05-18T15:00:00",
      "status": "confirmed",
      "user_note": "Friendly match with Alex"
    }
  ]
}
```

#### PUT /api/bookings/{booking_id}/approve
Approve a booking request (court responsible only).

**Request Body:**
```json
{
  "court_responsible_note": "Approved as requested"
}
```

**Response:**
```json
{
  "message": "Booking approved successfully",
  "booking_id": 1
}
```

#### PUT /api/bookings/{booking_id}/reject
Reject a booking request (court responsible only).

**Request Body:**
```json
{
  "court_responsible_note": "Court maintenance scheduled"
}
```

**Response:**
```json
{
  "message": "Booking rejected successfully",
  "booking_id": 1
}
```

#### PUT /api/bookings/{booking_id}/cancel
Cancel a booking.

**Response:**
```json
{
  "message": "Booking cancelled successfully",
  "booking_id": 1
}
```

### Notification Endpoints

#### GET /api/notifications
Get notifications for the current user.

**Query Parameters:**
- `unread_only`: true/false (optional)
- `page`: Page number (optional)
- `per_page`: Items per page (optional)

**Response:**
```json
{
  "notifications": [
    {
      "id": 1,
      "type": "booking_status",
      "content": "Your booking for Center Court on May 18 has been approved!",
      "is_read": false,
      "created_at": "2025-05-17T10:30:00"
    }
  ],
  "total_pages": 1,
  "current_page": 1,
  "total_notifications": 1,
  "unread_count": 1
}
```

#### PUT /api/notifications/{notification_id}/read
Mark a notification as read.

**Response:**
```json
{
  "message": "Notification marked as read"
}
```

#### PUT /api/notifications/read-all
Mark all notifications as read.

**Response:**
```json
{
  "message": "All notifications marked as read",
  "count": 5
}
```

### Court Following Endpoints

#### POST /api/courts/{court_id}/follow
Follow a court to receive notifications.

**Response:**
```json
{
  "message": "You are now following Center Court",
  "court_id": 1,
  "court_name": "Center Court"
}
```

#### POST /api/courts/{court_id}/unfollow
Unfollow a court.

**Response:**
```json
{
  "message": "You have unfollowed Center Court",
  "court_id": 1,
  "court_name": "Center Court"
}
```

#### GET /api/courts/followed
Get all courts followed by the current user.

**Response:**
```json
{
  "message": "Followed courts retrieved successfully",
  "courts": [
    {
      "id": 1,
      "name": "Center Court",
      "surface_type": "clay",
      "is_indoor": false,
      "status": "active"
    }
  ],
  "count": 1
}
```

## WebSocket Events

### Client Events

#### connect
Connect to the WebSocket server.

#### authenticate
Authenticate the WebSocket connection.

**Payload:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Server Events

#### authenticated
Sent when authentication is successful.

**Payload:**
```json
{
  "user_id": 1
}
```

#### authentication_error
Sent when authentication fails.

**Payload:**
```json
{
  "message": "Invalid token"
}
```

#### notification
Sent when a new notification is available.

**Payload:**
```json
{
  "id": 1,
  "type": "booking_status",
  "content": "Your booking for Center Court on May 18 has been approved!",
  "is_read": false,
  "created_at": "2025-05-17T10:30:00"
}
```

## User Guide

### Booking a Court
1. Navigate to the Court Listing page
2. Select a court to view details
3. Check the availability calendar
4. Select an available time slot
5. Fill in booking details and submit
6. Wait for approval notification

### Managing Bookings
1. Navigate to My Bookings page
2. View upcoming and past bookings
3. Filter bookings by status or date
4. Cancel bookings if needed (subject to 1-hour policy)

### Following Courts
1. Navigate to a Court Details page
2. Click the "Follow" button
3. Receive notifications about court availability and updates
4. View followed courts in the dashboard

### Managing Notifications
1. Click the notification bell icon
2. View all notifications
3. Mark individual notifications as read
4. Use "Mark all as read" to clear notifications

## Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

### Coding Standards
- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Write unit tests for new features

### Testing
- Run backend tests: `pytest`
- Test WebSocket functionality with the notification demo page

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For questions or support, please contact the repository owner.
