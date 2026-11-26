import type { Job, JobInput, Status } from "../types";

// Every change to the list of jobs is an "action". The reducer works out the new list.
export type JobsAction =
  | { type: "added"; job: Job }
  | { type: "updated"; id: string; changes: JobInput }
  | { type: "statusChanged"; id: string; status: Status; today: string }
  | { type: "deleted"; id: string };

export function jobsReducer(jobs: Job[], action: JobsAction): Job[] {
  switch (action.type) {
    case "added":
      return [action.job, ...jobs];
    case "updated":
      return jobs.map((job) => (job.id === action.id ? { ...action.changes, id: job.id } : job));
    case "statusChanged":
      return jobs.map((job) =>
        job.id === action.id
          ? {
              ...job,
              status: action.status,
              // Moving to "Applied" for the first time fills in today's date.
              appliedOn: action.status !== "Saved" && job.appliedOn === "" ? action.today : job.appliedOn,
            }
          : job,
      );
    case "deleted":
      return jobs.filter((job) => job.id !== action.id);
  }
}
