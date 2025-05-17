# CourtReserve API Documentation

This document provides detailed information about the CourtReserve API endpoints, request/response formats, authentication mechanisms, and real-time event structures.

## Base URL

The base URL for all API endpoints is `http://<your_server_address>:5000`.

## Authentication

Authentication is handled using JSON Web Tokens (JWT). Most endpoints require a valid JWT access token to be included in the `Authorization` header as a Bearer token:

`Authorization: Bearer <access_token>`

Access tokens are short-lived. When an access token expires, a `401 Unauthorized` error will be returned. A refresh token (obtained during login) can be used to get a new access token via the `/auth/refresh` endpoint.

## Common Error Responses

- `400 Bad Request`: Invalid input data or malformed request.
- `401 Unauthorized`: Missing or invalid authentication token.
- `403 Forbidden`: Authenticated user does not have permission to perform the action.
- `404 Not Found`: The requested resource was not found.
- `409 Conflict`: A conflict occurred, e.g., trying to create a resource that already exists.
- `422 Unprocessable Entity`: The request was well-formed but was unable to be followed due to semantic errors (e.g., validation errors).
- `500 Internal Server Error`: An unexpected error occurred on the server.

Error responses typically include a JSON body with a `message` field explaining the error, and sometimes an `errors` field with more specific details for validation issues.




## Authentication Endpoints (`/auth`)

### 1. Register User

*   **Endpoint:** `POST /auth/register`
*   **Description:** Registers a new user.
*   **Request Body:** `application/json`
    ```json
    {
        "full_name": "string (required)",
        "email": "string (required, valid email format)",
        "password": "string (required, min 8 characters)"
    }
    ```
*   **Success Response:** `201 Created`
    ```json
    {
        "message": "User registered successfully",
        "access_token": "string (JWT)",
        "refresh_token": "string (JWT)",
        "user": {
            "id": "integer",
            "full_name": "string",
            "email": "string",
            "role": "string (e.g., player, trainer, admin)",
            "is_approved_trainer": "boolean"
        }
    }
    ```
*   **Error Responses:**
    *   `400 Bad Request`: If email already exists or password is too short.
    *   `422 Unprocessable Entity`: If input validation fails (e.g., missing fields, invalid email format).

### 2. Login User

*   **Endpoint:** `POST /auth/login`
*   **Description:** Logs in an existing user.
*   **Request Body:** `application/json`
    ```json
    {
        "email": "string (required)",
        "password": "string (required)"
    }
    ```
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "Login successful",
        "access_token": "string (JWT)",
        "refresh_token": "string (JWT)",
        "user": {
            "id": "integer",
            "full_name": "string",
            "email": "string",
            "role": "string",
            "is_approved_trainer": "boolean"
        }
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If invalid credentials are provided.

### 3. Refresh Access Token

*   **Endpoint:** `POST /auth/refresh`
*   **Description:** Refreshes an expired access token using a valid refresh token.
*   **Authentication:** Requires a valid JWT refresh token in the `Authorization` header (Bearer token).
*   **Request Body:** None
*   **Success Response:** `200 OK`
    ```json
    {
        "access_token": "string (JWT)"
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If the refresh token is invalid or expired.

### 4. Logout User (Conceptual - JWTs are stateless)

*   **Endpoint:** `POST /auth/logout` (This endpoint might be implemented to blacklist tokens if using a more complex setup, but typically JWT logout is handled client-side by deleting the tokens.)
*   **Description:** Logs out the user. In a stateless JWT setup, this typically involves the client discarding the JWTs. The backend might implement a token blocklist for enhanced security.
*   **Authentication:** Requires a valid JWT access token.
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "Logout successful. Please discard your tokens."
    }
    ```




## User Endpoints (`/users`)

### 1. Get Current User Profile

