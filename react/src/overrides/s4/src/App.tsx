import { useState } from "react";
import JobCard from "./components/JobCard";
import JobForm from "./components/JobForm";
import { todayISO } from "./lib/dates";
import { sampleJobs } from "./lib/sampleJobs";
import { filterJobs } from "./lib/stats";
import { EMPTY_JOB, STATUSES, type Job, type JobInput, type Status } from "./types";

export default function App() {
  const [jobs, setJobs] = useState<Job[]>(() => sampleJobs());
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<Status | "">("");
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  const shown = filterJobs(jobs, search, status);
  const editing = jobs.find((job) => job.id === editingId);

  function changeStatus(id: string, newStatus: Status) {
    setJobs(
      jobs.map((job) =>
        job.id === id
          ? { ...job, status: newStatus, appliedOn: newStatus !== "Saved" && job.appliedOn === "" ? todayISO() : job.appliedOn }
          : job,
      ),
    );
  }

  function addJob(input: JobInput) {
    const job = { ...input, id: crypto.randomUUID() }; // a unique id for the new job
    setJobs([job, ...jobs]);
    setShowForm(false);
  }

  function updateJob(changes: JobInput) {
    setJobs(jobs.map((job) => (job.id === editingId ? { ...changes, id: job.id } : job)));
    setEditingId(null);
  }

  function deleteJob(id: string) {
    const job = jobs.find((j) => j.id === id);
    if (job && window.confirm(`Delete "${job.role}" at ${job.company}?`)) {
      setJobs(jobs.filter((j) => j.id !== id));
      if (editingId === id) setEditingId(null);
    }
  }

  return (
    <>
      <header className="site-header">
        <span className="logo">📋 Job Tracker</span>
      </header>
      <main>
        <div className="toolbar">
          <h1>My jobs</h1>
          <button type="button" className="button" onClick={() => setShowForm(!showForm)}>
            {showForm ? "Cancel" : "Add a job"}
          </button>
        </div>

        {showForm && (
          <section className="panel">
            <h2>Add a job</h2>
            <JobForm initial={EMPTY_JOB} submitLabel="Save job" onSave={addJob} />
          </section>
        )}

        {editing && (
          <section className="panel">
            <h2>Edit job</h2>
            {/* key: a different job gives a brand-new form, so it starts with that job's details. */}
            <JobForm key={editing.id} initial={editing} submitLabel="Save changes" onSave={updateJob} />
            <button type="button" className="link-button" onClick={() => setEditingId(null)}>
              Cancel
            </button>
          </section>
        )}

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
              <JobCard key={job.id} job={job} onStatusChange={changeStatus} onEdit={setEditingId} onDelete={deleteJob} />
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
