# Wireframes: Trainer Approval Flow (Mobile-First)

This document describes the wireframes for the key screens in the "Trainer Approval" user flow. The design prioritizes a mobile-first approach, minimalism, and clear calls to action for trainers.

**General Principles (consistent with Booking Flow):**
*   **Navigation:** Simple top navigation (hamburger menu on mobile, potentially expanding to a top bar on larger screens) and/or bottom tab bar for key sections on mobile if the trainer has other functionalities.
*   **Typography:** Clear hierarchy.
*   **CTAs:** Prominent buttons with clear labels (Approve, Decline).
*   **Spacing:** Generous white space.

---

## 1. Trainer Portal / Booking Requests Page (Mobile)

**Objective:** Display a list of pending booking requests for the trainer to review.

**Elements:**

*   **Header:**
    *   Title: "Booking Requests" or "Trainer Portal".
    *   Navigation Icon (Hamburger menu) or Profile Icon.
    *   (Optional) Filter/Sort options for requests (e.g., by date, court).
*   **Pending Requests List:**
    *   If no pending requests: Message like "No pending booking requests at this time."
    *   Each request as a tappable List Item or Card:
        *   **Player Info:** Player Name (e.g., "John Doe").
        *   **Court Info:** Court Name/Number (e.g., "Court 3").
        *   **Requested Slot:** Date and Time (e.g., "May 20, 2:00 PM - 3:00 PM").
        *   **Received Time:** e.g., "Requested: 1h ago" or timestamp.
        *   **Status Indicator:** Clearly marked as "Pending".
        *   (Optional) Short snippet of player's note if provided.
*   **(Optional) Tabs for different request statuses:**
    *   "Pending" (Default View)
    *   "Approved"
    *   "Declined"
    *   "History"
*   **Bottom Navigation Bar (if applicable for Trainer role, might differ from Player's):**
    *   Icons: Requests, Schedule, Messages, Profile.

**Layout Notes:** Clean, scannable list. Each item should provide enough information for a quick assessment before tapping for details.

---

## 2. Request Detail View (Mobile)

**Objective:** Show detailed information for a selected booking request and allow the trainer to approve, decline, or message the requester.

**Elements:**

*   **Header:**
    *   Title: "Request Details" or "[Player Name]'s Request".
    *   Back Button (to return to the requests list).
*   **Request Information Section:**
    *   **Player:** [Player Name] (Potentially tappable to view player profile/history - future).
    *   **Court:** [Court Name/Number], [Surface Type], [Indoor/Outdoor].
    *   **Date:** [Full Date, e.g., Tuesday, May 20, 2025].
    *   **Time:** [Time Slot, e.g., 2:00 PM - 3:00 PM].
    *   **Requested On:** [Date/Time of request submission].
    *   **Player's Note (if any):**
        *   "Note from [Player Name]: [Player's message content]"
*   **(Optional) Court Schedule Snippet:**
    *   A small visual or text indicating the court's availability around the requested slot (e.g., "Court is free 1hr before and 2hrs after this slot"). This helps in understanding context but the system should primarily handle conflict detection.
*   **Action Buttons (Prominently displayed, often at the bottom or in a sticky footer):**
    *   Primary Button: "Approve" (e.g., Green color).
    *   Secondary Button: "Decline" (e.g., Red or neutral with red icon).
    *   Tertiary Button/Link: "Chat with [Player Name]" (opens in-app messaging).

**Layout Notes:** All critical information clearly presented. Action buttons should be unambiguous and easy to tap.

---

## 3. Decline Reason Modal (Mobile)

**Objective:** Allow the trainer to provide a reason when declining a booking request (optional but good practice).

**Elements (Appears as a Modal Overlay after tapping "Decline"):**

*   **Title:** "Decline Booking Request".
*   **Instruction:** "Please provide a reason for declining (optional but recommended). This will be shared with the player."
*   **Predefined Reasons (Optional Radio Buttons/Checkboxes for quick selection):**
    *   [ ] Court Unavailable / Maintenance
    *   [ ] Scheduling Conflict (Trainer)
    *   [ ] Double Booking (System error, unlikely but possible)
    *   [ ] Other (allows custom text)
*   **Text Area for Custom Reason:**
    *   Input Field: "Custom reason..."
*   **Action Buttons:**
    *   Primary Button: "Confirm Decline"
    *   Secondary Button: "Cancel" (returns to Request Detail view).

**Layout Notes:** Simple, focused modal. Makes it easy to provide a reason or skip if truly optional.

---

## 4. Confirmation Toasts/Messages (Mobile)

**Objective:** Provide immediate feedback after an action (Approve/Decline).

**Elements (Typically non-intrusive Toasts or Banners):**

*   **On Approval:**
    *   Message: "Booking Approved! [Player Name] has been notified."
    *   (Disappears automatically after a few seconds).
*   **On Decline:**
    *   Message: "Booking Declined. [Player Name] has been notified."
    *   (Disappears automatically after a few seconds).

**Layout Notes:** Should not block further interaction unless it's a full-screen confirmation for a critical step (less common for simple approve/decline).

---

This completes the initial set of wireframes for the "Trainer Approval" flow. These, along with the "Booking a Court" wireframes, will form the basis for the high-fidelity prototypes.
