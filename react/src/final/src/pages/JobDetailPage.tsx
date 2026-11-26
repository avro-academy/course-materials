import { Link, useNavigate, useParams } from "react-router";
import StatusBadge from "../components/StatusBadge";
import { formatDate, todayISO } from "../lib/dates";
import { useJobs } from "../state/useJobs";
import { STATUSES } from "../types";
import NotFoundPage from "./NotFoundPage";

export default function JobDetailPage() {
  const { id } = useParams();
  const { jobs, dispatch } = useJobs();
  const navigate = useNavigate();
  const job = jobs.find((j) => j.id === id);

  if (!job) return <NotFoundPage />;

  const handleDelete = () => {
    if (window.confirm(`Delete "${job.role}" at ${job.company}?`)) {
      dispatch({ type: "deleted", id: job.id });
      navigate("/jobs");
    }
  };

  return (
    <>
      <p>
        <Link to="/jobs">← All jobs</Link>
      </p>
      <div className="toolbar">
        <h1>{job.role}</h1>
        <StatusBadge status={job.status} />
      </div>
      <p className="muted">
        {job.company}
        {job.location && ` · ${job.location}`}
      </p>

      <div className="status-buttons" role="group" aria-label="Change status">
        {STATUSES.map((s) => (
          <button
            key={s}
            type="button"
            aria-pressed={job.status === s}
            onClick={() => dispatch({ type: "statusChanged", id: job.id, status: s, today: todayISO() })}
          >
            {s}
          </button>
        ))}
      </div>

      <dl className="details">
        <dt>Applied</dt>
        <dd>{job.appliedOn ? formatDate(job.appliedOn) : "Not yet"}</dd>
        <dt>Follow up</dt>
        <dd>{job.followUp ? formatDate(job.followUp) : "—"}</dd>
        <dt>Job ad</dt>
        <dd>
          {job.link ? (
            <a href={job.link} target="_blank" rel="noreferrer">
              Open the ad
            </a>
          ) : (
            "—"
          )}
        </dd>
        <dt>Notes</dt>
        <dd className="notes">{job.notes || "—"}</dd>
      </dl>

      <div className="actions">
        <Link to={`/jobs/${job.id}/edit`} className="button">
          Edit
        </Link>
        <button type="button" className="button danger" onClick={handleDelete}>
          Delete
        </button>
      </div>
    </>
  );
}