*   **Endpoint:** `GET /users/me`
*   **Description:** Retrieves the profile of the currently authenticated user.
*   **Authentication:** Required (JWT Access Token)
*   **Success Response:** `200 OK`
    ```json
    {
        "id": "integer",
        "full_name": "string",
        "email": "string",
        "role": "string",
        "is_approved_trainer": "boolean",
        "created_at": "datetime_string"
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.

### 2. Update Current User Profile

*   **Endpoint:** `PUT /users/me`
*   **Description:** Updates the profile of the currently authenticated user.
*   **Authentication:** Required (JWT Access Token)
*   **Request Body:** `application/json` (Only include fields to be updated)
    ```json
    {
        "full_name": "string (optional)",
        "email": "string (optional, valid email format)",
        "password": "string (optional, min 8 characters, will update password if provided)"
    }
    ```
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "Profile updated successfully",
        "user": {
            "id": "integer",
            "full_name": "string",
            "email": "string",
            "role": "string",
            "is_approved_trainer": "boolean"
        }
    }
    ```
*   **Error Responses:**
    *   `400 Bad Request`: If email is already in use by another user.
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `422 Unprocessable Entity`: If input validation fails.

## Court Endpoints (`/courts`)

### 1. List Active Courts

*   **Endpoint:** `GET /courts`
*   **Description:** Retrieves a list of all active courts.
*   **Authentication:** Optional (Publicly accessible)
*   **Query Parameters:**
    *   `name`: string (optional) - Filter courts by name (partial match).
    *   `location`: string (optional) - Filter courts by location (partial match).
    *   `type`: string (optional) - Filter courts by type (e.g., Tennis, Badminton).
*   **Success Response:** `200 OK`
    ```json
    {
        "courts": [
            {
                "id": "integer",
                "name": "string",
                "location": "string",
                "type": "string",
                "description": "string",
                "hourly_rate": "float",
                "operating_hours": "string (e.g., 08:00-22:00)",
                "is_active": "boolean"
            }
            // ... more courts
        ]
    }
    ```

### 2. Get Specific Court Details

*   **Endpoint:** `GET /courts/<court_id>`
*   **Description:** Retrieves details for a specific court.
*   **Authentication:** Optional (Publicly accessible)
*   **Path Parameters:**
    *   `court_id`: integer (required) - The ID of the court.
*   **Success Response:** `200 OK`
    ```json
    {
        "id": "integer",
        "name": "string",
        "location": "string",
        "type": "string",
        "description": "string",
        "hourly_rate": "float",
        "operating_hours": "string",
        "is_active": "boolean",
        "created_at": "datetime_string",
        "updated_at": "datetime_string"
    }
    ```
*   **Error Responses:**
    *   `404 Not Found`: If the court with the given ID does not exist.

### 3. Get Court Availability

*   **Endpoint:** `GET /courts/<court_id>/availability`
*   **Description:** Retrieves the availability slots for a specific court on a given date.
*   **Authentication:** Optional (Publicly accessible)
*   **Path Parameters:**
    *   `court_id`: integer (required) - The ID of the court.
*   **Query Parameters:**
    *   `date`: string (required, format `YYYY-MM-DD`) - The date for which to check availability.
*   **Success Response:** `200 OK`
    ```json
    {
        "court_id": "integer",
        "date": "string (YYYY-MM-DD)",
        "availability": [
            {
                "start_time": "datetime_string (YYYY-MM-DDTHH:MM:SS)",
                "end_time": "datetime_string (YYYY-MM-DDTHH:MM:SS)",
                "status": "string (available, booked, pending, unavailable)"
            }
            // ... more slots
        ]
    }
    ```
*   **Error Responses:**
    *   `400 Bad Request`: If the date format is invalid.
    *   `404 Not Found`: If the court with the given ID does not exist.




## Booking Endpoints (`/bookings`)

### 1. Create a New Booking

*   **Endpoint:** `POST /bookings`
*   **Description:** Allows a player to request a new booking for a court.
*   **Authentication:** Required (JWT Access Token for Player role)
*   **Request Body:** `application/json`
    ```json
    {
        "court_id": "integer (required)",
        "start_time": "datetime_string (required, YYYY-MM-DDTHH:MM:SS)",
        "end_time": "datetime_string (required, YYYY-MM-DDTHH:MM:SS)",
        "notes": "string (optional)"
    }
    ```
*   **Success Response:** `201 Created`
    ```json
    {
        "message": "Booking request created successfully. Awaiting trainer approval.",
        "booking": {
            "id": "integer",
            "user_id": "integer",
            "court_id": "integer",
            "start_time": "datetime_string",
            "end_time": "datetime_string",
            "status": "string (pending)",
            "notes": "string",
            "total_price": "float"
        }
    }
    ```
