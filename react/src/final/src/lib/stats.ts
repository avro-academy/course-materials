import type { Job, Status } from "../types";
import { STATUSES } from "../types";
import { addDays } from "./dates";

/** Search text and a status filter. */
export function filterJobs(jobs: Job[], search: string, status: Status | ""): Job[] {
  const q = search.trim().toLowerCase();
  return jobs.filter(
    (job) =>
      (status === "" || job.status === status) &&
      (q === "" || `${job.company} ${job.role} ${job.location}`.toLowerCase().includes(q)),
  );
}

/** How many jobs have each status (including the ones with none). */
export function countByStatus(jobs: Job[]): Record<Status, number> {
  const counts = Object.fromEntries(STATUSES.map((s) => [s, 0])) as Record<Status, number>;
  for (const job of jobs) counts[job.status] += 1;
  return counts;
}

/** Open jobs with a follow-up date in the next 7 days (or already passed), soonest first. */
export function followUpsDue(jobs: Job[], today: string): Job[] {
  const weekAway = addDays(today, 7);
  return jobs
    .filter((job) => job.followUp !== "" && job.followUp <= weekAway && job.status !== "Rejected" && job.status !== "Offer")
    .sort((a, b) => a.followUp.localeCompare(b.followUp));
}
