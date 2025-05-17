# CourtReserve - Backend Architecture and Database Schema

This document outlines the proposed backend architecture, database schema, and API structure for the CourtReserve application. This design aims to support all specified functionalities, including user management, court reservations, trainer approvals, messaging, notifications, and real-time features.

## 1. Backend Architecture Overview

### 1.1. Technology Stack

*   **Web Framework:** Flask (Python) - Chosen for its flexibility, simplicity for this scale, and robust ecosystem.
*   **Database:** PostgreSQL - A powerful open-source relational database suitable for handling structured data, relationships, and ensuring data integrity. SQLite will be used for local development for ease of setup.
*   **Authentication:** JWT (JSON Web Tokens) for stateless API authentication. Social OAuth will be handled by integrating with relevant providers (e.g., Google, Facebook) and then issuing a JWT.
*   **Real-time Communication:** Flask-SocketIO - For implementing real-time features like messaging and notifications via WebSockets.
*   **API Specification:** OpenAPI (Swagger) will be used for documenting API endpoints (to be created in a later step).

### 1.2. High-Level Components

1.  **RESTful API (Flask):** The core of the backend, providing endpoints for all application functionalities.
2.  **Authentication Service:** Handles user registration, login (email/password & OAuth), session management (via JWT), and role-based access control (Player, Trainer, Admin - though Admin role is mostly for external data management for now).
3.  **Database (PostgreSQL/SQLite):** Stores all persistent data.
4.  **Real-time Service (Flask-SocketIO):** Manages WebSocket connections for instant messaging and notifications.
5.  **Background Tasks (Optional, e.g., Celery):** For handling asynchronous tasks like sending email/SMS notifications for cancellations or waitlist updates (if full SMS/email integration is pursued beyond in-app notifications).

## 2. Database Schema

The following entities and their relationships form the core of the database schema.

### 2.1. `Users`

*   `id` (SERIAL, Primary Key)
*   `email` (VARCHAR(255), Unique, Not Null)
*   `password_hash` (VARCHAR(255), Not Null) - For email/password auth.
*   `full_name` (VARCHAR(255))
*   `phone_number` (VARCHAR(50), Nullable)
*   `skill_level` (VARCHAR(50), Nullable) - e.g., Beginner, Intermediate, Advanced
*   `profile_picture_url` (VARCHAR(512), Nullable)
*   `communication_preferences` (JSONB, Nullable) - e.g., { "email_notifications": true, "sms_notifications": false }
*   `role` (VARCHAR(20), Not Null, Default: 'player') - e.g., 'player', 'trainer', 'admin'
*   `oauth_provider` (VARCHAR(50), Nullable) - e.g., 'google', 'facebook'
*   `oauth_id` (VARCHAR(255), Nullable)
*   `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)
*   `updated_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

### 2.2. `Courts`

*   `id` (SERIAL, Primary Key)
*   `name` (VARCHAR(255), Not Null)
*   `address` (VARCHAR(512), Nullable)
*   `location_coordinates` (POINT, Nullable) - For geo-location features (e.g., PostGIS extension for PostgreSQL)
*   `surface_type` (VARCHAR(50)) - e.g., 'Clay', 'Hard', 'Grass'
*   `setting` (VARCHAR(50)) - e.g., 'Indoor', 'Outdoor'
*   `thumbnail_url` (VARCHAR(512), Nullable)
*   `description` (TEXT, Nullable)
*   `operating_hours` (JSONB, Nullable) - e.g., { "monday": ["08:00", "22:00"], ... }
*   `status` (VARCHAR(20), Default: 'active') - e.g., 'active', 'maintenance', 'closed'
*   `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)
*   `updated_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

### 2.3. `Trainers` (linking Users to Courts they manage/train at)

*   `id` (SERIAL, Primary Key)
*   `user_id` (INTEGER, Foreign Key to `Users.id`, Not Null) - The user who is a trainer.
*   `bio` (TEXT, Nullable)
*   `specializations` (JSONB, Nullable) - e.g., ["Juniors", "Serve Technique"]
*   `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)
*   `updated_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

_Note: A trainer's association with specific courts they manage might be handled via a separate join table if a trainer can manage multiple courts and a court can have multiple trainers responsible for approvals._

### 2.4. `Court_Trainers` (Many-to-Many relationship between Courts and Trainers for approval rights)

*   `court_id` (INTEGER, Foreign Key to `Courts.id`, Primary Key)
*   `trainer_user_id` (INTEGER, Foreign Key to `Users.id` where `role` is 'trainer', Primary Key) - References the user who is a trainer.

### 2.5. `Bookings`

*   `id` (SERIAL, Primary Key)
*   `user_id` (INTEGER, Foreign Key to `Users.id`, Not Null) - The user who made the booking.
*   `court_id` (INTEGER, Foreign Key to `Courts.id`, Not Null)
*   `trainer_id` (INTEGER, Foreign Key to `Users.id`, Nullable) - The trainer assigned to this booking slot/court, or who approved it.
*   `start_time` (TIMESTAMP, Not Null)
*   `end_time` (TIMESTAMP, Not Null)
*   `status` (VARCHAR(20), Not Null, Default: 'pending') - e.g., 'pending', 'approved', 'declined', 'cancelled_by_user', 'cancelled_by_trainer', 'completed'
*   `user_notes` (TEXT, Nullable) - Note from player during booking request.
*   `trainer_notes` (TEXT, Nullable) - Note from trainer when approving/declining.
*   `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)
*   `updated_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

