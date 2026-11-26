import { createContext, type Dispatch } from "react";
import type { Job } from "../types";
import type { JobsAction } from "./jobsReducer";

export type JobsContextValue = { jobs: Job[]; dispatch: Dispatch<JobsAction> };

export const JobsContext = createContext<JobsContextValue | null>(null);
