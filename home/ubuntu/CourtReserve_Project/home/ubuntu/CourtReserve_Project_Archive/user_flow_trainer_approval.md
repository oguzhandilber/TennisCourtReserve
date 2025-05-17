# User Flow: Trainer Approval

This document outlines the user flow for a trainer approving or declining a court booking request on the CourtReserve platform.

**Actor:** Trainer

**Goal:** Review and respond to pending booking requests.

**Pre-conditions:**
*   Trainer has an account on CourtReserve and is designated as a trainer for one or more courts.
*   Trainer has received a notification (in-app, email, etc.) about a new booking request or logs in to check for pending requests.
*   Trainer has access to a device with an internet browser.

**Main Success Scenario (Approval):**

1.  **Login & Access Trainer Portal:**
    *   Trainer logs into their CourtReserve account.
    *   Trainer navigates to the "Trainer Portal" or a dedicated "Booking Requests" section (e.g., via dashboard link or main navigation).

2.  **View Pending Requests (Trainer Portal):**
    *   The Trainer Portal displays a list of pending booking requests.
    *   Each request in the list shows key information:
        *   Player Name (who made the request).
        *   Court Name/Number.
        *   Requested Date and Time Slot.
        *   Time of request submission (e.g., "Received 2 hours ago").
        *   (Optional) Any note from the player.
    *   Requests are typically sorted by urgency or submission time (newest first).

3.  **Select and Review Request:**
    *   Trainer taps/clicks on a specific pending request to view its details.
    *   The request detail view might show:
        *   All information from the list view.
        *   Player's booking history (briefly, if relevant and available).
        *   Court's schedule around the requested time to check for conflicts or availability (though the system should prevent overlapping requests for the same slot if it's already booked and confirmed).
        *   Any notes from the player.

4.  **Decision - Approve:**
    *   Trainer decides to approve the request.
    *   Trainer clicks the "Approve" button associated with the request.

5.  **Confirmation of Approval:**
    *   System updates the booking status from "Pending Approval" to "Confirmed".
    *   Trainer receives an on-screen confirmation (e.g., "Booking Approved!").
    *   The request is removed from the "Pending" list and may move to an "Approved" or "Upcoming Bookings" list within the Trainer Portal.
    *   A notification (in-app, email, SMS - based on player's preferences) is sent to the player confirming their booking.
    *   The court slot is now marked as "Booked" and unavailable to other users for that specific time.

**Alternative Scenario (Decline):**

4.  **Decision - Decline:**
    *   Trainer decides to decline the request.
    *   Trainer clicks the "Decline" button associated with the request.

5.  **Reason for Decline (Optional but Recommended):**
    *   A modal or field appears prompting the trainer to provide a brief reason for declining (e.g., "Court maintenance," "Conflicting event," or a custom message).
    *   Trainer enters a reason (if required/chosen) and confirms the decline.

6.  **Confirmation of Decline:**
    *   System updates the booking status to "Declined".
    *   Trainer receives an on-screen confirmation (e.g., "Booking Declined.").
    *   The request is removed from the "Pending" list and may move to a "Declined" or archived list.
    *   A notification is sent to the player informing them that their request was declined, including the reason if provided.
    *   The court slot remains available for booking by others (unless the reason for decline makes it unavailable, e.g., maintenance).

**Other Scenarios / Features:**

*   **Chat with Requester:**
    *   Before approving or declining, the trainer might need to clarify something with the player.
    *   A "Chat with [Player Name]" button or link is available on the request details.
    *   Clicking this opens the in-app messaging interface with the player (see Messaging Flow).
    *   The request remains pending while they chat.
*   **Multiple Pending Requests:** Trainer can process multiple requests one after another from their portal.
*   **Expired Request:** If a request is not acted upon within a certain timeframe (system rule), it might auto-expire or flag for attention (out of scope for initial MVP unless specified).

**Post-conditions (Approval):**
*   Booking is confirmed.
*   Player is notified of approval.
*   Court slot is marked as unavailable.
*   Trainer's pending list is updated.

**Post-conditions (Decline):**
*   Booking is declined.
*   Player is notified of decline (with reason, if provided).
*   Court slot typically remains available.
*   Trainer's pending list is updated.

--- 
This flow will be used as a basis for creating wireframes for the Trainer Portal and related interactions.
