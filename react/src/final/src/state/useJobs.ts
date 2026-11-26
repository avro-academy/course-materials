import { useContext } from "react";
import { JobsContext } from "./jobsContext";

/** Use the jobs list (and dispatch) in any component inside <JobsProvider>. */
export function useJobs() {
  const value = useContext(JobsContext);
  if (value === null) {
    throw new Error("useJobs must be used inside <JobsProvider>");
  }
  return value;
}
