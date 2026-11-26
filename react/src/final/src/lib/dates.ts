// Dates are stored as "YYYY-MM-DD" text: easy to read, and they sort and compare in the right order.

/** Today's date on this computer, as "YYYY-MM-DD". */
export function todayISO(): string {
  const now = new Date();
  return toISO(now);
}

function toISO(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

/** "2026-03-14" -> "14 Mar 2026" */
export function formatDate(iso: string): string {
  if (!iso) return "";
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(y, m - 1, d).toLocaleDateString("en-AU", { day: "numeric", month: "short", year: "numeric" });
}

/** addDays("2026-03-14", 3) -> "2026-03-17". Negative numbers go back. */
export function addDays(iso: string, days: number): string {
  const [y, m, d] = iso.split("-").map(Number);
  return toISO(new Date(y, m - 1, d + days));
}
