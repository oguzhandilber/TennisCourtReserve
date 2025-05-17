# CourtReserve Style Guide - Part 1: Foundations

This document outlines the foundational elements of the CourtReserve visual style: color palette, logo, and typography. The design aims for a modern, bright, inviting, and trustworthy feel, emphasizing speed and simplicity with a minimalist aesthetic.

## 1. Color Palette

As per the requirements, the palette consists of two primary brand colors and neutral tones. The goal is to be bright, inviting, and modern.

*   **Primary Brand Color 1 (Action & Energy):**
    *   Name: `Vibrant Teal`
    *   HEX: `#00A79D` (A bright, energetic teal that evokes a sense of activity and freshness, suitable for CTAs and active states.)
    *   Usage: Primary buttons, active navigation elements, key highlights, accents.

*   **Primary Brand Color 2 (Trust & Calm):**
    *   Name: `Deep Aqua`
    *   HEX: `#27677A` (A deeper, calming aqua that conveys trust and stability, good for secondary information or backgrounds for highlighted sections.)
    *   Usage: Secondary buttons, informational icons, subtle backgrounds, text links.

*   **Neutral Tones:**
    *   **Base Background:**
        *   Name: `Cloud White`
        *   HEX: `#F8F9FA` (A very light, almost white grey, providing a soft background that isn’t stark white, enhancing the generous white space feel.)
    *   **Content Background / Cards:**
        *   Name: `Pure White`
        *   HEX: `#FFFFFF` (For content areas, cards, and modals to make them pop against the Cloud White.)
    *   **Primary Text:**
        *   Name: `Charcoal Grey`
        *   HEX: `#343A40` (A dark grey for body text, ensuring high contrast and readability.)
    *   **Secondary Text / Labels:**
        *   Name: `Medium Grey`
        *   HEX: `#6C757D` (For less emphasized text, labels, and helper text.)
    *   **Borders / Dividers:**
        *   Name: `Light Grey`
        *   HEX: `#CED4DA` (For subtle borders, dividers, and disabled states.)

*   **Accent & Status Colors:**
    *   **Success/Confirmation:**
        *   Name: `Forest Green`
        *   HEX: `#28A745` (Standard green for success messages, approved status.)
    *   **Warning/Pending:**
        *   Name: `Amber Yellow`
        *   HEX: `#FFC107` (For warnings, pending status, or attention-grabbing notifications.)
    *   **Error/Decline:**
        *   Name: `Crimson Red`
        *   HEX: `#DC3545` (Standard red for error messages, declined status.)

## 2. Placeholder Logo

Since a final logo is not available, a simple, clean text-based placeholder will be used. This can be easily replaced later.

*   **Design:** The name "CourtReserve" in a modern, friendly sans-serif typeface.
*   **Option 1 (Minimalist Text):**
    *   `CourtReserve` (using the primary typography choice for headings, perhaps in `Deep Aqua` or `Charcoal Grey`).
*   **Option 2 (Text with a subtle icon hint - conceptual):**
    *   A very simple abstract representation of a tennis ball or court lines integrated subtly with the text. For now, we will stick to text-only for simplicity in HTML/CSS representation.
    *   Example: `CourtReserve` with a small teal dot (`#00A79D`) next to it or integrated into one of the letters if a suitable font allows.

**For initial HTML/CSS prototypes, the logo will be rendered as text styled with CSS.**

```html
<div class="logo" style="font-family: 'PrimaryFont', sans-serif; font-size: 24px; color: #27677A; font-weight: bold;">
  CourtReserve
</div>
```

## 3. Typography

Typography will focus on clarity, hierarchy, and a modern feel. A sans-serif font family is recommended for its readability on screens.

*   **Primary Font Family:** `Inter` (A highly legible and versatile sans-serif font, available via Google Fonts. If Inter is not available, a system default like `Helvetica Neue`, `Arial`, or `sans-serif` will be used as a fallback).

*   **Font Weights:** Regular (400), Medium (500), Semi-Bold (600), Bold (700).

*   **Hierarchy & Sizing (Mobile-first baseline, can scale up for larger screens):**

    *   **H1 / Page Titles (e.g., "Book Your Court", "Trainer Portal")**
        *   Font Size: `28px`
        *   Font Weight: `Bold (700)`
        *   Line Height: `1.2`
        *   Color: `Charcoal Grey (#343A40)`

    *   **H2 / Section Titles (e.g., "Your Upcoming Bookings", "Pending Requests")**
        *   Font Size: `22px`
        *   Font Weight: `Semi-Bold (600)`
        *   Line Height: `1.3`
        *   Color: `Charcoal Grey (#343A40)`

    *   **H3 / Card Titles, Sub-Section Titles (e.g., Court Name in a card)**
        *   Font Size: `18px`
        *   Font Weight: `Semi-Bold (600)`
        *   Line Height: `1.4`
        *   Color: `Charcoal Grey (#343A40)`

    *   **Body Text (Paragraphs, descriptions):**
        *   Font Size: `16px`
        *   Font Weight: `Regular (400)`
        *   Line Height: `1.6`
        *   Color: `Charcoal Grey (#343A40)`

    *   **Labels / Secondary Text (Input labels, helper text, timestamps):**
        *   Font Size: `14px`
        *   Font Weight: `Regular (400)`
        *   Line Height: `1.5`
        *   Color: `Medium Grey (#6C757D)`

    *   **Button Text:**
        *   Font Size: `16px`
        *   Font Weight: `Medium (500)` or `Semi-Bold (600)`
        *   Line Height: `1` (buttons usually have fixed height)
        *   Color: `Pure White (#FFFFFF)` for dark buttons, `Vibrant Teal (#00A79D)` for light/outline buttons.

    *   **Caption / Small Text (e.g., fine print, very subtle info):**
        *   Font Size: `12px`
        *   Font Weight: `Regular (400)`
        *   Line Height: `1.4`
        *   Color: `Medium Grey (#6C757D)`

**Accessibility Note:** Ensure sufficient contrast ratios between text and background colors, adhering to WCAG AA guidelines at a minimum.

---

This first part of the style guide sets the visual tone. The next part will detail spacing, grid, and specific UI components.
