import { useSearchParams } from "react-router";
import JobCard from "../components/JobCard";
import { filterJobs } from "../lib/stats";
import { STATUSES, type Job, type Status } from "../types";

export default function JobsPage({ jobs }: { jobs: Job[] }) {
  // The filters live in the URL (?q=cafe&status=Applied), so you can bookmark or share a filtered list.
  const [searchParams, setSearchParams] = useSearchParams();
  const q = searchParams.get("q") ?? "";
  const status = (searchParams.get("status") ?? "") as Status | "";

  function setFilter(name: "q" | "status", value: string) {
    const next = new URLSearchParams(searchParams);
    if (value) next.set(name, value);
    else next.delete(name);
    setSearchParams(next, { replace: true });
  }

  const shown = filterJobs(jobs, q, status);

  return (
    <>
      <h1>My jobs</h1>
      <div className="filters">
        <input
          type="search"
          value={q}
          onChange={(e) => setFilter("q", e.target.value)}
          placeholder="Search company, role or place…"
          aria-label="Search jobs"
        />
        <select value={status} onChange={(e) => setFilter("status", e.target.value)} aria-label="Filter by status">
          <option value="">All statuses</option>
          {STATUSES.map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>
      </div>
      <p className="muted" aria-live="polite">
        Showing {shown.length} of {jobs.length}
      </p>
      {shown.length > 0 ? (
        <ul className="cards">
          {shown.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </ul>
      ) : (
        <p className="empty">No jobs match. Try a different search.</p>
      )}
    </>
  );
}
