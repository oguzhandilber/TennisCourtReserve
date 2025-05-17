# CourtReserve - Accessibility Considerations

This document outlines accessibility considerations for the CourtReserve application prototypes, aiming to ensure the platform is usable by people with a wide range of abilities, including those with visual, auditory, motor, and cognitive impairments. Adherence to Web Content Accessibility Guidelines (WCAG) 2.1 Level AA is the target.

## 1. Semantic HTML Structure

*   **Rationale:** Using correct HTML5 semantic elements (e.g., `<header>`, `<nav>`, `<main>`, `<article>`, `<aside>`, `<footer>`, `<button>`, `<label>`, `<input>`) provides inherent meaning and structure to the content, which is crucial for assistive technologies like screen readers.
*   **Implementation Notes:**
    *   Prototypes use semantic elements where appropriate (e.g., `app-header`, `app-footer`, `main`, `section`, `form`, `button`).
    *   Headings (`<h1>` - `<h6>`) are used hierarchically to structure page content.
    *   Lists (`<ul>`, `<ol>`, `<li>`) are used for navigation items and lists of content.

## 2. Color Contrast

*   **Rationale:** Sufficient contrast between text and its background is essential for users with low vision or color blindness.
*   **Implementation Notes (as per Style Guide):**
    *   **Primary Text (`#343A40` Charcoal Grey) on Light Backgrounds (`#FFFFFF` Pure White, `#F8F9FA` Cloud White):** This combination generally provides excellent contrast (e.g., Charcoal on White is ~15.7:1, well above WCAG AA requirement of 4.5:1 for normal text).
    *   **Primary Action Buttons (`#FFFFFF` White text on `#00A79D` Vibrant Teal background):** Contrast ratio is approximately 4.56:1, which meets WCAG AA for large text (buttons are considered large text due to font weight and size) and just meets for normal text. Care should be taken if smaller text is used on this background.
    *   **Secondary Text (`#6C757D` Medium Grey) on Light Backgrounds:** Contrast with Pure White is ~4.7:1, meeting AA.
    *   **Placeholder Text (`#CED4DA` in prototypes, should be darker):** The placeholder color `#CED4DA` on `#FFFFFF` has a low contrast (1.57:1). **Recommendation:** Placeholder text color should be darkened to meet at least 3:1 against the input background, or ideally 4.5:1 if it conveys essential information (though placeholders shouldn't be the sole source of information).
    *   **Status Colors:** Ensure text on status color backgrounds (e.g., white text on green/red toasts) meets contrast requirements.
*   **Tooling:** Use contrast checker tools during development to verify all text/background combinations.

## 3. Keyboard Navigation

*   **Rationale:** All interactive elements must be operable via a keyboard for users who cannot use a mouse (e.g., users with motor impairments, screen reader users).
*   **Implementation Notes:**
    *   **Focus Order:** Logical and intuitive focus order is maintained by using semantic HTML and ensuring the DOM order matches the visual order.
    *   **Interactive Elements:** All links (`<a>`), buttons (`<button>`), form fields (`<input>`, `<select>`, `<textarea>`), and custom interactive components (like calendar days, time slots, tabs) must be focusable and operable using the keyboard (Enter/Space for activation).
        *   Custom interactive elements (e.g., `div`s used as buttons or tabs) need `tabindex="0"` to be included in the focus order and appropriate JavaScript event listeners for key presses (Enter/Space).
    *   **Visible Focus Indicator:** Browsers provide default focus indicators. These are preserved and enhanced in prototypes (e.g., `.form-input:focus` styles). Custom focus indicators should be highly visible and meet contrast requirements.
    *   **Skip Links (Not explicitly prototyped but recommended):** For pages with extensive navigation before the main content, a "Skip to main content" link should be the first focusable element, visible only when focused.

## 4. ARIA (Accessible Rich Internet Applications) Attributes

*   **Rationale:** ARIA attributes can enhance the accessibility of custom controls and dynamic content updates by providing additional information to assistive technologies.
*   **Implementation Notes (Recommendations for full development):**
    *   **Roles:** Assign appropriate roles to custom widgets (e.g., `role="tablist"`, `role="tab"`, `role="tabpanel"` for tabbed interfaces; `role="dialog"` for modals; `role="alert"` for toast notifications).
        *   *Prototype Note:* `signup_login.html` tabs could be enhanced with these roles.
    *   **States and Properties:** Use ARIA attributes to indicate states (e.g., `aria-selected` for active tabs or selected calendar dates/times, `aria-expanded` for accordions/menus, `aria-hidden` for off-screen content, `aria-disabled` for disabled elements, `aria-invalid` for form errors).
        *   *Prototype Note:* Calendar days/time slots selection, modal visibility, and tab states are good candidates for ARIA state attributes.
    *   **Live Regions:** For dynamic content changes (e.g., toast notifications, error messages appearing, search results updating), use `aria-live` regions (`aria-live="polite"` or `aria-live="assertive"`) to inform screen reader users.
        *   *Prototype Note:* Toast notifications should be within an `aria-live` region.
    *   **Labels and Descriptions:** Use `aria-label`, `aria-labelledby`, or `aria-describedby` to provide accessible names or descriptions for elements where visible text labels are insufficient or absent (e.g., icon-only buttons, complex form groups).
        *   *Prototype Note:* Icon buttons (e.g., nav-icon, favorite icon, filter icon) should have `aria-label`.

## 5. Images and Icons

*   **Rationale:** Images need alternative text for screen reader users. Icons that convey meaning also need accessible names.
*   **Implementation Notes:**
    *   **Informative Images (`<img>` tags):** Provide descriptive `alt` text (e.g., court thumbnails should describe the court or scene).
        *   *Prototype Note:* Placeholder images have generic alt text; this would be specific in production.
    *   **Decorative Images:** Use empty `alt=""` or CSS background images if an image is purely decorative and adds no information.
    *   **Icon Fonts / SVG Icons:** Ensure icons are not read out as meaningless characters. If they are interactive (buttons), provide an accessible name via `aria-label` or visually hidden text.
        *   *Prototype Note:* Placeholder text icons (e.g., 🔔, ⚙️, 📅) should be replaced with actual SVGs or icon fonts with proper accessibility handling (e.g., `aria-hidden="true"` on the icon itself if text label is present, or `aria-label` on the button containing the icon).

## 6. Forms

*   **Rationale:** Forms must be understandable and operable for all users.
*   **Implementation Notes:**
    *   **Labels:** All form inputs (`<input>`, `<textarea>`, `<select>`) must have associated `<label>` elements, programmatically linked using `for` and `id` attributes.
        *   *Prototype Note:* Implemented in `signup_login.html` and modal forms.
    *   **Error Handling:** Validation errors should be clearly identified, described to the user (both visually and programmatically), and focus should be managed to help users correct errors.
        *   *Prototype Note:* Inline error messages are styled. Programmatic association via `aria-describedby` and `aria-invalid="true"` is recommended. Focus should ideally move to the first invalid field on submission error.
    *   **Required Fields:** Clearly indicate required fields visually (e.g., with an asterisk) and programmatically (e.g., `aria-required="true"`).

## 7. Dynamic Content and Modals

*   **Rationale:** Changes in content and the appearance of modals need to be managed for accessibility.
*   **Implementation Notes:**
    *   **Modals (`role="dialog"`, `aria-modal="true"`):**
        *   When a modal opens, focus should be moved into the modal.
        *   Keyboard focus should be trapped within the modal until it is closed.
        *   When the modal closes, focus should return to the element that triggered it.
        *   The underlying page content should be inert (e.g., `aria-hidden="true"` on the main content container).
        *   *Prototype Note:* Basic modal visibility is handled. Full focus management is a development task.
    *   **Toast Notifications (`role="alert"` or `aria-live` region):** Ensure screen readers announce these non-modal messages.

## 8. Page Titles

*   **Rationale:** Each page should have a unique and descriptive `<title>` element for browser history and assistive technology orientation.
*   **Implementation Notes:** All prototyped HTML pages have unique `<title>`s.

## Testing

*   **Manual Keyboard Testing:** Navigate through all interactive elements using only the keyboard (Tab, Shift+Tab, Enter, Space, Arrow keys where appropriate).
*   **Screen Reader Testing:** Test with common screen readers (e.g., NVDA, JAWS, VoiceOver) to ensure a good experience.
*   **Automated Tools:** Use accessibility checker browser extensions or linters (e.g., Axe, WAVE) to catch common issues.

By considering these aspects throughout the design and development process, CourtReserve can be made accessible to a wider audience, aligning with best practices and legal requirements.

