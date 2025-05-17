# CourtReserve Backend API Design - V2 (Dynamic Booking)

This document outlines the API endpoints required to support a dynamic reservation workflow, including court availability, booking, approval, cancellation, court following, and notifications.

## 1. Authentication

- Existing JWT-based authentication will be used. All private endpoints will require a valid `Authorization: Bearer <token>` header.

## 2. Courts API

### GET /api/courts
- **Description:** Get a list of all courts.
- **Response:** `200 OK`
  ```json
  [
    {
      "id": 1,
      "name": "Cerciler",
      "surface_type": "Hard",
      "setting": "Outdoor",
      "description": "Cerciler hard court.",
      "address": "Cerciler Tennis Club",
      "operating_hours": {"default": ["07:00", "22:00"]},
      "status": "active",
      "is_followed_by_current_user": true // New field
    },
    // ... other courts
  ]
  ```

### GET /api/courts/<int:court_id>
- **Description:** Get details for a specific court.
- **Response:** `200 OK`
  ```json
  {
    "id": 1,
    "name": "Cerciler",
    "surface_type": "Hard",
    // ... other court details
    "is_followed_by_current_user": false // New field
  }
  ```

### GET /api/courts/<int:court_id>/availability
- **Description:** Get daily availability for a specific court for a given date. Slots are 1 hour long.
- **Query Parameters:**
  - `date` (string, YYYY-MM-DD): The date for which to fetch availability.
- **Response:** `200 OK`
  ```json
  {
    "court_id": 1,
    "date": "2025-05-17",
    "operating_hours": ["07:00", "22:00"], // Court's operating hours for the day
    "available_slots": [
      {"time": "07:00", "status": "available"},
      {"time": "08:00", "status": "booked", "booking_id": 101, "booked_by_current_user": false},
      {"time": "09:00", "status": "available"},
      // ... more slots for the day, up to closing time
      {"time": "21:00", "status": "pending_approval", "booking_id": 102, "booked_by_current_user": true}
    ]
  }
  ```
  - `status` can be: `available`, `booked`, `pending_approval`, `unavailable` (e.g., maintenance, outside operating hours).

## 3. Bookings API

### POST /api/bookings/request
- **Description:** Create a new booking request.
- **Authentication:** Required (Player, Tutor, Court Responsible)
- **Request Body:**
  ```json
  {
    "court_id": 1,
    "date": "2025-05-17", // YYYY-MM-DD
    "time": "09:00", // HH:MM (start time of 1-hour slot)
    "note": "Optional note for the booking."
  }
  ```
- **Response:** `201 Created`
  ```json
  {
    "message": "Booking request created successfully. Awaiting approval.",
    "booking": {
      "id": 103,
      "court_id": 1,
      "user_id": 5, // ID of the user making the booking
      "date": "2025-05-17",
      "time": "09:00",
      "status": "pending_approval",
      "note": "Optional note for the booking.",
      "created_at": "2025-05-16T10:30:00Z"
    }
  }
  ```
- **Error Responses:** `400 Bad Request` (e.g., slot not available, invalid data), `409 Conflict` (e.g., slot already booked/pending).

### GET /api/bookings
- **Description:** Get a list of bookings for the current user.
- **Authentication:** Required
- **Query Parameters (Optional):**
  - `status` (string): Filter by status (e.g., `pending_approval`, `confirmed`, `cancelled`, `completed`)
  - `period` (string): Filter by period (e.g., `upcoming`, `past`)
- **Response:** `200 OK`
  ```json
  [
    {
      "id": 103,
      "court_id": 1,
      "court_name": "Cerciler",
      "date": "2025-05-17",
      "time": "09:00",
      "status": "pending_approval",
      // ... other booking details
    }
  ]
  ```

### GET /api/bookings/court/<int:court_id>
- **Description:** Get bookings for a specific court (for court responsible users).
- **Authentication:** Required (Court Responsible for this court)
- **Query Parameters (Optional):**
  - `status` (string): Filter by status.
  - `date` (string, YYYY-MM-DD): Filter by date.
- **Response:** `200 OK` (similar to `/api/bookings` but for a specific court and includes user details)

### POST /api/bookings/<int:booking_id>/approve
- **Description:** Approve a pending booking request.
- **Authentication:** Required (Court Responsible for the court associated with the booking)
- **Response:** `200 OK`
  ```json
  {
    "message": "Booking approved successfully.",
    "booking": { /* updated booking object with status 'confirmed' */ }
  }
  ```
- **Notifications:** Notify the user who made the booking.

### POST /api/bookings/<int:booking_id>/reject
- **Description:** Reject a pending booking request.
- **Authentication:** Required (Court Responsible)
- **Request Body (Optional):**
  ```json
  {
    "reason": "Court maintenance scheduled at that time."
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "message": "Booking rejected.",
    "booking": { /* updated booking object with status 'rejected' */ }
  }
  ```
- **Notifications:** Notify the user who made the booking, including reason if provided.

### POST /api/bookings/<int:booking_id>/cancel
- **Description:** Cancel a confirmed or pending booking.
- **Authentication:** Required (User who made the booking OR Court Responsible)
- **Response:** `200 OK`
  ```json
  {
    "message": "Booking cancelled successfully.",
    "booking": { /* updated booking object with status 'cancelled' */ }
  }
  ```
- **Logic:** Enforce 1-hour cancellation policy (cannot cancel if booking is less than 1 hour away, unless by Court Responsible).
- **Notifications:** If cancelled by user and slot becomes available, notify followers of the court. If cancelled by Court Responsible, notify the user who made the booking.

## 4. Court Following API

### POST /api/courts/<int:court_id>/follow
- **Description:** Current user follows a specific court.
- **Authentication:** Required
- **Response:** `200 OK`
  ```json
  {
    "message": "You are now following Court Cerciler."
  }
  ```

### POST /api/courts/<int:court_id>/unfollow
- **Description:** Current user unfollows a specific court.
- **Authentication:** Required
- **Response:** `200 OK`
  ```json
  {
    "message": "You have unfollowed Court Cerciler."
  }
  ```

### GET /api/users/me/followed-courts
- **Description:** Get a list of courts followed by the current user.
- **Authentication:** Required
- **Response:** `200 OK`
  ```json
  [
    { "id": 1, "name": "Cerciler" /* ... other minimal court details */ },
    { "id": 3, "name": "Yarimada" }
  ]
  ```

## 5. Notifications (Conceptual)

- Notifications will be triggered by backend actions (booking approval, rejection, cancellation).
- A mechanism to store and retrieve notifications for users will be needed (e.g., a `Notification` model and `/api/notifications` endpoint).
- Notification content will include: Court Name, Date/Time, Status (Approved, Cancelled, Slot Available).

## 6. User Roles and Permissions

- **Player:** Can request bookings, cancel their own bookings (respecting policy), follow/unfollow courts.
- **Tutor:** Same as Player. (Future: May have special booking privileges or visibility).
- **Court Responsible:** Can request bookings, approve/reject/cancel any booking for their managed courts, manage court details (future).

This API design provides a foundation for the dynamic reservation system. Further details for each endpoint (e.g., specific error codes, request validation) will be refined during implementation.
