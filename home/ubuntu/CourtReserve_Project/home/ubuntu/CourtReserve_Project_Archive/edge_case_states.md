# CourtReserve - Edge Case State Documentation

This document outlines key edge-case states for the prototyped user flows (Booking a Court and Trainer Approval) in the CourtReserve application. Handling these gracefully is crucial for a good user experience.

## 1. Booking a Court Flow Edge Cases

### 1.1 Court Listing Page (`court_listing.html`)

*   **No Courts Available / No Search Results:**
    *   **Scenario:** User's search criteria (text search, filters) yield no matching courts, or there are genuinely no courts in the system/area.
    *   **UI State:**
        *   The `loading-indicator` (skeleton screens) is hidden.
        *   The `court-list` div is empty or hidden.
        *   The `no-results` message (already in prototype HTML, initially hidden) is displayed prominently.
        *   Message: "No courts found matching your criteria. Try adjusting your filters or search term." or "No courts available in your area at the moment."
        *   **Action:** Encourage user to broaden search, clear filters, or check back later.

*   **API Error / Failed to Load Courts:**
    *   **Scenario:** The backend call to fetch court listings fails.
    *   **UI State:**
        *   Display an error message (e.g., using a toast notification or an inline message within the court list area).
        *   Message: "Oops! We couldn't load court information right now. Please try again in a few moments."
        *   **Action:** Provide a "Retry" button if feasible, or suggest refreshing the page.

### 1.2 Court Detail Page (`court_detail.html`)

*   **Court Information Not Found:**
    *   **Scenario:** User navigates to a court detail page with an invalid `courtId` or the court data fails to load.
    *   **UI State:**
        *   Display a clear error message instead of the court content.
        *   Message: "Sorry, we couldn't find details for this court." or "This court is no longer available."
        *   **Action:** Provide a button to go back to the Court Listing page.

*   **No Available Slots for Selected Date:**
    *   **Scenario:** User selects a date in the calendar for which the `currentCrtData.slots[dateStr]` is empty or undefined.
    *   **UI State (as prototyped):**
        *   The `time-slots-container` remains hidden or shows a message like "No available slots for [Selected Date]. Please try another date."
        *   The `booking-action-bar` remains hidden.

*   **Selected Slot Becomes Unavailable (Booking Conflict):**
    *   **Scenario:** While the user is on the Court Detail page, or just before they confirm the booking, the selected time slot is booked by another user.
    *   **UI State (on attempting to book or on data refresh):**
        *   When the user clicks "Request Booking" or when the page data refreshes (if live updates were implemented):
            *   The booking modal should not proceed, or if it does, the confirmation step should fail.
            *   Display a clear message (toast or modal update): "Sorry, this slot ([Date], [Time]) is no longer available. Please select another time."
            *   The calendar/time slot UI should refresh to show the slot as booked.
            *   The `booking-action-bar` should hide or update to reflect no valid slot is selected.
        *   **Action:** User needs to select a new available slot.

*   **Booking Request Fails (API Error):**
    *   **Scenario:** User submits a booking request, but the API call to the backend fails.
    *   **UI State (after clicking "Send Request" in modal):**
        *   The booking confirmation modal remains open or reopens with an error message.
        *   Display an error message: "We couldn't process your booking request at this time. Please try again."
        *   The "Send Request" button might show a temporary disabled/loading state during the attempt.
        *   **Action:** Allow user to retry the request or cancel.

### 1.3 Sign Up / Log In Page (`signup_login.html`)

*   **Email Already Exists (Sign Up):**
    *   **Scenario:** User tries to sign up with an email address that is already registered.
    *   **UI State:**
        *   Display an inline error message below the email field or a general form error.
        *   Message: "This email address is already registered. Please log in or use a different email."
        *   **Action:** Highlight the email field. Suggest logging in.

