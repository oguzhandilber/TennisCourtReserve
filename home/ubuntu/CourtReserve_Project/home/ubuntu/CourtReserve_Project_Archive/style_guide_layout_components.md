# CourtReserve Style Guide - Part 2: Spacing, Layout, and Core Components

This document builds upon the foundational elements (colors, logo, typography) and details spacing, layout principles, and the design of core UI components for the CourtReserve application.

## 4. Spacing and Layout Grid Principles

Consistent spacing is key to a minimalist aesthetic and clear visual hierarchy. We will use a base unit of `8px` for spacing and sizing.

*   **Base Unit:** `8px`
*   **Common Spacing Values:**
    *   `xs (Extra Small)`: `4px` (0.5 * base unit)
    *   `sm (Small)`: `8px` (1 * base unit)
    *   `md (Medium)`: `16px` (2 * base unit)
    *   `lg (Large)`: `24px` (3 * base unit)
    *   `xl (Extra Large)`: `32px` (4 * base unit)
    *   `xxl (Extra Extra Large)`: `48px` (6 * base unit)

*   **Layout Grid (Mobile-First):**
    *   **Gutters:** `16px (md)` on mobile for main content padding from screen edges.
    *   **Column System (Conceptual for now, more relevant for wider screens):** While mobile is primarily single-column, a flexible grid system (e.g., 12-column) will be considered for tablet and desktop layouts. For mobile, content flow will be vertical.
    *   **Vertical Rhythm:** Strive for consistent vertical spacing between elements using multiples of the base unit to create a harmonious flow.

*   **Generous White Space:** Intentionally leave ample space around elements and sections to improve readability and reduce clutter, reinforcing the minimalist design.

## 5. Core UI Components

Below are the specifications for core UI components. For each component, a description, visual attributes (to be represented as image assets later or via HTML/CSS), and states will be defined.

--- 

### 5.1 Buttons

Buttons are crucial for user interaction and CTAs. They should be easily identifiable and provide clear feedback.

**General Button Styling:**
*   **Border Radius:** `4px` (xs) or `8px` (sm) for a slightly rounded, modern feel.
*   **Padding (Vertical):** `12px` (1.5 * base unit)
*   **Padding (Horizontal):** `24px` (lg)
*   **Font Weight:** `Semi-Bold (600)` (from typography guide).
*   **Text Transform:** `None` (use sentence case for labels, e.g., "Book a Court").

**Types & States:**

1.  **Primary Button (e.g., "Book a Court Now", "Send Request")**
    *   **Default State:**
        *   Background: `Vibrant Teal (#00A79D)`
        *   Text Color: `Pure White (#FFFFFF)`
        *   Border: None
    *   **Hover State:**
        *   Background: Darker shade of Vibrant Teal (e.g., `#008C82`)
        *   Text Color: `Pure White (#FFFFFF)`
    *   **Active/Pressed State:**
        *   Background: Even darker shade of Vibrant Teal (e.g., `#007A70`)
        *   Text Color: `Pure White (#FFFFFF)`
    *   **Disabled State:**
        *   Background: `Light Grey (#CED4DA)`
        *   Text Color: `Medium Grey (#6C757D)`
        *   Cursor: `not-allowed`

2.  **Secondary Button (e.g., "Cancel", "View Details" - less emphasis than primary)**
    *   **Default State:**
        *   Background: `Pure White (#FFFFFF)` or `Cloud White (#F8F9FA)`
        *   Text Color: `Vibrant Teal (#00A79D)`
        *   Border: `1px solid Vibrant Teal (#00A79D)`
    *   **Hover State:**
        *   Background: Very light teal tint (e.g., `#E0F7F6`)
        *   Text Color: `Vibrant Teal (#00A79D)`
        *   Border: `1px solid Darker Vibrant Teal (#008C82)`
    *   **Active/Pressed State:**
        *   Background: Light teal tint (e.g., `#B2EBE8`)
        *   Text Color: `Vibrant Teal (#00A79D)`
    *   **Disabled State:**
        *   Background: `Pure White (#FFFFFF)`
        *   Text Color: `Light Grey (#CED4DA)`
        *   Border: `1px solid Light Grey (#CED4DA)`

3.  **Tertiary/Text Button (e.g., "Forgot Password?", "Chat with Player")**
    *   **Default State:**
        *   Background: Transparent
        *   Text Color: `Deep Aqua (#27677A)`
        *   Border: None
    *   **Hover State:**
        *   Text Color: Darker `Deep Aqua` (e.g., `#1E505F`)
        *   Text Decoration: Underline
    *   **Disabled State:**
        *   Text Color: `Light Grey (#CED4DA)`

