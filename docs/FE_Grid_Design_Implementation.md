# NewsGrid Redesign & Feature Implementation Plan

## Overview
This document outlines the implementation plan for the next phase of NewsLens frontend improvements, focusing on:
- Header cleanup
- Enhanced date picker
- Source filter integration
- Grid frame and image sizing redesign (**3:2 aspect ratio grid cell redesign: ✅ Complete and validated, looks good**)
- (Optional) Grid padding/spacing tweaks

Each section includes code references and actionable steps for developers.

---

## 1. Remove Top Date Header

**Goal:** Eliminate the redundant date display in the top right of the header.

**Code References:**
- `frontend/src/components/Header.tsx`

**Steps:**
1. Locate the date display logic in `Header.tsx` (look for the current date rendered in the header bar).
2. Remove or comment out the JSX and any related logic for this date display.
3. Test to ensure only the main date picker remains visible.

---

## 2. Enhanced Date Picker (Calendar Selector)

**Goal:** Make the main date display clickable to open a monthly calendar selector, while retaining left/right day navigation.

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

## 5. (Optional) Grid Padding/Spacing Tweaks

**Goal:** Experiment with reducing or eliminating padding/gaps between image boxes for a seamless, photographic negative effect.

**Code References:**
- `frontend/src/components/NewsGrid.tsx` (grid layout CSS)

**Steps:**
1. Adjust the `gap` or `padding` properties in the grid container and cell CSS.
2. Test the visual effect with real data.
3. Review with design/UX stakeholders and decide whether to keep or revert.

---

## 6. Grid Page Layout & Control Bar Redesign

**Goal:** Streamline the grid page layout for maximum grid visibility and a cleaner, more focused UI.

**Design Adjustments:**
- Keep the existing simple top-level navigation bar (no changes).
- Move the main page title (e.g., "Media Coverage Comparison") up, directly below the nav bar.
- Remove the subtitle below the page title.
- Remove the search bar and the calendar label/date in the top right corner.
- Shift all content up to minimize vertical whitespace and maximize grid visibility.
- Place the calendar filter and source filter controls inline, right-justified with the page title.
- Reduce whitespace between the title/control bar and the grid so more of the grid is visible on page load.
- Maintain a 5x5 grid with even cell spacing and a 3:2 aspect ratio for all grid cells.

**Code References:**
- `frontend/src/components/Header.tsx` (for nav bar and top-level layout)
- `frontend/src/routes/Home.tsx` (for page title, subtitle, and control bar)
- `frontend/src/components/Controls.tsx` (for calendar and source filter controls)
- `frontend/src/components/NewsGrid.tsx` (for grid layout and spacing)

**Steps:**
1. Remove the subtitle and search bar from the Home page layout.
2. Remove the top-right calendar label/date from the header.
3. Move the page title up, directly below the nav bar.
4. Place the calendar filter and source filter controls inline, right-justified with the page title.
5. Adjust layout and CSS to minimize vertical whitespace between the title/control bar and the grid.
6. Ensure the grid remains 5x5, with even spacing and a 3:2 aspect ratio for all cells.
7. Test on desktop and mobile to confirm improved grid visibility and alignment.

---

## General Notes
- All changes should be tested for responsiveness and accessibility.
- Update documentation and code comments as needed.
- Coordinate with backend if image dimensions or formats change in the future.

---

**Contact:** For questions or code review, see the `#frontend` channel or contact the lead engineer. 