*   **Passwords Do Not Match (Sign Up):**
    *   **Scenario:** User's password and confirm password fields do not match.
    *   **UI State (as prototyped via alert, ideally inline):**
        *   Display an inline error message below the confirm password field.
        *   Message: "Passwords do not match. Please re-enter."
        *   **Action:** Clear both password fields or just the confirm password field.

*   **Invalid Credentials (Log In):**
    *   **Scenario:** User enters an incorrect email/password combination.
    *   **UI State:**
        *   Display a general form error message.
        *   Message: "Invalid email or password. Please try again or reset your password."
        *   **Action:** Do not specifically indicate whether the email or password was wrong for security.

*   **Account Locked / Disabled:**
    *   **Scenario:** User attempts to log in to an account that has been locked or disabled by an admin.
    *   **UI State:**
        *   Display a general form error message.
        *   Message: "Your account has been temporarily locked. Please contact support for assistance."

## 2. Trainer Approval Flow Edge Cases

### 2.1 Trainer Portal (`trainer_portal.html`)

*   **No Pending Requests (or other filtered states):**
    *   **Scenario:** Trainer navigates to the portal or applies a filter, and there are no requests matching the criteria.
    *   **UI State (as prototyped):**
        *   The `request-list-section` shows the `no-requests-message`.
        *   Message: "No requests match the current filter." or "You have no pending booking requests right now."

*   **Request Already Processed (Race Condition):**
    *   **Scenario:** Two trainers are viewing the same pending request. One trainer approves/declines it. The other trainer attempts to process it shortly after.
    *   **UI State (on attempting to approve/decline):**
        *   The action (approve/decline) should fail gracefully.
        *   Display a toast notification: "This request has already been processed by another trainer."
        *   The request item in the list should refresh to show its current (already processed) status.
        *   The action buttons for that item should be removed or disabled.

*   **API Error on Processing Request:**
    *   **Scenario:** Trainer attempts to approve/decline a request, but the backend API call fails.
    *   **UI State:**
        *   The request item remains in its current state (e.g., pending).
        *   Display a toast notification: "Failed to update request status. Please try again."
        *   The approve/decline buttons remain active to allow retry.

*   **Failed to Load Requests:**
    *   **Scenario:** The initial load of requests for the trainer portal fails.
    *   **UI State:**
        *   Display an error message within the main content area.
        *   Message: "Could not load booking requests. Please check your connection and try again."
        *   **Action:** Provide a "Retry" button.

## 3. General Edge Cases (Applicable to Multiple Pages)

*   **Network Offline:**
    *   **Scenario:** User loses internet connectivity while using the app.
    *   **UI State:**
        *   Any action requiring network communication (fetching data, submitting forms) should fail.
        *   Display a global offline notification (e.g., a banner at the top/bottom of the screen or a toast).
        *   Message: "You appear to be offline. Please check your internet connection."
        *   Disable buttons that require network access or show a loading state that doesn't resolve until connection is back.
        *   **Action:** App could attempt to retry automatically when connection is restored, or prompt user to retry.

*   **Slow Network Connection:**
    *   **Scenario:** Network is slow, API responses are delayed.
    *   **UI State:**
        *   Use loading indicators (skeletons, spinners on buttons) clearly to show that the app is working.
        *   Avoid multiple submissions by disabling buttons after the first click until a response is received.
        *   Consider timeouts for operations and inform the user if an operation is taking too long, offering a chance to cancel or wait.

*   **Expired Session / Authentication Required:**
    *   **Scenario:** User's session expires, or they attempt an action that requires authentication without being logged in.
    *   **UI State:**
        *   Redirect user to the Log In page.
        *   Display a message (on the Log In page or as a toast before redirect): "Your session has expired. Please log in again." or "You need to be logged in to perform this action."
        *   Attempt to save user's current state or intended action to restore after successful login (e.g., redirect back to the page they were on).

This list covers critical edge cases. Each would ideally be accompanied by visual mockups showing the UI state in a full design specification.

