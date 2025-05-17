# CourtReserve - Prototype Annotations and Key Interactions

This document provides annotations for key interactions and functionalities within the CourtReserve HTML prototypes. These annotations complement the UX Rationale document and aim to clarify how users interact with the application.

## General Interactions (Implemented across multiple pages)

*   **Navigation:**
    *   **Logo Link:** Clicking the "CourtReserve" logo in the header navigates to the primary starting page (Landing Page for unauthenticated users, Dashboard for authenticated users).
        *   *Annotation:* `landing_page.html`, `signup_login.html`, `dashboard.html`, `court_listing.html`, `court_detail.html`, `trainer_portal.html` - Logo is a link.
    *   **Back Arrow:** On pages like Court Detail or Court Listing (when navigated from Dashboard), a back arrow (`&larr;`) in the header allows users to return to the previous page.
        *   *Annotation:* `court_listing.html`, `court_detail.html` - Back arrow uses `javascript:history.back()` or links to a logical previous page.
    *   **Bottom Navigation (Mobile):** Sticky bottom navigation on `dashboard.html` and `court_listing.html` (and would be on other core pages) allows quick switching between main app sections. Active tab is highlighted.
        *   *Annotation:* `dashboard.html`, `court_listing.html` - JS can be used to highlight active tab based on current page, or direct links are used.
    *   **Placeholder Nav Icons (Header/Footer):** Icons like hamburger menu, notifications, profile, etc., trigger JavaScript `alert()` placeholders indicating future functionality.
        *   *Annotation:* Across various pages.
*   **Button States:** All buttons (`.btn` classes) have defined default, hover, active, and disabled states as per `common_styles.css` and the Style Guide. Disabled states prevent interaction.
    *   *Annotation:* Visual feedback on interaction.
*   **Form Input Focus:** Input fields (`.form-input`) show a visual change (border color, box shadow) when focused, guiding the user.
    *   *Annotation:* CSS `:focus` pseudo-class.
*   **Toast Notifications:** Used for non-critical feedback (e.g., booking request sent, favorite toggled). Appear, display a message, and auto-dismiss.
    *   *Annotation:* `court_detail.html` (booking, favorite), `trainer_portal.html` (request processing). JS controls visibility and content.
*   **Modal Interactions:** Modals (e.g., booking confirmation) overlay the content, have a close button (`&times;`), and action buttons (Confirm/Cancel). Clicking the overlay (optional, not prototyped) or Cancel/Close button dismisses the modal.
    *   *Annotation:* `court_detail.html` - Booking confirmation modal.

## Page-Specific Interactions

### 1. Landing Page (`landing_page.html`)

*   **"Book a Court Now" Button:** Primary CTA, navigates to `signup_login.html` (assuming new user or needs to log in).
    *   *Annotation:* Clear entry point into the booking flow.

### 2. Sign Up / Log In Page (`signup_login.html`)

*   **Tab Switching (Sign Up / Log In):** Clicking tabs dynamically shows the corresponding form and updates the active tab style.
    *   *Annotation:* JavaScript `showForm()` function handles this.
*   **Form Submission:**
    *   Email/Password forms: On submit, basic validation (e.g., password match for sign-up) is performed (placeholder). Successful submission (placeholder) navigates to `dashboard.html`.
    *   Social OAuth Buttons: Placeholder `alert()` indicating future functionality.
    *   *Annotation:* JavaScript event listeners on form submit.
*   **"Forgot Password?" Link:** Placeholder `alert()` or would navigate to a password reset flow.
*   **Switch Form Links ("Already have an account? Log In" / "Don’t have an account? Sign Up"):** Calls `showForm()` to switch between forms.

### 3. Dashboard (`dashboard.html`)

*   **"Find & Book a Court" Button:** Navigates to `court_listing.html`.
*   **Notification Icon:** Placeholder `alert()` for opening notification center.
*   **Upcoming Booking Cards:** These are static in the prototype but would typically be clickable to view booking details.

### 4. Court Listing Page (`court_listing.html`)

*   **Search Input & Button:** Typing in search and clicking search icon triggers `applySearch()` JS function, which simulates loading (shows skeleton) and then displays results (currently just re-shows default list or no-results example).
*   **Filter Icon (Gear):** Toggles visibility of the `advanced-filters` panel using `toggleFilters()` JS.
*   **Advanced Filters Apply Button:** Simulates applying filters, shows loading, then hides panel.
*   **Court Card Clicks:** Each court card is wrapped in an `<a>` tag, navigating to `court_detail.html` with the respective `courtId` as a query parameter.
    *   *Annotation:* `href="court_detail.html?courtId=X"`.
*   **Loading Skeletons:** `showLoading()` and `hideLoading()` JS functions control the display of skeleton screens during simulated data fetches.

### 5. Court Detail Page (`court_detail.html`)

*   **Dynamic Content Load:** Page content (court name, image, details) is populated by JavaScript based on the `courtId` from the URL query parameter and `courtData` object.
*   **Favorite Icon (Star):** Toggles between filled (★) and outline (☆) star, simulating add/remove from favorites. Shows a toast notification. JS `toggleFavorite()`.
*   **Calendar Interaction:**
    *   **Month Navigation ("Prev" / "Next"):** Updates the displayed month in the calendar using JS `renderCalendar()`.
    *   **Date Selection:** Clicking an "available" date cell highlights it, calls `selectDate()`, and populates the "Available Slots" section for that date. Previously selected date is de-highlighted.
    *   *Annotation:* Available dates have `.available` class; selected date gets `.selected` class.
*   **Time Slot Selection:** Clicking an available time slot highlights it and calls `selectTime()`. Previously selected time is de-highlighted.
    *   *Annotation:* Selected time slot gets `.selected` class.
*   **Booking Action Bar:** Appears only when both a date and a time slot are selected. Displays a summary of the selection. JS `updateBookingActionState()`.
*   **"Request Booking" Button:** Opens the booking confirmation modal. JS `openBookingModal()`.
*   **Booking Confirmation Modal:**
    *   Displays selected court, date, and time.
    *   "Cancel" or Close button (`&times;`) closes the modal (`closeBookingModal()`).
    *   "Send Request" button simulates API call, closes modal, shows success toast, and clears selection/refreshes calendar. JS `confirmBookingRequest()`.
*   **Trainer Chip Click:** Placeholder `alert()` for viewing trainer profile.

### 6. Trainer Portal (`trainer_portal.html`)

*   **Filter Tabs (Pending, Approved, Declined, All):** Clicking tabs filters the list of requests. JS `filterRequests()` updates visibility of `.request-item` elements based on `data-status` attribute. Active tab is highlighted. Counts in tabs are updated by `updateCounts()`.
*   **"Approve" / "Decline" Buttons:** For pending requests, these buttons call `processRequest()`. This JS function updates the item’s `data-status`, changes its visual style (border, removes action buttons, adds status text), and shows a toast.
*   **"Chat" Button:** Placeholder `alert()` indicating navigation to a chat interface with the player.
*   **Settings/Menu Icon (Header):** Placeholder `alert()`.

This annotation list covers the primary interactive elements of the prototyped flows. In a more detailed specification, each screen would have these annotations directly overlaid or listed alongside screenshots.

