import type { Metadata } from "next";
import BookingForm from "./BookingForm";

export const metadata: Metadata = {
  title: "Book a table",
  description: "Request a table at Corner Café for up to 8 people.",
};

export default function BookPage() {
  return (
    <>
      <h1 className="text-3xl font-extrabold">Book a table</h1>
      <p className="mt-2 mb-6 text-stone-600">Tables for 1 to 8 people. For bigger groups, give us a call.</p>
      <BookingForm />
    </>
  );
}
