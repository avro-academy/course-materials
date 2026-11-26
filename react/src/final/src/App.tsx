import { useEffect } from "react";
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import DashboardPage from "./pages/DashboardPage";
import EditJobPage from "./pages/EditJobPage";
import JobDetailPage from "./pages/JobDetailPage";
import JobsPage from "./pages/JobsPage";
import NewJobPage from "./pages/NewJobPage";
import NotFoundPage from "./pages/NotFoundPage";
import { useJobs } from "./state/useJobs";

// Just the list of pages. The jobs live in <JobsProvider>, so no props are needed.
export default function App() {
  const { jobs } = useJobs();

  useEffect(() => {
    document.title = `Job Tracker (${jobs.length})`;
  }, [jobs.length]);

  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<DashboardPage />} />
        <Route path="jobs" element={<JobsPage />} />
        <Route path="jobs/new" element={<NewJobPage />} />
        <Route path="jobs/:id" element={<JobDetailPage />} />
        <Route path="jobs/:id/edit" element={<EditJobPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
