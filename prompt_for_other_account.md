# CourtReserve Project: Comprehensive Task Prompt

## Project Overview

The CourtReserve project is a tennis court reservation system that allows different types of users (players, tutors, and court responsibles) to view courts, make booking requests, approve/reject bookings, and receive notifications. The project consists of a Python/Flask backend and HTML/CSS/JavaScript frontend.

## Current Project State

### What's Working
- Backend database models for users, courts, and bookings
- User authentication system (signup and login functionality)
- Court creation and management
- User roles (player, tutor, court_responsible)
- Basic UI navigation between pages
- Login/signup UI (after fixing a tab switching bug)

### Critical Blocker
The main issue preventing full functionality is that the frontend booking workflow is **entirely static**:
- Court availability data is hardcoded in JavaScript, not fetched from the backend
- The "Request Booking" functionality doesn't actually submit data to any backend API
- This prevents testing the entire reservation, approval, and cancellation workflow

### Progress Made So Far
- Fixed the UI bug in signup_login.html where clicking the "Log In" tab didn't switch to the login form
- Successfully created the database with proper user types and courts via the seed.py script
- Created a detailed API design document (api_design_v2.md) for implementing the dynamic booking workflow
- Identified all necessary backend endpoints and frontend changes needed

## Required Features to Implement

1. **Dynamic Court Availability**
   - Backend API endpoint to provide real-time court availability
   - Frontend to fetch and display this dynamic data

2. **Booking Request System**
   - Backend API to handle booking requests
   - Frontend to submit booking requests to the backend
   - Status tracking for bookings (pending, approved, rejected, cancelled)

3. **Court Following Feature**
   - Allow users to follow specific courts
   - Store these preferences in the database
   - API endpoints for follow/unfollow actions

4. **Approval Workflow**
   - Interface for court responsible users to see pending requests
   - Functionality to approve or reject booking requests

5. **Cancellation System with Policy Enforcement**
   - Allow users to cancel their bookings
   - Enforce the "cannot cancel if less than 1 hour remaining" policy
   - Backend logic to handle cancellation requests

6. **Notification System**
   - Notify users when their booking requests are approved/rejected
   - Notify users who follow a court when a slot becomes available
   - Include court name, hour info, and approval/cancellation details in notifications

## Detailed Implementation Tasks

### Backend Tasks
1. Implement the API endpoints as specified in api_design_v2.md:
   - GET /api/courts/<court_id>/availability
   - POST /api/bookings/request
   - GET /api/bookings
   - POST /api/bookings/<booking_id>/approve
   - POST /api/bookings/<booking_id>/reject
   - POST /api/bookings/<booking_id>/cancel
   - POST /api/courts/<court_id>/follow
   - POST /api/courts/<court_id>/unfollow

2. Create or update database models:
   - Add a "follows" relationship between users and courts
   - Ensure the Booking model has appropriate status fields and timestamps

3. Implement business logic:
   - 1-hour cancellation policy enforcement
   - Notification generation and storage

### Frontend Tasks
1. Modify court_detail.html to:
   - Fetch real court availability from the backend API
   - Display dynamic time slots based on API response
   - Submit actual booking requests to the backend

2. Create or update UI components:
   - Add "Follow Court" button on court detail page
   - Create a booking management interface for users
   - Create an approval interface for court responsible users
   - Add a notifications view

3. Implement frontend logic:
   - Handle booking status changes
   - Display appropriate messages based on booking status
   - Show notifications to users

### Testing Tasks
1. Test user registration and login
2. Test court following/unfollowing
3. Test the complete reservation workflow:
   - Player makes a booking request
   - Court responsible approves the request
   - Verify notifications are sent
   - Test cancellation (both within and outside the 1-hour window)

## Project Structure
The main project files are located in:
- Backend: `/project_files/home/ubuntu/CourtReserve_Project/home/ubuntu/CourtReserve_Project_Archive/CourtReserve_Backend/`
- Frontend: `/project_files/home/ubuntu/CourtReserve_Project/home/ubuntu/CourtReserve_Project_Archive/courtreserve_prototypes/`

Key documentation:
- Project Report: `/project_report.md`
- API Design: `/api_design_v2.md`
- Todo List: `/todo.md`

## Testing Instructions
1. Run the backend server:
   ```
   cd /path/to/CourtReserve_Backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python src/app.py
   ```

2. Run the frontend server:
   ```
   cd /path/to/courtreserve_prototypes
   python -m http.server 8080
   ```

3. Test with the following users (all with password "password123"):
   - player@example.com (Role: player)
   - tutor@example.com (Role: tutor)
   - responsible@example.com (Role: court_responsible)

## Next Steps
1. Implement the backend API endpoints for dynamic court availability and booking
2. Refactor the frontend to use these dynamic endpoints
3. Implement the court following feature
4. Add the approval and cancellation workflows
5. Test the complete reservation system end-to-end
6. Fix any issues found during testing

Please refer to the project_report.md and api_design_v2.md files for more detailed information on the current state and planned enhancements.