**HTML/CSS Example (Primary Button):**
```html
<button class="btn btn-primary" style="background-color: #00A79D; color: #FFFFFF; padding: 12px 24px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
  Primary Action
</button>
<style>
  .btn-primary:hover { background-color: #008C82; }
  .btn-primary:active { background-color: #007A70; }
  .btn-primary:disabled { background-color: #CED4DA; color: #6C757D; cursor: not-allowed; }
</style>
```

--- 

### 5.2 Form Fields (Input, Textarea, Select)

Form fields should be clear, easy to use, and provide visual feedback for states like focus or error.

**General Styling:**
*   **Background:** `Pure White (#FFFFFF)`
*   **Border:** `1px solid Light Grey (#CED4DA)`
*   **Border Radius:** `4px` (xs) or `8px` (sm)
*   **Padding (Internal):** `12px` (1.5 * base unit)
*   **Text Color (Input):** `Charcoal Grey (#343A40)`
*   **Placeholder Text Color:** `Medium Grey (#6C757D)`
*   **Font Size:** `16px` (Body Text)

**States:**

1.  **Default State:** As above.
2.  **Focus State:**
    *   Border Color: `Vibrant Teal (#00A79D)`
    *   Box Shadow (Subtle): `0 0 0 2px rgba(0, 167, 157, 0.25)`
3.  **Error State:**
    *   Border Color: `Crimson Red (#DC3545)`
    *   (Optional) Error icon inside the field or an error message below.
4.  **Disabled State:**
    *   Background: `Cloud White (#F8F9FA)`
    *   Border Color: `Light Grey (#CED4DA)`
    *   Text Color: `Medium Grey (#6C757D)`

**Labels:** Positioned above the input field. Font Size: `14px`, Color: `Medium Grey (#6C757D)`.
**Helper/Error Text:** Positioned below the input field. Font Size: `12px`. Color: `Medium Grey (#6C757D)` for helper, `Crimson Red (#DC3545)` for error.

**HTML/CSS Example (Input Field with Label and Error):**
```html
<div>
  <label for="email" style="font-size: 14px; color: #6C757D; display: block; margin-bottom: 4px;">Email Address</label>
  <input type="email" id="email" class="form-input form-input-error" placeholder="you@example.com" style="width: calc(100% - 24px); background-color: #FFFFFF; border: 1px solid #DC3545; border-radius: 8px; padding: 12px; font-size: 16px; color: #343A40;">
  <p class="error-message" style="font-size: 12px; color: #DC3545; margin-top: 4px;">Please enter a valid email.</p>
</div>
<style>
  .form-input:focus { border-color: #00A79D; box-shadow: 0 0 0 2px rgba(0, 167, 157, 0.25); outline: none; }
  /* .form-input-error specific style already inline for example */
</style>
```

--- 

### 5.3 Modals

Modals are used for focused tasks like confirmations or short forms.

**Styling:**
*   **Overlay Background:** Semi-transparent `Charcoal Grey` (e.g., `rgba(52, 58, 64, 0.6)`).
*   **Modal Container:**
    *   Background: `Pure White (#FFFFFF)`
    *   Border Radius: `8px` (sm) or `12px`
    *   Padding: `24px (lg)` or `32px (xl)`
    *   Box Shadow: Standard shadow for depth (e.g., `0 4px 12px rgba(0,0,0,0.15)`).
*   **Header (Optional):**
    *   Title: `H3` typography, `Charcoal Grey (#343A40)`.
    *   Close Button (X icon): Top right, `Medium Grey (#6C757D)`.
*   **Content Area:** Flexible, uses standard typography and spacing.
*   **Footer/Action Area:** Contains primary/secondary buttons, typically right-aligned or full-width on mobile.

**HTML/CSS Example (Conceptual Structure):**
```html
<div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(52, 58, 64, 0.6); display: flex; align-items: center; justify-content: center;">
  <div class="modal-container" style="background-color: #FFFFFF; border-radius: 8px; padding: 24px; min-width: 300px; max-width: 90%; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
    <div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
      <h3 style="font-size: 18px; font-weight: 600; color: #343A40; margin: 0;">Modal Title</h3>
      <button class="close-button" style="background: none; border: none; font-size: 24px; color: #6C757D; cursor: pointer;">&times;</button>
    </div>
    <div class="modal-content" style="margin-bottom: 24px;">
      <p style="font-size: 16px; color: #343A40; line-height: 1.6;">This is the modal content area.</p>
    </div>
    <div class="modal-footer" style="text-align: right;">
      <button class="btn btn-secondary" style="/* styles from above */ margin-right: 8px;">Cancel</button>
      <button class="btn btn-primary" style="/* styles from above */">Confirm</button>
    </div>
  </div>
</div>
```

