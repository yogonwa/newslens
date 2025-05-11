# NewsGrid Redesign & Feature Implementation Plan

## Overview
This document outlines the implementation plan and completed changes for the NewsLens frontend grid redesign, focusing on:
- Header cleanup
- Enhanced date picker
- Source filter integration
- Grid frame and image sizing redesign (**3:2 aspect ratio grid cell redesign: ✅ Complete and validated, looks good**)
- Grid padding/spacing tweaks
- Page layout and control bar adjustments

Each section includes code references and actionable steps for developers.

---

## 1. Remove Top Date Header

**Goal:** Eliminate the redundant date display in the top right of the header.

**Status:** ✅ Complete

**Code References:**
- `frontend/src/components/Header.tsx`

**Steps:**
1. Locate the date display logic in `Header.tsx` (look for the current date rendered in the header bar).
2. Remove or comment out the JSX and any related logic for this date display.
3. Test to ensure only the main date picker remains visible.

---

## 2. Enhanced Date Picker (Calendar Selector)

**Goal:** Make the main date display clickable to open a monthly calendar selector, while retaining left/right day navigation.

**Status:** ✅ Complete

**Code References:**
- `frontend/src/components/Controls.tsx` (date navigation and picker)
- `frontend/src/routes/Home.tsx` (date state management)

**Steps:**
1. Install a calendar picker library (e.g., `react-day-picker`).
   ```bash
   npm install react-day-picker
   ```
2. In `Controls.tsx`, wrap the date display in a clickable element.
3. On click, open a popover/modal with the calendar picker.
4. On date selection, update the selected date state and close the picker.
5. Ensure left/right arrows still increment/decrement by one day.
6. Test for accessibility and mobile usability.

---

## 3. Source Filter Integration

**Goal:** Integrate source toggles into the filter toolbar, allowing users to show/hide source rows with clear active/inactive states.

**Status:** ✅ Complete

**Code References:**
- `frontend/src/components/Controls.tsx` (filter UI and toggles)
- `frontend/src/routes/Home.tsx` (activeSourceIds state, filtering logic)
- `frontend/src/components/NewsGrid.tsx` (sources prop, row rendering)

**Steps:**
1. Refactor the filter toolbar in `Controls.tsx` to display toggle buttons for each source.
2. Use the `activeSourceIds` state to determine which sources are active.
3. Style toggles for clear active (on) and inactive (off) states (e.g., color, opacity, border).
4. On toggle, update `activeSourceIds` in `Home.tsx`.
5. Pass only active sources to `NewsGrid.tsx` so only those rows are rendered.
6. Test toggling sources on/off and verify the grid updates accordingly.

---

## 4. Grid Frame and Image Sizing Redesign

**Goal:** Redesign grid cell dimensions and aspect ratio to match the standard image size from the backend.

**Status:** ✅ Complete

**Code References:**
- `frontend/src/components/NewsGrid.tsx` (grid layout)
- `frontend/src/components/NewsCell.tsx` (image rendering)
- `frontend/src/constants/timeSlots.ts` (grid structure)

**Steps:**
1. Determine the standard image dimensions/aspect ratio from backend/S3 (e.g., 4:3, 16:9, 400x300px, etc.).
2. In `NewsGrid.tsx`, update the grid cell CSS to use a fixed aspect ratio (e.g., via `aspect-ratio` property or padding hack).
3. In `NewsCell.tsx`, set the `<img>` tag to use `object-fit: cover` or `contain` as appropriate.
4. Set a fixed width (or responsive width) for grid cells; let height be determined by aspect ratio.
5. Test with real images to ensure clean, consistent display with no awkward cropping or stretching.
6. Adjust as needed for best visual results.

---

## 5. Grid Padding/Spacing Tweaks

**Goal:** Reduce or eliminate padding/gaps between image boxes for a seamless, photographic negative effect.

**Status:** ✅ Complete (current grid uses a 3:2 aspect ratio and even spacing; further tweaks can be made as needed)

**Code References:**
- `frontend/src/components/NewsGrid.tsx` (grid layout CSS)

**Steps:**
1. Adjust the `gap` or `padding` properties in the grid container and cell CSS.
2. Test the visual effect with real data.
3. Review with design/UX stakeholders and decide whether to keep or revert.

---

## 6. Grid Page Layout & Control Bar Redesign

**Goal:** Streamline the grid page layout for maximum grid visibility and a cleaner, more focused UI.

**Status:** ✅ Complete

**Key Changes:**
- Source labels are displayed as column headers, center justified, in colored boxes (e.g., CNN in a red box with white text). See `NewsGrid.tsx`.
- The top padding between the nav bar and the page title is set to 61px (`pt-[61px]` in Tailwind), per user request. See `Home.tsx`.
- The time slot row titles display the rounded grey vertical bar before the time (reverted to original style). See `NewsGrid.tsx`.
- The page title and controls are positioned directly below the nav bar, with minimal vertical whitespace.
- All grid and control bar layout changes have been accepted and are live in the codebase.

**Code References:**
- `frontend/src/components/Header.tsx` (nav bar and top-level layout)
- `frontend/src/routes/Home.tsx` (page title, subtitle, control bar, and top padding)
- `frontend/src/components/Controls.tsx` (calendar and source filter controls)
- `frontend/src/components/NewsGrid.tsx` (grid layout, source headers, time slot row titles)

**Relevant Code Comments:**
- `Home.tsx`: The main container uses `pt-[61px]` to control the space below the nav bar. Adjust this value if the nav bar height changes.
- `NewsGrid.tsx`: Source labels are rendered as colored, center-justified column headers. The time slot row label layout is documented inline.

---

## 7. Outstanding or Optional Items

- All requested grid layout, spacing, and labeling changes are complete and live.
- No outstanding required items remain for the grid redesign.
- Optional: Further grid gap/padding tweaks or additional visual polish can be considered in the future if desired by design/UX stakeholders.

---

## General Notes
- All changes should be tested for responsiveness and accessibility.
- Update documentation and code comments as needed.
- Coordinate with backend if image dimensions or formats change in the future.

---

**Contact:** For questions or code review, see the `#frontend` channel or contact the lead engineer. 