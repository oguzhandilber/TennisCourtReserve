# Tennis Project Analysis and Development Strategy

## 1. Introduction

This document provides an analysis of the current state of the TennisCourtReserve project based on a review of its backend and frontend files. It identifies implemented features, assesses the correctness of the logic, and proposes a strategy for further development and improvement.

## 2. Current State Analysis

The project is structured with a Python/Flask backend and an HTML/CSS/JavaScript frontend.

### 2.1. Backend Analysis

Based on the review of files in `backend/src/models/` and `backend/src/routes/`, the backend has a solid foundation with the following features implemented at the database model and API route levels:

*   **User Management:**
    *   Models for users with roles (`player`, `tutor`, `court_responsible`, `admin`).
    *   Backend routes for user registration (`/api/auth/register`), login (`/api/auth/login`), and token refresh (`/api/auth/refresh`).
    *   Backend routes for fetching (`GET /api/users/me`) and updating (`PUT /api/users/me`) the authenticated user's profile.
    *   Admin-protected CRUD routes for managing all users (`GET /api/users`, `GET /api/users/<user_id>`, `PUT /api/users/<user_id>`, `DELETE /api/users/<user_id>`).
*   **Court Management:**
    *   Model for courts with details like name, location, type, operating hours, and status.
    *   Backend routes for listing courts (`/api/courts`) with filtering (search, surface type, setting) and getting court details (`/api/courts/<int:court_id>`).
    *   Backend route for getting court availability for a specific date (`/api/courts/<int:court_id>/availability`), which checks against existing bookings.
*   **Booking System:**
    *   Model for bookings with statuses (`pending_approval`, `confirmed`, `rejected`, `cancelled`, `completed`).
    *   Backend routes for requesting a new booking (`/api/bookings/request`), retrieving user bookings (`/api/bookings`), and retrieving court bookings (for authorized users) (`/api/bookings/court/<int:court_id>`).
    *   Backend routes for approving (`/api/bookings/<int:booking_id>/approve`), rejecting (`/api/bookings/<int:booking_id>/reject`), and canceling (`/api/bookings/<int:booking_id>/cancel`) bookings with authorization checks and a 1-hour cancellation policy implemented for users.
*   **Court Following:**
    *   Model (`CourtFollower`) and backend routes (`/api/courts/<int:court_id>/follow`, `/api/courts/<int:court_id>/unfollow`) for users to follow courts.
*   **Notifications:**
    *   Model for notifications with type, content, and read status.
    *   Backend routes for getting user notifications (`/api/notifications`), marking individual notifications as read (`/api/notifications/<int:notification_id>/read`), and marking all as read (`/api/notifications/read-all`).
    *   Helper functions for creating and sending real-time notifications via Socket.IO. Notification logic for booking approval/rejection by trainers is now included.
*   **Messaging:**
    *   Model for messages.
    *   Backend routes and Socket.IO event handlers for retrieving chat lists (`/api/messages/chats`), message history (`/api/messages/chats/<int:other_user_id>`), and sending/receiving messages in real-time.
*   **Waitlist:**
    *   Model (`WaitlistEntry`) exists, indicating intent for a waitlist feature. Backend routes for adding to (`/api/waitlist`), retrieving user entries (`/api/waitlist`), and removing entries (`/api/waitlist/<int:entry_id>`) have been added. Logic to notify waitlisted users upon booking cancellation/rejection is also implemented in booking routes.

### 2.2. Frontend Analysis

Based on the review of the main HTML files in `frontend/`, the frontend provides the user interface and interacts with the backend API:

*   **Landing Page (`landing_page.html`):** Basic entry point with an overview and link to authentication.
*   **Signup/Login Page (`signup_login.html`):** Implements user registration and login forms and interacts with the backend `/api/auth` endpoints. Stores tokens in local storage and redirects on success.
*   **Dashboard (`dashboard.html`):** Displays user info, fetches and renders upcoming bookings and unread notification count from backend APIs (`/api/bookings`, `/api/notifications`). Includes placeholders for other features and a bottom navigation bar.
*   **Court Listing Page (`court_listing.html`):** Fetches and displays a list of courts from `/api/courts`, with UI and JavaScript logic to apply search and advanced filters that are sent to the backend. The "Next available" placeholder has been removed, directing users to the detail page for availability. Links to court detail pages.
*   **Court Detail Page (`court_detail.html`):** Fetches court details (`/api/courts/<int:court_id>`) and availability (`/api/courts/<int:court_id>/availability`). Implements a calendar for date selection and displays time slots based on availability status. Includes a modal for submitting booking requests to `/api/bookings/request`. Implements UI and logic for following/unfollowing a court. Includes a "Join Waitlist" button for unavailable slots that interacts with the backend `/api/waitlist` endpoint. Includes placeholders for trainer information.
*   **Trainer Portal (`trainer_portal.html`):** Provides a UI for court responsible users to view and manage booking requests, including fetching requests from the backend (`/api/trainer/bookings`) and sending approval/rejection actions.
*   **Messages Page (`messages.html`):** Initial implementation of the messaging frontend, including UI structure for chat lists and conversations, and JavaScript logic for fetching chats, displaying messages, sending messages via WebSocket, and handling new messages.
*   **My Waitlist Page (`waitlist.html`):** Initial implementation of the waitlist frontend, including UI structure for displaying waitlist entries and JavaScript logic for fetching and removing entries via the backend.
*   **Profile Page (`profile.html`):** Fetches and displays user profile information from `/api/users/me`. Includes an "Edit Profile" modal and JavaScript logic to update user details via the `PUT /api/users/me` endpoint.

