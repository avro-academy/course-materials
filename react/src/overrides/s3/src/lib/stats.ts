import type { Job, Status } from "../types";

/** Search text and a status filter. */
export function filterJobs(jobs: Job[], search: string, status: Status | ""): Job[] {
  const q = search.trim().toLowerCase();
  return jobs.filter(
    (job) =>
      (status === "" || job.status === status) &&
      (q === "" || `${job.company} ${job.role} ${job.location}`.toLowerCase().includes(q)),
  );
}