_Constraint: Ensure `start_time` < `end_time`. Ensure no overlapping approved bookings for the same court._

### 2.6. `Messages`

*   `id` (SERIAL, Primary Key)
*   `sender_id` (INTEGER, Foreign Key to `Users.id`, Not Null)
*   `receiver_id` (INTEGER, Foreign Key to `Users.id`, Not Null)
*   `booking_id` (INTEGER, Foreign Key to `Bookings.id`, Nullable) - Optional link to a booking if message is related.
*   `content` (TEXT, Not Null)
*   `sent_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)
*   `read_at` (TIMESTAMP, Nullable)

### 2.7. `Notifications`

*   `id` (SERIAL, Primary Key)
*   `user_id` (INTEGER, Foreign Key to `Users.id`, Not Null) - The recipient of the notification.
*   `type` (VARCHAR(50), Not Null) - e.g., 'booking_approved', 'booking_declined', 'booking_cancelled', 'new_message', 'waitlist_slot_available'
*   `related_entity_id` (INTEGER, Nullable) - e.g., `booking_id`, `message_id`
*   `content` (TEXT, Not Null) - The notification message.
*   `is_read` (BOOLEAN, Default: false)
*   `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

### 2.8. `Waitlist_Entries`

*   `id` (SERIAL, Primary Key)
*   `user_id` (INTEGER, Foreign Key to `Users.id`, Not Null)
*   `court_id` (INTEGER, Foreign Key to `Courts.id`, Not Null)
*   `desired_date` (DATE, Not Null)
*   `desired_start_time` (TIME, Not Null)
*   `desired_end_time` (TIME, Not Null)
*   `status` (VARCHAR(20), Default: 'active') - e.g., 'active', 'notified', 'booked', 'expired'
*   `created_at` (TIMESTAMP, Default: CURRENT_TIMESTAMP)

_Unique constraint on (`user_id`, `court_id`, `desired_date`, `desired_start_time`) to prevent duplicate entries._

## 3. API Structure Overview (High-Level)

*   `/auth`
    *   `POST /auth/register` - User registration.
    *   `POST /auth/login` - User login (email/password).
    *   `POST /auth/oauth/{provider}` - Initiate OAuth flow.
    *   `GET /auth/oauth/{provider}/callback` - OAuth callback.
    *   `POST /auth/refresh` - Refresh JWT.
    *   `POST /auth/logout` - User logout (if using token blocklist).
*   `/users`
    *   `GET /users/me` - Get current user's profile.
    *   `PUT /users/me` - Update current user's profile.
    *   `GET /users/{user_id}/profile` - Get another user's public profile (e.g., trainer).
*   `/courts`
    *   `GET /courts` - List all available courts (with filtering/searching).
    *   `GET /courts/{court_id}` - Get details of a specific court.
    *   `GET /courts/{court_id}/availability` - Get availability for a court (e.g., for a specific date range).
*   `/bookings`
    *   `POST /bookings` - Request a new booking.
    *   `GET /bookings` - List user's bookings (for players).
    *   `GET /bookings/{booking_id}` - Get details of a specific booking.
    *   `PUT /bookings/{booking_id}/cancel` - Cancel a booking (by player or trainer).
*   `/trainer/bookings` (Trainer-specific booking management)
    *   `GET /trainer/bookings` - List pending/managed bookings for a trainer.
    *   `PUT /trainer/bookings/{booking_id}/approve` - Approve a booking.
    *   `PUT /trainer/bookings/{booking_id}/decline` - Decline a booking.
*   `/messages` (Real-time via WebSockets, with REST API for history)
    *   `GET /messages/chats` - List user's chat conversations.
    *   `GET /messages/chats/{other_user_id}` - Get message history with a specific user.
    *   `POST /messages/chats/{other_user_id}` - Send a message (can also be purely WebSocket).
*   `/notifications` (Real-time via WebSockets, with REST API for history)
    *   `GET /notifications` - List user's notifications.
    *   `PUT /notifications/{notification_id}/read` - Mark notification as read.
    *   `PUT /notifications/read-all` - Mark all notifications as read.
*   `/waitlist`
    *   `POST /waitlist` - Add user to a waitlist for a specific court/slot.
    *   `DELETE /waitlist/{entry_id}` - Remove user from a waitlist.

## 4. Real-time Features Approach

*   **Flask-SocketIO:** Will be used to manage WebSocket connections.
*   **Messaging:**
    *   Clients connect to a Socket.IO namespace (e.g., `/chat`).
    *   Users join rooms based on their `user_id` or specific chat `conversation_id`.
    *   When a message is sent, the server emits it to the recipient's room/socket.
    *   Read receipts can be implemented by client emitting an event when messages are viewed, and server updating the `read_at` status in DB and notifying sender.
*   **Notifications:**
    *   Clients connect to a Socket.IO namespace (e.g., `/notifications`).
    *   Users join a room based on their `user_id`.
    *   When a relevant event occurs (e.g., booking approved, new message), the server creates a `Notification` record in the DB and emits a `new_notification` event to the user's room with the notification payload.

This architecture and schema provide a solid foundation for building the CourtReserve backend. Further details for each API endpoint (request/response bodies, specific status codes) will be defined in the API documentation phase.

