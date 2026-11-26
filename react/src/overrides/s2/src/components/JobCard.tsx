import { formatDate } from "../lib/dates";
import type { Job } from "../types";
import StatusBadge from "./StatusBadge";

// Props are the inputs a component is given, like arguments to a function.
type Props = {
  job: Job;
};

export default function JobCard({ job }: Props) {
  return (
    <li className="card">
      <div className="card-top">
        <h3>{job.role}</h3>
        <StatusBadge status={job.status} />
      </div>
      <p className="muted">
        {job.company}
        {job.location && ` · ${job.location}`}
      </p>
      {job.appliedOn && <p className="small">Applied {formatDate(job.appliedOn)}</p>}
    </li>
  );
}
