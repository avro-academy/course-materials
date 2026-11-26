import type { JobInput } from "../types";

export type Errors = Partial<Record<keyof JobInput, string>>;

/** Check the form. Returns an object with a message for each problem (empty if all good). */
export function validateJob(job: JobInput): Errors {
  const errors: Errors = {};
  if (job.company.trim() === "") errors.company = "Enter the company or organisation.";
  if (job.role.trim() === "") errors.role = "Enter the job title.";
  if (job.link !== "" && !/^https?:\/\/\S+$/.test(job.link)) {
    errors.link = "Links must start with http:// or https://";
  }
  if (job.status !== "Saved" && job.appliedOn === "") {
    errors.appliedOn = "Add the date you applied.";
  }
  if (job.followUp !== "" && job.appliedOn !== "" && job.followUp < job.appliedOn) {
    errors.followUp = "The follow-up date can't be before you applied.";
  }
  if (job.notes.length > 500) errors.notes = "Keep notes under 500 characters.";
  return errors;
}
