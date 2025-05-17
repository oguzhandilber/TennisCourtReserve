# CourtReserve Backend - Testing Todo

This document outlines the testing tasks for the CourtReserve backend implementation.

## Phase 1: Initial Setup & Basic Endpoint Testing

*   [ ] **Database & Migrations:**
    *   [X] Configure backend to use SQLite for local development.
    *   [X] Initialize Flask-Migrate.
    *   [X] Generate initial migration script for all models.
    *   [X] Apply migrations to create SQLite database schema.
*   [X] **Data Seeding Mechanism:**
    *   [X] Implement a Flask CLI command or a utility function to seed initial data (e.g., a trainer user, a sample court).
    *   [X] Run the seeding mechanism to populate the database for testing.
*   [ ] **Authentication Endpoints (`/auth`):
    *   [ ] Test user registration (`POST /auth/register`) for a new player.
    *   [ ] Test user login (`POST /auth/login`) with correct credentials.
    *   [ ] Test user login with incorrect credentials.
    *   [ ] Test token refresh (`POST /auth/refresh`).
*   [ ] **User Profile Endpoints (`/users`):
    *   [ ] Test getting current user profile (`GET /users/me`).
    *   [ ] Test updating current user profile (`PUT /users/me`).
*   [ ] **Court Endpoints (`/courts`):
    *   [ ] Test listing active courts (`GET /courts`) - should show seeded court.
    *   [ ] Test getting details for a specific court (`GET /courts/<court_id>`).
    *   [ ] Test getting court availability (`GET /courts/<court_id>/availability?date=YYYY-MM-DD`).

## Phase 2: Core Flow Testing

*   [ ] **Booking Flow (Player Perspective):**
    *   [ ] Player requests a booking for an available slot (`POST /bookings`).
    *   [ ] Player views their list of bookings (`GET /bookings`).
    *   [ ] Player views details of a specific booking (`GET /bookings/<booking_id>`).
    *   [ ] Player attempts to book an already booked/pending slot (should fail).
    *   [ ] Player attempts to book more than 20 pending slots (should fail).
    *   [ ] Player cancels a pending booking (`PUT /bookings/<booking_id>/cancel`).
    *   [ ] Player cancels an approved booking (`PUT /bookings/<booking_id>/cancel`).
*   [ ] **Trainer Approval Flow (Trainer Perspective):**
    *   [ ] Login as the seeded trainer user.
    *   [ ] Trainer views pending booking requests for their managed courts (`GET /trainer/bookings?status=pending`).
    *   [ ] Trainer approves a pending booking (`PUT /trainer/bookings/<booking_id>/approve`).
    *   [ ] Trainer declines a pending booking (`PUT /trainer/bookings/<booking_id>/decline`).
*   [ ] **Messaging Flow (Real-time with SocketIO):**
    *   [ ] Test retrieving chat list for a user (`GET /messages/chats`).
    *   [ ] Test retrieving message history between two users (`GET /messages/chats/<other_user_id>`).
    *   [ ] Simulate SocketIO connection for chat (`connect` event on `/chat` namespace).
    *   [ ] Simulate sending a message via SocketIO (`send_message` event).
    *   [ ] Verify message is stored in the database.
    *   [ ] Verify `new_message` event is emitted to the receiver's room.
    *   [ ] Verify notification is created for the new message.
*   [ ] **Notifications Flow (Real-time with SocketIO):**
    *   [ ] Test retrieving user notifications (`GET /notifications`).
    *   [ ] Test marking a notification as read (`PUT /notifications/<notification_id>/read`).
    *   [ ] Test marking all notifications as read (`PUT /notifications/read-all`).
    *   [ ] Simulate SocketIO connection for notifications (`connect` event on `/notifications` namespace).
    *   [ ] Verify `new_notification` event is emitted when relevant actions occur (e.g., booking approved/declined, new message).
*   [ ] **Waitlist Flow:**
    *   [ ] Player adds themselves to a waitlist for a booked slot (`POST /waitlist`).
    *   [ ] Player views their active waitlist entries (`GET /waitlist`).
    *   [ ] Player removes themselves from a waitlist (`DELETE /waitlist/<entry_id>`).
    *   [ ] Simulate a booking cancellation that opens a waitlisted slot.
    *   [ ] Verify waitlisted user is notified (SocketIO event and Notification model).

## Phase 3: Edge Cases & Robustness

*   [ ] Test endpoints with invalid input data (missing fields, incorrect formats).
*   [ ] Test endpoints with unauthorized access attempts.
*   [ ] Verify proper error handling and status codes.
*   [ ] Check for concurrency issues if possible (more advanced).

## Documentation
*   [ ] Document the SQLite fallback and any implications for deployment.

