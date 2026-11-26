import { useState } from "react";
import JobCard from "./components/JobCard";
import { todayISO } from "./lib/dates";
import { sampleJobs } from "./lib/sampleJobs";
import { filterJobs } from "./lib/stats";
import { STATUSES, type Job, type Status } from "./types";

export default function App() {
  // State: values React remembers between renders. Changing them redraws the screen.
  const [jobs, setJobs] = useState<Job[]>(() => sampleJobs());
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<Status | "">("");

  // Not state: worked out from state every time the component renders.
  const shown = filterJobs(jobs, search, status);

  // The jobs live here, in the parent, so this is where they're changed. JobCard calls this.
  function changeStatus(id: string, newStatus: Status) {
    setJobs(
      jobs.map((job) =>
        job.id === id
          ? { ...job, status: newStatus, appliedOn: newStatus !== "Saved" && job.appliedOn === "" ? todayISO() : job.appliedOn }
          : job,
      ),
    );
  }

  return (
    <>
      <header className="site-header">
        <span className="logo">📋 Job Tracker</span>
      </header>
      <main>
        <h1>My jobs</h1>
        <div className="filters">
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search company, role or place…"
            aria-label="Search jobs"
          />
          <select value={status} onChange={(e) => setStatus(e.target.value as Status | "")} aria-label="Filter by status">
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
              <JobCard key={job.id} job={job} onStatusChange={changeStatus} />
            ))}
          </ul>
        ) : (
          <p className="empty">No jobs match. Try a different search.</p>
        )}
      </main>
      <footer className="site-footer">A practice app from Avro Academy</footer>
    </>
  );
}
