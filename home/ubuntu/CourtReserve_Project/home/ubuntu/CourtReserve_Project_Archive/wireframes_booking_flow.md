# Wireframes: Booking a Court Flow (Mobile-First)

This document describes the wireframes for the key screens in the "Booking a Court" user flow. The design prioritizes a mobile-first approach, minimalism, and clear calls to action.

**General Principles:**
*   **Navigation:** Simple top navigation (hamburger menu on mobile, potentially expanding to a top bar on larger screens) and/or bottom tab bar for key sections on mobile.
*   **Typography:** Clear hierarchy. Large, bold for titles and key info (like times/dates). Standard size for body text and labels.
*   **CTAs:** Prominent buttons with clear labels.
*   **Spacing:** Generous white space.

---

## 1. Landing Page (Mobile)

**Objective:** Introduce CourtReserve and guide users to book a court.

**Elements:**

*   **Header:**
    *   Logo (placeholder text: "CourtReserve") - top left or centered.
    *   Navigation Icon (Hamburger menu) - top right (if not using bottom tabs for primary nav).
*   **Hero Section:**
    *   Headline: e.g., "Book Your Court, Effortlessly."
    *   Sub-headline: Brief description of CourtReserve (e.g., "Find, book, and manage tennis court reservations in your community.")
    *   Primary CTA Button: "Book a Court Now" (full width or prominent).
*   **Features Overview (Brief):**
    *   Short section with 2-3 icons and brief text highlighting key benefits (e.g., "Easy Scheduling", "Trainer Approved", "Community Focused").
*   **Footer (Optional at this stage for mobile landing):**
    *   Links: About Us, Contact, Terms (minimal).

**Layout Notes:** Single column, scrollable. Focus on the hero and CTA.

---

## 2. Sign Up / Log In Page (Mobile)

**Objective:** Allow users to create an account or log in.

**Elements:**

*   **Header:**
    *   Logo (placeholder text: "CourtReserve") - centered.
    *   (Optional) Back button if navigated from another part of the app.
*   **Tabs/Toggle (for Sign Up / Log In):**
    *   Clear toggle to switch between "Sign Up" and "Log In" forms.
*   **Sign Up Form (Active by default or if selected):**
    *   Input Field: Full Name
    *   Input Field: Email Address
    *   Input Field: Password
    *   Input Field: Confirm Password
    *   Button: "Sign Up"
    *   Separator: "Or sign up with"
    *   Social OAuth Buttons: [Google Icon] [Facebook Icon] (other relevant providers)
    *   Link: "Already have an account? Log In"
*   **Log In Form (Active if selected):**
    *   Input Field: Email Address
    *   Input Field: Password
    *   Link: "Forgot Password?"
    *   Button: "Log In"
    *   Separator: "Or log in with"
    *   Social OAuth Buttons: [Google Icon] [Facebook Icon]
    *   Link: "Don’t have an account? Sign Up"

**Layout Notes:** Centered content, clear form fields. Error message placeholders below fields.

---

## 3. Dashboard (Relevant View for Booking - Mobile)

**Objective:** Show user their current bookings, pending approvals, and provide easy access to find new courts.

**Elements:**

*   **Header:**
    *   Title: "Dashboard" or "Welcome, [User Name]!"
    *   Navigation Icon (Hamburger menu) or Profile Icon.
*   **Primary CTA (if no immediate bookings):**
    *   Button: "Find a Court"
*   **Upcoming Bookings Section:**
    *   Title: "Your Upcoming Bookings"
    *   List/Cards of upcoming bookings:
        *   Court Name, Date, Time
        *   Status: "Confirmed" or "Pending Approval" (with distinct visual cue)
    *   Message if no bookings: "You have no upcoming bookings. Find a court!"
*   **Calendar View (Simplified for initial wireframe):**
    *   A compact calendar display (e.g., weekly view).
    *   Days with bookings/pending requests are highlighted.
    *   Tapping a day might show details below or navigate to a daily schedule view.
*   **(Optional) Quick Access / Favorites:**
    *   Links or cards for "Favorite Courts" or "Recently Viewed".
