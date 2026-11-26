import type { Job } from "../types";
import { sampleJobs } from "./sampleJobs";

const KEY = "job-tracker.jobs";

/** Load saved jobs from the browser. First visit (or broken data) → the sample jobs. */
export function loadJobs(): Job[] {
  try {
    const saved = localStorage.getItem(KEY);
    return saved ? (JSON.parse(saved) as Job[]) : sampleJobs();
  } catch {
    return sampleJobs();
  }
}

export function saveJobs(jobs: Job[]): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(jobs));
  } catch {
    // Storage can be full or switched off (e.g. some private windows). The app still works, it just won't remember.
  }
}
