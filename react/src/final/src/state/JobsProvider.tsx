import { useEffect, useReducer } from "react";
import { loadJobs, saveJobs } from "../lib/storage";
import { JobsContext } from "./jobsContext";
import { jobsReducer } from "./jobsReducer";

// Holds the list of jobs for the whole app, and saves it whenever it changes.
export default function JobsProvider({ children }: { children: React.ReactNode }) {
  const [jobs, dispatch] = useReducer(jobsReducer, undefined, loadJobs);

  useEffect(() => {
    saveJobs(jobs);
  }, [jobs]);

  return <JobsContext value={{ jobs, dispatch }}>{children}</JobsContext>;
}