### 2.3. Correctness Assessment

*   **Backend Logic:** The backend models and core route logic for authentication, courts, bookings, following, notifications, messaging, and user profiles appear largely correct and well-structured, supporting the intended features. Authorization checks for role-specific actions (like booking approval/rejection) are present. The 1-hour cancellation policy is implemented.
*   **Frontend Logic:** The frontend correctly interacts with the backend authentication, court listing, court detail, trainer portal, and profile APIs. The `court_detail.html` has made significant progress in dynamically fetching availability and submitting booking requests. The `fetchWithAuth` helper for handling authentication tokens is a good practice.
*   **Identified Inconsistencies/Areas for Improvement:**
    *   The inconsistency in notification parameter names in the `create_notification` helper function in `backend/src/routes/bookings_bp.py` has been addressed.
    *   The generic user CRUD routes in `backend/src/routes/user.py` have been reviewed and updated with admin role protection.
    *   The frontend has numerous placeholders, indicating that while the backend supports many features, the corresponding frontend UI and logic are not yet fully implemented (e.g., full calendar view, dedicated bookings page, messages page, advanced filtering on court listing).
    *   Real-time notification display and interaction (beyond just showing the count) need to be implemented in the frontend.
    *   The messaging UI and real-time updates need to be fully built out in the frontend.

## 3. Development Strategy and Future Improvements

The primary focus should be on completing the frontend implementation for the features already supported by the backend and then building out the remaining features like the waitlist.

Here is a proposed strategy:

1.  **Complete Core Booking Workflow (Frontend):**
    *   Refine the display of time slots on `court_detail.html` to clearly show 'available', 'booked', and 'pending_approval' states.
    *   Thoroughly test the booking request submission and ensure appropriate user feedback (toasts, UI updates).

2.  **Implement Booking Approval/Rejection UI:** This step is largely complete with the existing implementation in `trainer_portal.html`, which fetches and displays requests and sends approval/rejection actions to the backend. Further refinement and testing may be needed.

3.  **Implement Booking Cancellation UI:** This step is largely complete with the existing implementation in `my_bookings.html`, which fetches and displays user bookings and includes logic for cancellation via the backend API, including a frontend check for the 1-hour policy. Further refinement and testing may be needed.

4.  **Integrate Real-time Notifications (Frontend):** This step is largely complete with the existing implementation in `notifications.html`, which includes WebSocket integration, fetching and rendering notifications, marking as read, and handling real-time updates. Further refinement and testing may be needed.

5.  **Develop Messaging Feature (Frontend & Backend):** Initial frontend implementation in `messages.html` is complete, including UI and core logic for chat lists, message display, sending, and receiving via WebSocket. Further backend route/Socket.IO handler completion and frontend refinement are needed.

6.  **Implement Waitlist Feature (Backend & Frontend):** Backend routes for adding to, retrieving user entries, and removing entries are implemented, including logic to notify waitlisted users when a booking is rejected or cancelled. Frontend UI for joining the waitlist is added to `court_detail.html`. A dedicated frontend page (`waitlist.html`) for viewing user waitlist entries is created, including logic for removing entries via the backend API.

7.  **Enhance UI/UX:**
    *   Replace all placeholder elements and improve the overall visual design and user experience.
    *   Implement the interactive calendar view (currently blocked by backend capabilities for month-wide availability data).
    *   Complete the user profile page (largely done with view and edit functionality).
    *   Add advanced filtering functionality on the court listing page that interacts with the backend (Frontend and Backend for basic filters implemented).

8.  **Refine Backend Logic:**
    *   Address the notification parameter inconsistency (addressed for `bookings_bp.py`).
    *   Ensure consistent notification triggering across all relevant actions (addressed for `trainer.py`).
    *   Review and potentially refactor the generic user CRUD routes for admin capabilities and to avoid conflicts (addressed by adding admin protection).
    *   Add more comprehensive backend validation and error handling (enhanced for booking creation).

9.  **Testing:**
    *   Implement automated tests (unit, integration, end-to-end) to ensure the stability and correctness of the application as new features are added and existing ones are refined.

## 4. Conclusion

The TennisCourtReserve project has a strong backend foundation for its core features. The frontend is progressing well in integrating with the backend, particularly for the booking workflow. The key to moving forward is to complete the frontend implementation for the existing backend features and then build out the remaining planned features like the waitlist. Following the outlined strategy will help guide the development process effectively.