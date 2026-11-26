// Opening hours and "today" in the café's own time zone.
export const TIME_ZONE = "Australia/Sydney";

// Hours as decimals: 7 = 7:00am, 15.5 = 3:30pm.
export const HOURS: Record<string, { open: number; close: number }> = {
  Monday: { open: 7, close: 15 },
  Tuesday: { open: 7, close: 15 },
  Wednesday: { open: 7, close: 15 },
  Thursday: { open: 7, close: 15 },
  Friday: { open: 7, close: 16 },
  Saturday: { open: 7, close: 16 },
  Sunday: { open: 7, close: 14 },
};

export const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

export function cafeClock(now: Date): { day: string; time: number } {
  const parts = new Intl.DateTimeFormat("en-AU", {
    timeZone: TIME_ZONE,
    weekday: "long",
    hour: "numeric",
    minute: "numeric",
    hourCycle: "h23",
  }).formatToParts(now);
  const get = (type: string) => parts.find((p) => p.type === type)?.value ?? "";
  return { day: get("weekday"), time: Number(get("hour")) + Number(get("minute")) / 60 };
}

export function isOpen(now: Date): boolean {
  const { day, time } = cafeClock(now);
  const today = HOURS[day];
  return time >= today.open && time < today.close;
}

/** 15.5 -> "3:30pm" */
export function formatHour(hour: number): string {
  const h = Math.floor(hour);
  const m = Math.round((hour - h) * 60);
  const suffix = h < 12 ? "am" : "pm";
  const h12 = h % 12 === 0 ? 12 : h % 12;
  return `${h12}${m ? `:${String(m).padStart(2, "0")}` : ""}${suffix}`;
}
