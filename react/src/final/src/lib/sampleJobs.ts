import type { Job } from "../types";
import { addDays, todayISO } from "./dates";

// Example applications shown the first time you open the app, so it isn't empty.
// They're made up — delete them and add your own. Dates are worked out from today.
export function sampleJobs(today: string = todayISO()): Job[] {
  return [
    { id: "sample-1", company: "Corner Café", role: "Casual barista", location: "Sydney", status: "Interview",
      appliedOn: addDays(today, -8), followUp: addDays(today, 2), link: "", notes: "Interview on Thursday at 10am." },
    { id: "sample-2", company: "City Sports Store", role: "Retail team member", location: "Parramatta", status: "Applied",
      appliedOn: addDays(today, -4), followUp: addDays(today, 10), link: "", notes: "" },
    { id: "sample-3", company: "Local library", role: "Weekend assistant", location: "Sydney", status: "Saved",
      appliedOn: "", followUp: "", link: "", notes: "Applications close at the end of the month." },
  ];
}
