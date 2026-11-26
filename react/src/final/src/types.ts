// The shape of one job application. Every part of the app uses this type.

export const STATUSES = ["Saved", "Applied", "Interview", "Offer", "Rejected"] as const;

export type Status = (typeof STATUSES)[number];

export type Job = {
  id: string;
  company: string;
  role: string;
  location: string;
  status: Status;
  appliedOn: string; // "YYYY-MM-DD", or "" if not applied yet
  followUp: string; // "YYYY-MM-DD" to check in with them, or ""
  link: string; // the job ad
  notes: string;
};

// What the form works with: everything except the id.
export type JobInput = Omit<Job, "id">;

// A blank form for a new job.
export const EMPTY_JOB: JobInput = {
  company: "",
  role: "",
  location: "",
  status: "Saved",
  appliedOn: "",
  followUp: "",
  link: "",
  notes: "",
};
