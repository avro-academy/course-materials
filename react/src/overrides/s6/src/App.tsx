import { useEffect } from "react";
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import { useLocalStorage } from "./hooks/useLocalStorage";
import { todayISO } from "./lib/dates";
import { sampleJobs } from "./lib/sampleJobs";
import DashboardPage from "./pages/DashboardPage";
import EditJobPage from "./pages/EditJobPage";
import JobDetailPage from "./pages/JobDetailPage";
import JobsPage from "./pages/JobsPage";
import NewJobPage from "./pages/NewJobPage";
import NotFoundPage from "./pages/NotFoundPage";
import type { Job, JobInput, Status } from "./types";

export default function App() {
  // The jobs still live here, at the top, and are handed down to each page as props.
  const [jobs, setJobs] = useLocalStorage<Job[]>("job-tracker.jobs", sampleJobs);

  useEffect(() => {
    document.title = `Job Tracker (${jobs.length})`;
  }, [jobs.length]);

  function addJob(job: Job) {
    setJobs([job, ...jobs]);
  }

  function updateJob(id: string, changes: JobInput) {
    setJobs(jobs.map((job) => (job.id === id ? { ...changes, id } : job)));
  }

  function changeStatus(id: string, newStatus: Status) {
    setJobs(
      jobs.map((job) =>
        job.id === id
          ? { ...job, status: newStatus, appliedOn: newStatus !== "Saved" && job.appliedOn === "" ? todayISO() : job.appliedOn }
          : job,
      ),
    );
  }

  function deleteJob(id: string) {
    setJobs(jobs.filter((job) => job.id !== id));
  }

  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<DashboardPage jobs={jobs} />} />
        <Route path="jobs" element={<JobsPage jobs={jobs} />} />
        <Route path="jobs/new" element={<NewJobPage onAdd={addJob} />} />
        <Route path="jobs/:id" element={<JobDetailPage jobs={jobs} onStatusChange={changeStatus} onDelete={deleteJob} />} />
        <Route path="jobs/:id/edit" element={<EditJobPage jobs={jobs} onUpdate={updateJob} />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
