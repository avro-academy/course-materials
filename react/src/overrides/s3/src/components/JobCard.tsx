import { formatDate } from "../lib/dates";
import { STATUSES, type Job, type Status } from "../types";
import StatusBadge from "./StatusBadge";

type Props = {
  job: Job;
  onStatusChange: (id: string, status: Status) => void; // a function from the parent, called when the status changes
};

export default function JobCard({ job, onStatusChange }: Props) {
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
      <select
        value={job.status}
        onChange={(e) => onStatusChange(job.id, e.target.value as Status)}
        aria-label={`Status of ${job.role}`}
      >
        {STATUSES.map((s) => (
          <option key={s}>{s}</option>
        ))}
      </select>
    </li>
  );
}