--- 

### 5.4 Toast Notifications

Toasts provide brief, auto-expiring messages for feedback on actions.

**Styling:**
*   **Position:** Typically top-right or bottom-center of the screen.
*   **Background:** Based on type (Success: `Forest Green`, Error: `Crimson Red`, Warning: `Amber Yellow`, Info: `Deep Aqua`).
*   **Text Color:** `Pure White (#FFFFFF)` for dark backgrounds, or `Charcoal Grey` for light backgrounds (e.g. if Amber Yellow is too light).
*   **Border Radius:** `4px` (xs) or `8px` (sm).
*   **Padding:** `12px (md)` vertically, `16px (md)` horizontally.
*   **Icon (Optional):** Relevant icon for the type (check, x-mark, warning sign).
*   **Box Shadow:** Subtle shadow for elevation.

**HTML/CSS Example (Success Toast):**
```html
<div class="toast toast-success" style="position: fixed; top: 20px; right: 20px; background-color: #28A745; color: #FFFFFF; padding: 12px 16px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: flex; align-items: center;">
  <!-- Optional Icon -->
  <span style="margin-right: 8px;">✔</span> 
  <span>Action was successful!</span>
</div>
```

--- 

### 5.5 List Items & Cards

Used for displaying collections of data like court listings, booking requests, notifications.

**List Item (Simple, for notifications, menu items):**
*   **Padding:** `12px (md)` vertically, `16px (md)` horizontally.
*   **Border (Bottom):** `1px solid Light Grey (#CED4DA)` for separation.
*   **Content:** Icon (optional), Text, Timestamp/Meta, Chevron (if tappable).
*   **Hover State (if interactive):** Slight background change (e.g., `Cloud White (#F8F9FA)` if on `Pure White`).

**Card (For court listings, dashboard summaries):**
*   **Background:** `Pure White (#FFFFFF)`.
*   **Border Radius:** `8px` (sm) or `12px`.
*   **Border:** `1px solid Light Grey (#CED4DA)` (optional, can rely on shadow).
*   **Box Shadow:** Subtle (e.g., `0 2px 4px rgba(0,0,0,0.05)`).
*   **Padding (Internal):** `16px (md)`.
*   **Structure:**
    *   Image/Thumbnail (for courts).
    *   Title (`H3` style).
    *   Subtitle/Details (labels, secondary text).
    *   Action area (buttons, links - if applicable).

**HTML/CSS Example (Basic Card):**
```html
<div class="card" style="background-color: #FFFFFF; border-radius: 8px; padding: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 16px;">
  <img src="placeholder-court.jpg" alt="Court Thumbnail" style="width: 100%; height: auto; border-radius: 4px; margin-bottom: 12px;">
  <h3 style="font-size: 18px; font-weight: 600; color: #343A40; margin: 0 0 8px 0;">Court Name One</h3>
  <p style="font-size: 14px; color: #6C757D; margin: 0 0 4px 0;">Surface: Clay, Outdoor</p>
  <p style="font-size: 14px; color: #00A79D; margin: 0;">Next Available: Today, 3:00 PM</p>
</div>
```

--- 

### 5.6 Calendar Widget Elements (Basic)

For displaying availability and selecting dates/times. Full calendar is complex, these are basic elements.

*   **Date Cell (in a grid):**
    *   **Default:** `Pure White` background, `Charcoal Grey` text.
    *   **Today:** Special border or background (e.g., `Vibrant Teal` border).
    *   **Selected:** `Vibrant Teal` background, `Pure White` text.
    *   **Available:** Standard.
    *   **Booked/Unavailable:** `Light Grey` background or strikethrough text, `Medium Grey` text.
    *   **Pending:** `Amber Yellow` subtle indicator (e.g., a dot).
    *   **Hover (on available):** Light teal tint.
*   **Time Slot Item (in a list):**
    *   Similar styling to date cells for states (Selected, Available, Booked).
    *   Padding: `8px`.
    *   Border: `1px solid Light Grey`.

--- 

This section covers the main UI components. Image assets would be generated for these states, and the HTML/CSS provides a starting point for the web-based style guide and prototypes. The final step for Task 3 will be to compile these into a cohesive web-based style guide document.
