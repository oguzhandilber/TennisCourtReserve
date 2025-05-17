# Wireframes: Ancillary Pages (Mobile-First)

This document describes the basic wireframes for the Notifications and Profile & Settings pages, ensuring consistency with the overall mobile-first and minimalist design approach of CourtReserve.

---

## 1. Notifications Center Page (Mobile)

**Objective:** Display a list of real-time alerts for approvals, cancellations, new messages, and other relevant events.

**Elements:**

*   **Header:**
    *   Title: "Notifications".
    *   Back Button (if accessed from a deeper link, otherwise part of main navigation).
    *   (Optional) "Mark all as read" button/icon.
    *   (Optional) Filter icon (e.g., to show only unread, or filter by type - messages, bookings).
*   **Notifications List:**
    *   If no notifications: Message like "No new notifications."
    *   Each notification as a List Item:
        *   Icon relevant to notification type (e.g., calendar for booking, chat bubble for message).
        *   Notification Text: Concise summary (e.g., "Your booking for Court 2 on May 21st is confirmed!", "New message from John Doe", "Trainer Alice approved your request for Court 1").
        *   Timestamp: e.g., "2m ago", "1h ago", "Yesterday".
        *   Unread Indicator: (e.g., a small dot or different background color for unread items).
        *   Tappable: Clicking a notification navigates to the relevant screen (e.g., booking detail, chat window).
*   **Bottom Navigation Bar (if used, Notifications might be one of the tabs).**

**Layout Notes:** Clean, chronological list. Easy to scan and identify unread/important items. Swipe actions (e.g., swipe to mark as read or delete) could be considered for higher fidelity.

---

## 2. Profile & Settings Page (Mobile)

**Objective:** Allow users to manage personal information, photo, linked trainers (for players), notification preferences, and saved favorite courts.

**Elements:**

*   **Header:**
    *   Title: "Profile & Settings" or "My Profile".
    *   Back Button (if applicable) or part of main navigation.
    *   (Optional) "Edit" button for profile section, or inline edit icons.
*   **Profile Summary Section (Top):**
    *   User Avatar/Photo (placeholder if none uploaded, with an option to upload/change).
    *   User Name (e.g., "Jane Doe").
    *   Email Address (display only, or link to change email).
    *   (Optional for Trainer) Trainer Badge/Status.
*   **Settings Menu (List of tappable items):**
    *   **Account Information:**
        *   Link: "Edit Profile" (navigates to a screen to change name, photo, potentially password if not using social OAuth primarily).
        *   Link: "Manage Password" (if email/password login is used).
    *   **Player-Specific (if user is a player):**
        *   Link: "My Favorite Courts" (navigates to a list of saved courts).
        *   Link: "Linked Trainers" (view and manage trainers they follow or are linked with - future feature).
    *   **Trainer-Specific (if user is a trainer):**
        *   Link: "My Courts" (manage courts they are assigned to - future feature).
        *   Link: "Availability Settings" (manage their working hours/blackout dates - future feature).
    *   **General Settings:**
        *   Link: "Notification Preferences" (navigates to a screen to toggle push/email/SMS for different event types like booking confirmations, cancellations, messages, waitlist alerts).
        *   Link: "Payment Methods" (if payments are integrated - future feature).
    *   **Application Settings:**
        *   Link: "Help & Support / FAQ".
        *   Link: "Terms of Service".
        *   Link: "Privacy Policy".
    *   **Action:**
        *   Button/Link: "Log Out".
*   **Bottom Navigation Bar (if used, Profile might be one of the tabs).**

**Layout Notes:** Group related settings logically. Use standard list item format for menu options, often with a chevron icon (>) to indicate navigation to a new screen.

---

## 2a. Edit Profile Screen (Mobile - Sub-screen of Profile & Settings)

**Objective:** Allow users to update their personal information.

**Elements:**

*   **Header:**
    *   Title: "Edit Profile".
    *   Back Button (to Profile & Settings).
    *   "Save" Button (becomes active if changes are made).
*   **Profile Fields:**
    *   Avatar/Photo Section: Current photo with "Change Photo" button/icon.
    *   Input Field: Full Name.
    *   Input Field (Display Only or Editable with verification): Email Address.
    *   (Optional) Input Field: Phone Number (for SMS notifications).

**Layout Notes:** Simple form layout.

---

## 2b. Notification Preferences Screen (Mobile - Sub-screen of Profile & Settings)

**Objective:** Allow users to customize how they receive notifications.

**Elements:**

*   **Header:**
    *   Title: "Notification Preferences".
    *   Back Button (to Profile & Settings).
    *   (Optional) "Save" button if changes require explicit saving, otherwise changes are instant.
*   **Notification Types List (Each with toggles for different channels):**
    *   **Booking Confirmations:**
        *   Toggle: In-App
        *   Toggle: Email
        *   Toggle: SMS (if phone number provided and SMS enabled)
    *   **Booking Cancellations:**
        *   Toggle: In-App
        *   Toggle: Email
        *   Toggle: SMS
    *   **New Messages:**
        *   Toggle: In-App
        *   Toggle: Email
    *   **Waitlist Alerts:**
        *   Toggle: In-App
        *   Toggle: Email
        *   Toggle: SMS
    *   **(More notification types as features are added)**

**Layout Notes:** Clear list of notification categories with easy-to-use toggles for each channel.

---

These basic structures will help maintain a consistent user experience across the application. They are designed to be simple and extensible as more features are added.
