# CourtReserve - Responsive Layout Specifications

This document outlines the responsive layout strategy for the CourtReserve application, focusing on the key prototyped flows: Booking a Court and Trainer Approval. The design is mobile-first, with adaptations for tablet and desktop breakpoints.

## 1. Breakpoints

Standard breakpoints will be used to ensure a consistent experience across devices:

*   **Mobile:** Up to 767px (Base design, single column, touch-friendly)
*   **Tablet:** 768px to 1023px (Wider layout, potentially 2 columns for some content, increased spacing)
*   **Desktop:** 1024px and above (Full-width layouts, multi-column designs, enhanced navigation)

## 2. General Principles for Responsiveness

*   **Fluid Grids:** Content will reflow naturally as screen size changes. The `app-container` in the prototypes has a `max-width` for mobile, which will be adjusted or removed for wider screens.
*   **Flexible Images:** Images will scale within their containers.
*   **Navigation:**
    *   Mobile: Hamburger menu for primary navigation (if applicable beyond bottom nav), bottom navigation bar for core app sections.
    *   Tablet/Desktop: Visible top navigation bar, potentially a sidebar for more complex sections like a full admin dashboard (though admin is out of scope for initial prototypes).
*   **Typography:** Font sizes may be slightly increased for larger screens to maintain readability and visual hierarchy.
*   **Spacing:** Margins, paddings, and gutters will increase proportionally on larger screens to utilize white space effectively.
*   **Touch Targets:** Remain sufficiently large on all devices.

## 3. Key Screen Adaptations

Below are descriptions of how key prototyped screens will adapt. (Visual illustrations would typically accompany these descriptions in a full design document.)

### 3.1 Landing Page (`landing_page.html`)

*   **Mobile (Current Prototype):** Single column layout. Hero section text and CTA are centered. Features are listed vertically or in a simple grid if space allows (as prototyped).
*   **Tablet:**
    *   Hero section: Text may remain centered, or content could be split into two columns (e.g., text on one side, illustrative graphic/image on the other if available).
    *   Features overview: Can comfortably use a 2 or 3-column grid for feature items.
    *   Header: Logo on left, navigation links (e.g., "Features", "Log In", "Sign Up") on right instead of just a hamburger menu icon.
*   **Desktop:**
    *   Hero section: Similar to tablet, potentially wider, with more prominent visuals.
    *   Features overview: Clear 3-column layout for features.
    *   Header: Full navigation menu visible.

### 3.2 Sign Up / Log In Page (`signup_login.html`)

*   **Mobile (Current Prototype):** Centered, single-column form. Tabs for Sign Up/Log In.
*   **Tablet & Desktop:**
    *   The form container can remain centered with a defined `max-width` (e.g., 400-500px) to maintain focus and readability, even on larger screens. The overall page background (`Cloud White`) would fill the rest of the screen.
    *   Alternatively, the layout could become a two-panel design on desktop: one panel for an illustrative graphic or brand message, the other for the authentication form.
    *   No significant changes to the form elements themselves are needed, as they are standard.

### 3.3 Dashboard (`dashboard.html`)

*   **Mobile (Current Prototype):** Single column layout. Quick actions, upcoming bookings list, calendar placeholder. Bottom navigation bar.
*   **Tablet:**
    *   Content sections (Quick Actions, Bookings, Calendar) could be arranged in a two-column layout if it improves information density without clutter. For example, Quick Actions and a summary of Bookings on one side, Calendar on the other.
    *   Calendar placeholder could show a more expansive view.
    *   Bottom navigation might transition to a sidebar or a more prominent top navigation if the app had more top-level sections.
*   **Desktop:**
    *   A multi-column dashboard is possible. For instance, a main content area for the calendar, a sidebar for upcoming bookings and quick actions.
    *   The calendar view would be much larger and more interactive.
    *   Header: Logo, user profile/notifications, main navigation links.

### 3.4 Court Listing Page (`court_listing.html`)

*   **Mobile (Current Prototype):** Single column list of court cards. Filter bar at the top.
*   **Tablet:**
    *   Court cards could be displayed in a 2-column grid.
    *   Filter bar remains at the top. Advanced filters panel could be a persistent sidebar or a wider dropdown/modal.
*   **Desktop:**
    *   Court cards in a 2 or 3-column grid.
    *   Filters could be in a dedicated sidebar for easier access and more complex filtering options.
    *   Map view (future feature) could be integrated alongside the list view.

### 3.5 Court Detail Page (`court_detail.html`)

*   **Mobile (Current Prototype):** Single column. Image carousel at top, followed by info, then calendar/time slots. Sticky booking action bar at the bottom.
*   **Tablet:**
    *   Layout could become two-column below the image carousel: court information (name, description, trainer) on one side, and the calendar/time slot selection on the other.
    *   Image carousel could be wider.
    *   Booking action bar remains, possibly with more information displayed if space allows.
*   **Desktop:**
    *   Similar to tablet, but with more generous spacing. The two-column layout for info and booking would be very effective.
    *   Image carousel could be larger, or show multiple thumbnails.
    *   Calendar and time slots can be more expansive.

### 3.6 Trainer Portal (`trainer_portal.html`)

*   **Mobile (Current Prototype):** Single column list of request cards. Filter tabs at the top.
*   **Tablet:**
    *   Request cards remain in a single column for clarity of information within each card, but the overall container could be wider.
    *   Filter tabs remain prominent.
    *   If a chat interface were integrated, it could appear as a modal or a split view on larger tablets.
*   **Desktop:**
    *   A two-panel layout could be effective: list of requests on one side, and when a request is selected, its details and action options (or a chat interface) appear in a larger panel on the other side.
    *   Filter tabs could be part of a more comprehensive dashboard header for trainers.

## 4. CSS Implementation Notes

*   Use CSS Flexbox and Grid for layout structures to ensure inherent flexibility.
*   Employ media queries (`@media (min-width: 768px) { ... }`, `@media (min-width: 1024px) { ... }`) in `common_styles.css` or page-specific CSS to apply layout changes.
*   Adjust `max-width` of `.app-container` for tablet and desktop, or allow it to be full-width within a larger site wrapper.
*   Test thoroughly on different devices and screen sizes.

This document provides a high-level strategy. Detailed mockups for each breakpoint would typically be created in a design tool to visualize these changes accurately.

