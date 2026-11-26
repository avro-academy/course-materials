"use client";

import { useActionState } from "react";
import { BOOKING_TIMES } from "@/lib/booking";
import { bookTable, type BookingState } from "./actions";

const initialState: BookingState = { status: "idle", message: "", errors: {}, values: {} };

function Field({ label, error, children }: { label: string; error?: string; children: React.ReactNode }) {
  return (
    <label className="grid gap-1 font-semibold">
      {label}
      {children}
      {error && <span className="text-sm font-normal text-red-700">{error}</span>}
    </label>
  );
}

const input = "rounded-lg border border-stone-300 px-3 py-2 font-normal";

export default function BookingForm() {
  const [state, formAction, pending] = useActionState(bookTable, initialState);

  if (state.status === "success") {
    return (
      <div role="status" className="max-w-md rounded-2xl bg-green-50 p-6 text-green-900 ring-1 ring-green-200">
        <p className="text-lg font-bold">Booking requested 🎉</p>
        <p className="mt-2">{state.message}</p>
        <p className="mt-2 text-sm">We&apos;ll email you to confirm.</p>
      </div>
    );
  }

  return (
    <form action={formAction} noValidate className="grid max-w-md gap-4 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-stone-200">
      {state.message && (
        <p role="alert" className="rounded-lg bg-red-50 p-3 text-red-800">
          {state.message}
        </p>
      )}
      <Field label="Your name" error={state.errors.name}>
        <input name="name" defaultValue={state.values.name} className={input} autoComplete="name" />
      </Field>
      <Field label="Email" error={state.errors.email}>
        <input name="email" type="email" defaultValue={state.values.email} className={input} autoComplete="email" />
      </Field>
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Date" error={state.errors.date}>
          <input name="date" type="date" defaultValue={state.values.date} className={input} />
        </Field>
        <Field label="Time" error={state.errors.time}>
          {/* The key rebuilds the list after an error, so it shows the time that was chosen */}
          <select key={state.values.time} name="time" defaultValue={state.values.time ?? ""} className={input}>
            <option value="">Choose…</option>
            {BOOKING_TIMES.map((t) => (
              <option key={t}>{t}</option>
            ))}
          </select>
        </Field>
      </div>
      <Field label="Number of people" error={state.errors.guests}>
        <input name="guests" type="number" min={1} max={8} defaultValue={state.values.guests ?? "2"} className={input} />
      </Field>
      <button
        disabled={pending}
        className="rounded-full bg-stone-900 px-5 py-2.5 font-semibold text-white hover:bg-stone-700 disabled:opacity-60"
      >
        {pending ? "Sending…" : "Request booking"}
      </button>
    </form>
  );
}
