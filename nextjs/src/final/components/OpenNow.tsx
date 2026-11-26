import { connection } from "next/server";
import { isOpen } from "@/lib/hours";

// Depends on the time of the visit, so it must run when someone visits — not at build time.
export default async function OpenNow() {
  await connection(); // "wait for a real visitor"
  const open = isOpen(new Date());

  return open ? (
    <p className="inline-block rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-800">
      ● Open now
    </p>
  ) : (
    <p className="inline-block rounded-full bg-stone-200 px-3 py-1 text-sm font-semibold text-stone-700">
      ● Closed right now
    </p>
  );
}
