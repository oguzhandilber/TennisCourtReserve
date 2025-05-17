# User Flow: Booking a Court

This document outlines the user flow for booking a tennis court on the CourtReserve platform.

**Actor:** Player (new or returning user)

**Goal:** Find and request a booking for a tennis court.

**Pre-conditions:**
*   User has access to a device with an internet browser.

**Main Success Scenario:**

1.  **Landing Page & Initiation:**
    *   User lands on the CourtReserve homepage.
    *   Homepage displays a hero section with a clear "Book a Court" call-to-action (CTA).
    *   User clicks the "Book a Court" CTA or a navigation link to view courts.

2.  **Authentication (if not logged in):**
    *   If the user is not logged in, they are redirected to the Sign Up / Log In page.
    *   **New User (Sign Up):**
        *   User chooses to sign up (e.g., with email or social OAuth - Google, Facebook).
        *   User provides necessary details (name, email, password or authenticates via OAuth).
        *   User successfully signs up and is logged in.
    *   **Existing User (Log In):**
        *   User chooses to log in.
        *   User provides credentials (email/password) or uses social OAuth.
        *   User successfully logs in.
    *   Upon successful login/signup, the user is typically redirected to the Dashboard or the Court Listing page (depending on the entry point or previous action).

3.  **Court Discovery (Court Listing Page):**
    *   User navigates to or is on the Court Listing page.
    *   The page displays a grid of available courts.
    *   Each court card shows a thumbnail image, name/number, surface type (e.g., Clay, Hard, Grass), indoor/outdoor status, and the next available time slot (e.g., "Available today at 3:00 PM").
    *   User can use filters (if implemented at this stage, e.g., surface type, indoor/outdoor - though advanced filters are for later).
    *   User browses the list and identifies a suitable court.
    *   User clicks on a court card to view more details.

4.  **Court Details & Availability (Court Detail Page):**
    *   User is on the Court Detail page for the selected court.
    *   Page displays:
        *   Larger image(s) of the court.
        *   Court name/number, surface type, indoor/outdoor, capacity, price (if applicable).
        *   Assigned trainer(s) for the court (if any, with links to their profiles).
        *   A schedule/calendar view showing available hours/slots for booking (e.g., daily, weekly view).
        *   Clear visual distinction between available, booked, and pending slots.
    *   User selects a desired available date and time slot.

5.  **Booking Request:**
    *   After selecting a slot, the "Request Booking" button becomes active or is already visible.
    *   User clicks the "Request Booking" button.
    *   A confirmation modal or section appears, summarizing the selected court, date, time, and any associated fees (if applicable).
    *   User might be able to add a short note to the trainer (optional).
    *   User confirms the booking request.

6.  **Confirmation & Next Steps:**
    *   System records the booking request as "Pending Approval".
    *   User receives an on-screen confirmation message (e.g., "Booking request sent! You will be notified once the trainer approves.").
    *   The booked slot on the user's dashboard calendar now shows as "Pending Approval".
    *   A notification is sent to the assigned trainer(s) about the new booking request.

**Post-conditions:**
*   Booking request is submitted and awaiting trainer approval.
*   User is informed about the status of their request.
*   Trainer is notified of the pending request.

**Alternative Flows / Edge Cases:**

*   **No Courts Available:** If no courts match filters or are available, a message informs the user.
*   **Selected Slot Becomes Unavailable:** If the chosen slot is booked by another user just before confirmation, the user is notified and asked to select another slot.
*   **Login/Sign Up Failure:** User is shown an error message and can retry.
*   **User Navigates Away:** If the user navigates away during the booking process, their selections might be lost unless a save/draft feature is implemented (out of scope for initial MVP unless specified).
*   **Court has no assigned trainer:** The booking might be auto-approved (system rule to be defined) or go to a general admin pool for approval.

--- 
This flow will be used as a basis for creating wireframes for the relevant pages.
