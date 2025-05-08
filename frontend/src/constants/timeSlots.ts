// Canonical time slots for NewsLens grid (US Eastern Time)
// IMPORTANT: Keep in sync with backend/config/base.py: DEFAULT_CAPTURE_TIMES

export const STANDARD_TIME_SLOTS = [
  { id: '06:00', label: '6:00 AM', time: '06:00' },
  { id: '09:00', label: '9:00 AM', time: '09:00' },
  { id: '12:00', label: '12:00 PM', time: '12:00' },
  { id: '15:00', label: '3:00 PM', time: '15:00' },
  { id: '18:00', label: '6:00 PM', time: '18:00' },
];

export type TimeSlot = typeof STANDARD_TIME_SLOTS[number]; 