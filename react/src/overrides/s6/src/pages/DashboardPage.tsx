import { Link } from "react-router";
import StatusBadge from "../components/StatusBadge";
import Tips from "../components/Tips";
import { formatDate, todayISO } from "../lib/dates";
import { countByStatus, followUpsDue } from "../lib/stats";
import { STATUSES, type Job } from "../types";

export default function DashboardPage({ jobs }: { jobs: Job[] }) {
  const today = todayISO();

  const counts = countByStatus(jobs);
  const due = followUpsDue(jobs, today);

  return (
    <>
      <h1>Dashboard</h1>
      <p className="muted">
        You&apos;re tracking {jobs.length} {jobs.length === 1 ? "job" : "jobs"}.
      </p>

      <ul className="stats">
        {STATUSES.map((status) => (
          <li key={status}>
            <Link to={`/jobs?status=${status}`}>
              <span className="stat-number">{counts[status]}</span>
              <StatusBadge status={status} />
            </Link>
          </li>
        ))}
      </ul>

      <section className="panel">
        <h2>Follow up this week</h2>
        {due.length > 0 ? (
          <ul className="plain-list">
            {due.map((job) => (
              <li key={job.id}>
                <Link to={`/jobs/${job.id}`}>{job.role}</Link> at {job.company}
                <span className={job.followUp < today ? "due overdue" : "due"}>
                  {job.followUp < today ? "Overdue · " : ""}
                  {formatDate(job.followUp)}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="muted">Nothing due. Nice work!</p>
        )}
      </section>

      <section className="panel">
        <h2>Tip of the day</h2>
        <Tips />
      </section>
    </>
  );
}
