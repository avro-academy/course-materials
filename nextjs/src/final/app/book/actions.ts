"use server";

import { BOOKING_TIMES } from "@/lib/booking";
import { TIME_ZONE } from "@/lib/hours";

export type BookingState = {
  status: "idle" | "error" | "success";
  message: string;
  errors: Partial<Record<"name" | "email" | "date" | "time" | "guests", string>>;
  values: Record<string, string>;
};

/** Today's date as YYYY-MM-DD in the café's time zone. */
function todayInSydney(): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: TIME_ZONE }).format(new Date());
}

export async function bookTable(prevState: BookingState, formData: FormData): Promise<BookingState> {
  // Everything from a form arrives as text — and could be anything, so check it all here on the server.
  const values = {
    name: String(formData.get("name") ?? "").trim(),
    email: String(formData.get("email") ?? "").trim(),
    date: String(formData.get("date") ?? ""),
    time: String(formData.get("time") ?? ""),
    guests: String(formData.get("guests") ?? ""),
  };
  const errors: BookingState["errors"] = {};

  if (values.name.length < 2 || values.name.length > 60) {
    errors.name = "Please enter your name (2–60 characters).";
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
    errors.email = "Please enter a valid email address.";
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(values.date)) {
    errors.date = "Please choose a date.";
  } else if (values.date < todayInSydney()) {
    errors.date = "That date has already passed.";
  }
  if (!BOOKING_TIMES.includes(values.time)) {
    errors.time = "Please choose a time from the list.";
  }
  const guests = Number(values.guests);
  if (!Number.isInteger(guests) || guests < 1 || guests > 8) {
    errors.guests = "We can book tables for 1 to 8 people.";
  }

  if (Object.keys(errors).length > 0) {
    return { status: "error", message: "Please fix the highlighted fields.", errors, values };
  }

  // A real site would save the booking to a database and send an email here.
  return {
    status: "success",
    message: `Thanks, ${values.name}! Your table for ${guests} on ${values.date} at ${values.time} is requested.`,
    errors: {},
    values: {},
  };
}