*   **Bottom Navigation Bar (Common for mobile apps):**
    *   Icons: Home/Dashboard, Courts, Bookings, Messages, Profile.

**Layout Notes:** Sections clearly delineated. Prioritize upcoming bookings and access to court search.

---

## 4. Court Listing Page (Mobile)

**Objective:** Allow users to browse and find available courts.

**Elements:**

*   **Header:**
    *   Title: "Find a Court"
    *   Back Button (if navigated from another screen).
    *   Filter Icon (top right).
*   **Search/Filter Bar (Below Header):**
    *   Search Input: "Search by court name..." (optional for MVP)
    *   Basic Filter Toggles/Dropdowns (visible or accessible via Filter Icon):
        *   Date Picker (default to today)
        *   Time Slot (e.g., Morning, Afternoon, Evening)
        *   (Advanced filters like surface, indoor/outdoor are for later, but placeholders can be considered)
*   **Court Grid/List:**
    *   Each item as a Card:
        *   Thumbnail Image of the court.
        *   Court Name/Number.
        *   Surface Type (e.g., "Clay", "Hard").
        *   Indoor/Outdoor Icon/Text.
        *   Next Available Slot: e.g., "Next: Today, 3:00 PM" or "Available Now".
        *   (Optional) Distance if geo-location is active.
    *   Loading indicator if fetching data.
    *   Message if no courts match criteria: "No courts available for your selection."
*   **Bottom Navigation Bar (if used).**

**Layout Notes:** Scrollable list of court cards. Each card should be tappable to go to Court Detail.

---

## 5. Court Detail Page (Mobile)

**Objective:** Provide detailed information about a specific court and allow users to select a time slot for booking.

**Elements:**

*   **Header:**
    *   Court Name (or "Court Details").
    *   Back Button.
    *   Favorite Icon (to add/remove from favorites).
*   **Court Information Section:**
    *   Image Gallery/Carousel (1-3 images of the court).
    *   Court Name/Number (repeated, larger).
    *   Key Details: Surface Type, Indoor/Outdoor, Capacity, Price per slot (if applicable).
    *   Description (brief).
    *   Trainer(s) Assigned: List of trainer names (tappable to view trainer profile - future).
*   **Availability Schedule Section:**
    *   Date Selector: (e.g., horizontal scrollable list of dates, or a mini-calendar to pick a day).
    *   Time Slot Selector for the chosen date:
        *   List of available time slots (e.g., "09:00 - 10:00", "10:00 - 11:00").
        *   Clear visual distinction for: Available, Selected, Booked, Pending (for others).
        *   Each available slot is tappable.
*   **Booking Action Section (Sticky at bottom or below schedule):**
    *   Selected Slot Info: Display chosen date and time (e.g., "Selected: Mon, May 19, 10:00 AM").
    *   Button: "Request Booking" (becomes active once a slot is selected).
*   **(Optional) Ratings & Reviews Snippet (for later).**

**Layout Notes:** Clear separation between court info and the interactive schedule. The booking action should always be easily accessible once a slot is chosen.

---

## 6. Booking Confirmation Modal/Screen (Mobile)

**Objective:** Confirm the booking request details before submission and provide feedback.

**Elements (Typically a Modal Overlay):**

*   **Title:** "Confirm Your Booking" or "Booking Request".
*   **Summary of Booking:**
    *   Court: [Court Name]
    *   Date: [Selected Date]
    *   Time: [Selected Time]
    *   (Optional) Price: [Price]
*   **(Optional) Note to Trainer:**
    *   Text Area: "Add a note (optional)"
*   **Action Buttons:**
    *   Primary Button: "Send Request" or "Confirm Booking"
    *   Secondary Button: "Cancel" or "Edit Selection"

**After Request Sent (Toast Notification or new screen/modal state):**
*   **Title:** "Request Sent!"
*   **Message:** "Your booking request for [Court Name] on [Date] at [Time] has been sent. You will be notified once it is approved by the trainer."
*   **Button:** "View My Bookings" or "OK"

**Layout Notes:** Modal should be clear and focused. Confirmation message should be reassuring.

---

This completes the initial set of wireframes for the "Booking a Court" flow. These will be refined and used as a basis for high-fidelity prototypes.
