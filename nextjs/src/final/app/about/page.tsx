import type { Metadata } from "next";
import { DAYS, HOURS, formatHour } from "@/lib/hours";

export const metadata: Metadata = {
  title: "About",
  description: "Who we are, where to find us and our opening hours.",
};

// Read on the server. Set CAFE_PHONE in .env.local (or in your hosting settings).
const phone = process.env.CAFE_PHONE ?? "(02) 5550 0000";

export default function AboutPage() {
  return (
    <div className="grid gap-10 py-4 md:grid-cols-2">
      <div>
        <h1 className="text-3xl font-extrabold">About Corner Café</h1>
        <p className="mt-4 text-stone-700">
          We&apos;re a small neighbourhood café run by a team of locals. We roast our beans in Marrickville, bake
          every morning and know most of our regulars by name.
        </p>
        <p className="mt-4 text-stone-700">
          Find us at <strong>12 King Street, Newtown NSW</strong>, or call us on <strong>{phone}</strong>.
        </p>
      </div>
      <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-stone-200">
        <h2 className="text-xl font-extrabold">Opening hours</h2>
        <table className="mt-3 w-full text-stone-700">
          <tbody>
            {DAYS.map((day) => (
              <tr key={day} className="border-b border-stone-100 last:border-0">
                <td className="py-1.5">{day}</td>
                <td className="py-1.5 text-right">
                  {formatHour(HOURS[day].open)} – {formatHour(HOURS[day].close)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