*   **Error Responses:**
    *   `400 Bad Request`: If the requested slot is invalid, outside operating hours, or overlaps with existing bookings.
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `403 Forbidden`: If the user is not a player or tries to book too many pending slots.
    *   `404 Not Found`: If the court does not exist.
    *   `409 Conflict`: If the slot is already booked or pending for another user.
    *   `422 Unprocessable Entity`: If input validation fails.

### 2. Get User's Bookings

*   **Endpoint:** `GET /bookings`
*   **Description:** Retrieves a list of bookings for the currently authenticated user.
*   **Authentication:** Required (JWT Access Token)
*   **Query Parameters:**
    *   `status`: string (optional) - Filter bookings by status (e.g., `pending`, `approved`, `declined`, `cancelled_by_user`, `cancelled_by_trainer`). Can be a comma-separated list.
    *   `court_id`: integer (optional) - Filter by specific court ID.
    *   `date_from`: string (optional, `YYYY-MM-DD`) - Filter bookings from this date.
    *   `date_to`: string (optional, `YYYY-MM-DD`) - Filter bookings up to this date.
*   **Success Response:** `200 OK`
    ```json
    {
        "bookings": [
            {
                "id": "integer",
                "user_id": "integer",
                "court_id": "integer",
                "court_name": "string", // Added for convenience
                "start_time": "datetime_string",
                "end_time": "datetime_string",
                "status": "string",
                "notes": "string",
                "total_price": "float",
                "created_at": "datetime_string",
                "updated_at": "datetime_string"
            }
            // ... more bookings
        ]
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.

### 3. Get Specific Booking Details

*   **Endpoint:** `GET /bookings/<booking_id>`
*   **Description:** Retrieves details for a specific booking.
*   **Authentication:** Required (JWT Access Token - user must own the booking or be a trainer/admin)
*   **Path Parameters:**
    *   `booking_id`: integer (required) - The ID of the booking.
*   **Success Response:** `200 OK`
    ```json
    {
        "id": "integer",
        "user_id": "integer",
        "user_full_name": "string", // Added for convenience
        "court_id": "integer",
        "court_name": "string", // Added for convenience
        "start_time": "datetime_string",
        "end_time": "datetime_string",
        "status": "string",
        "notes": "string",
        "total_price": "float",
        "created_at": "datetime_string",
        "updated_at": "datetime_string"
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `403 Forbidden`: If the user does not have permission to view this booking.
    *   `404 Not Found`: If the booking does not exist.

### 4. Cancel a Booking (Player)

*   **Endpoint:** `PUT /bookings/<booking_id>/cancel`
*   **Description:** Allows a player to cancel their own booking (if pending or approved with sufficient notice).
*   **Authentication:** Required (JWT Access Token for Player role)
*   **Path Parameters:**
    *   `booking_id`: integer (required) - The ID of the booking to cancel.
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "Booking cancelled successfully",
        "booking": { // updated booking details }
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `403 Forbidden`: If the user is not the owner of the booking or cancellation is not allowed (e.g., too close to start time for an approved booking).
    *   `404 Not Found`: If the booking does not exist.
    *   `409 Conflict`: If the booking cannot be cancelled in its current state.




## Trainer Endpoints (`/trainer`)

These endpoints are for users with the `trainer` role to manage booking requests for courts they are assigned to.

### 1. Get Bookings for Managed Courts

*   **Endpoint:** `GET /trainer/bookings`
*   **Description:** Retrieves a list of booking requests for courts managed by the authenticated trainer.
*   **Authentication:** Required (JWT Access Token for Trainer role)
*   **Query Parameters:**
    *   `page`: integer (optional, default: 1) - For pagination.
    *   `per_page`: integer (optional, default: 10) - Number of items per page.
    *   `status`: string (optional, default: `pending`) - Filter bookings by status (e.g., `pending`, `approved`, `declined`).
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "<Status> bookings for managed courts retrieved successfully",
        "bookings": [
            {
                "id": "integer",
                "user_id": "integer",
                "user_full_name": "string", // User who made the booking
                "court_id": "integer",
                "court_name": "string",
                "start_time": "datetime_string",
                "end_time": "datetime_string",
                "status": "string",
                "notes": "string (player notes)",
                "trainer_notes": "string (trainer notes, if any)",
                "total_price": "float",
                "created_at": "datetime_string"
            }
            // ... more bookings
        ],
        "total_pages": "integer",
        "current_page": "integer",
        "total_bookings": "integer"
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `403 Forbidden`: If the user is not a trainer.
    *   `200 OK` with empty bookings list if trainer manages no courts or no bookings match filter.

### 2. Approve a Pending Booking

*   **Endpoint:** `PUT /trainer/bookings/<booking_id>/approve`
*   **Description:** Allows a trainer to approve a pending booking request for a court they manage.
*   **Authentication:** Required (JWT Access Token for Trainer role)
*   **Path Parameters:**
    *   `booking_id`: integer (required) - The ID of the booking to approve.
*   **Request Body:** `application/json` (optional)
    ```json
    {
        "trainer_notes": "string (optional, notes from the trainer)"
    }
    ```
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "Booking approved successfully",
        "booking": { // updated booking details with status "approved" and trainer_id set }
    }
    ```
*   **Error Responses:**
    *   `400 Bad Request`: If the booking is not in `pending` state.
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `403 Forbidden`: If the user is not a trainer or does not manage the court for this booking.
    *   `404 Not Found`: If the booking does not exist.
    *   `500 Internal Server Error`: If an error occurs during database update.

### 3. Decline a Pending Booking

*   **Endpoint:** `PUT /trainer/bookings/<booking_id>/decline`
*   **Description:** Allows a trainer to decline a pending booking request for a court they manage.
*   **Authentication:** Required (JWT Access Token for Trainer role)
*   **Path Parameters:**
    *   `booking_id`: integer (required) - The ID of the booking to decline.
*   **Request Body:** `application/json` (optional)
    ```json
    {
        "trainer_notes": "string (optional, reason for declining or other notes)"
    }
    ```
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "Booking declined successfully",
        "booking": { // updated booking details with status "declined" and trainer_id set }
    }
    ```
*   **Error Responses:**
    *   `400 Bad Request`: If the booking is not in `pending` state.
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `403 Forbidden`: If the user is not a trainer or does not manage the court for this booking.
    *   `404 Not Found`: If the booking does not exist.
    *   `500 Internal Server Error`: If an error occurs during database update.




## Messaging Endpoints (`/messages`)

These endpoints handle real-time chat between users.

### 1. Get User's Chat List

*   **Endpoint:** `GET /messages/chats`
*   **Description:** Retrieves a list of chats for the authenticated user, showing the latest message for each chat.
*   **Authentication:** Required (JWT Access Token)
*   **Success Response:** `200 OK`
    ```json
    {
        "chats": [
            {
                "other_user_id": "integer",
                "other_user_full_name": "string",
                "last_message": {
                    "id": "integer",
                    "sender_id": "integer",
                    "receiver_id": "integer",
                    "content": "string",
                    "timestamp": "datetime_string",
                    "is_read": "boolean"
                },
                "unread_count": "integer"
            }
            // ... more chats
        ]
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.

### 2. Get Message History with Another User

*   **Endpoint:** `GET /messages/chats/<other_user_id>`
*   **Description:** Retrieves the message history between the authenticated user and another specified user.
*   **Authentication:** Required (JWT Access Token)
*   **Path Parameters:**
    *   `other_user_id`: integer (required) - The ID of the other user in the chat.
*   **Query Parameters:**
    *   `page`: integer (optional, default: 1) - For pagination.
    *   `per_page`: integer (optional, default: 20) - Number of messages per page.
*   **Success Response:** `200 OK`
    ```json
    {
        "messages": [
            {
                "id": "integer",
                "sender_id": "integer",
                "receiver_id": "integer",
                "content": "string",
                "timestamp": "datetime_string",
                "is_read": "boolean"
            }
            // ... more messages, typically in reverse chronological order
        ],
        "total_pages": "integer",
        "current_page": "integer",
        "total_messages": "integer"
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `404 Not Found`: If the other user does not exist.

### 3. Send a Message (Handled by SocketIO)

*   Sending messages is primarily handled via SocketIO events. See "Real-Time Events (SocketIO)" section.
*   When a message is sent via SocketIO, it is persisted in the database and then broadcasted.

## Notification Endpoints (`/notifications`)

### 1. Get User Notifications

*   **Endpoint:** `GET /notifications`
*   **Description:** Retrieves notifications for the authenticated user.
*   **Authentication:** Required (JWT Access Token)
*   **Query Parameters:**
    *   `unread_only`: boolean (optional, default: `false`) - If true, returns only unread notifications.
    *   `page`: integer (optional, default: 1) - For pagination.
    *   `per_page`: integer (optional, default: 10) - Number of notifications per page.
*   **Success Response:** `200 OK`
    ```json
    {
        "notifications": [
            {
                "id": "integer",
                "user_id": "integer",
                "message": "string",
                "type": "string (e.g., booking_approved, new_message, waitlist_slot_available)",
                "related_id": "integer (optional, e.g., booking_id, chat_user_id)",
                "is_read": "boolean",
                "created_at": "datetime_string"
            }
            // ... more notifications
        ],
        "total_pages": "integer",
        "current_page": "integer",
        "total_notifications": "integer"
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.

### 2. Mark Notification as Read

*   **Endpoint:** `PUT /notifications/<notification_id>/read`
*   **Description:** Marks a specific notification as read.
*   **Authentication:** Required (JWT Access Token)
*   **Path Parameters:**
    *   `notification_id`: integer (required) - The ID of the notification to mark as read.
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "Notification marked as read",
        "notification": { // updated notification details }
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `403 Forbidden`: If the notification does not belong to the user.
    *   `404 Not Found`: If the notification does not exist.

### 3. Mark All Notifications as Read

*   **Endpoint:** `PUT /notifications/read-all`
*   **Description:** Marks all unread notifications for the authenticated user as read.
*   **Authentication:** Required (JWT Access Token)
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "All notifications marked as read"
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.

## Waitlist Endpoints (`/waitlist`)

### 1. Add to Waitlist

*   **Endpoint:** `POST /waitlist`
*   **Description:** Allows a player to add themselves to the waitlist for a specific court and time slot if it's fully booked.
*   **Authentication:** Required (JWT Access Token for Player role)
*   **Request Body:** `application/json`
    ```json
    {
        "court_id": "integer (required)",
        "date": "string (required, YYYY-MM-DD)",
        "time_slot": "string (required, e.g., 14:00-15:00 - specific format TBD based on how slots are defined)"
    }
    ```
*   **Success Response:** `201 Created`
    ```json
    {
        "message": "Successfully added to waitlist",
        "waitlist_entry": {
            "id": "integer",
            "user_id": "integer",
            "court_id": "integer",
            "date": "string",
            "time_slot": "string",
            "status": "string (active)",
            "created_at": "datetime_string"
        }
    }
    ```
*   **Error Responses:**
    *   `400 Bad Request`: If the slot is not actually full, or invalid slot details.
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `403 Forbidden`: If the user is not a player.
    *   `404 Not Found`: If the court does not exist.
    *   `409 Conflict`: If the user is already on the waitlist for this slot.
    *   `422 Unprocessable Entity`: If input validation fails.

### 2. View User's Waitlist Entries

*   **Endpoint:** `GET /waitlist`
*   **Description:** Retrieves active waitlist entries for the authenticated user.
*   **Authentication:** Required (JWT Access Token)
*   **Success Response:** `200 OK`
    ```json
    {
        "waitlist_entries": [
            {
                "id": "integer",
                "user_id": "integer",
                "court_id": "integer",
                "court_name": "string",
                "date": "string",
                "time_slot": "string",
                "status": "string (active)",
                "created_at": "datetime_string"
            }
            // ... more entries
        ]
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.

### 3. Remove from Waitlist

*   **Endpoint:** `DELETE /waitlist/<entry_id>`
*   **Description:** Allows a player to remove themselves from a waitlist entry.
*   **Authentication:** Required (JWT Access Token for Player role)
*   **Path Parameters:**
    *   `entry_id`: integer (required) - The ID of the waitlist entry to remove.
*   **Success Response:** `200 OK`
    ```json
    {
        "message": "Successfully removed from waitlist"
    }
    ```
*   **Error Responses:**
    *   `401 Unauthorized`: If token is missing or invalid.
    *   `403 Forbidden`: If the user does not own this waitlist entry.
    *   `404 Not Found`: If the waitlist entry does not exist.




## Real-Time Events (SocketIO)

The application uses SocketIO for real-time communication, primarily for messaging and notifications.

### Namespaces

*   **`/chat`**: Used for real-time messaging between users.
*   **`/notifications`**: Used for broadcasting real-time notifications to users.

### Chat Namespace (`/chat`)

#### Connecting

*   Clients should connect to the `/chat` namespace after successful authentication.
*   The server will automatically place the connected user into a room identified by their user ID (e.g., `user_<user_id>`). This room is used for direct messaging and notifications.

#### Emitted Events (Server to Client)

1.  **`new_message`**
    *   **Description:** Emitted to a user (in their specific room `user_<receiver_id>`) when they receive a new chat message.
    *   **Payload:**
        ```json
        {
            "id": "integer (message_id)",
            "sender_id": "integer",
            "sender_full_name": "string",
            "receiver_id": "integer",
            "content": "string",
            "timestamp": "datetime_string"
        }
        ```

2.  **`message_sent_confirmation`** (Optional, if implemented for sender feedback)
    *   **Description:** Emitted back to the sender to confirm their message was successfully processed and stored.
    *   **Payload:** Same as `new_message` payload, confirming the sent message details.

3.  **`error`**
    *   **Description:** Emitted if an error occurs during a SocketIO operation related to chat.
    *   **Payload:**
        ```json
        {
            "message": "string (error description)"
        }
        ```

#### Received Events (Client to Server)

1.  **`send_message`**
    *   **Description:** Sent by a client when a user sends a new chat message.
    *   **Payload:**
        ```json
        {
            "receiver_id": "integer (ID of the message recipient)",
            "content": "string (message text)"
        }
        ```
    *   **Server Action:** The server will:
        1.  Authenticate the sender (implicitly via the SocketIO session linked to the JWT).
        2.  Validate the payload.
        3.  Store the message in the database.
        4.  Emit the `new_message` event to the recipient's room (`user_<receiver_id>`).
        5.  Optionally, emit `message_sent_confirmation` back to the sender.
        6.  Create a `new_message` type notification for the recipient.

2.  **`mark_messages_as_read`** (Optional, if implementing read receipts via SocketIO)
    *   **Description:** Sent by a client when a user has viewed messages from another user.
    *   **Payload:**
        ```json
        {
            "chat_partner_id": "integer (ID of the other user in the chat whose messages were read)"
        }
        ```
    *   **Server Action:** The server would update the `is_read` status of the relevant messages in the database.

### Notifications Namespace (`/notifications`)

#### Connecting

*   Clients should connect to the `/notifications` namespace after successful authentication.
*   The server will use the user-specific room (`user_<user_id>`) established during the initial connection (or chat connection) to send targeted notifications.

#### Emitted Events (Server to Client)

1.  **`new_notification`**
    *   **Description:** Emitted to a user (in their specific room `user_<user_id>`) when a new notification is generated for them.
    *   **Payload:**
        ```json
        {
            "id": "integer (notification_id)",
            "message": "string (notification text)",
            "type": "string (e.g., booking_approved, new_message, waitlist_slot_available)",
            "related_id": "integer (optional, e.g., booking_id, chat_user_id)",
            "created_at": "datetime_string"
        }
        ```
    *   **Trigger Actions:** This event is triggered by various backend actions, such as:
        *   A booking being approved or declined by a trainer.
        *   Receiving a new chat message.
        *   A slot becoming available from a waitlist they are on.
        *   Admin announcements (if implemented).

2.  **`all_notifications_read_update`** (Optional)
    *   **Description:** Emitted if the client needs a real-time confirmation that all their notifications were marked as read (e.g., to update UI across multiple devices).
    *   **Payload:** None, or a simple confirmation message.

This concludes the API documentation.

