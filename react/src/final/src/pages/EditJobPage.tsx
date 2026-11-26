import { useNavigate, useParams } from "react-router";
import JobForm from "../components/JobForm";
import { useJobs } from "../state/useJobs";
import type { JobInput } from "../types";
import NotFoundPage from "./NotFoundPage";

export default function EditJobPage() {
  const { id } = useParams();
  const { jobs, dispatch } = useJobs();
  const navigate = useNavigate();
  const job = jobs.find((j) => j.id === id);

  if (!job) return <NotFoundPage />;

  const handleSave = (changes: JobInput) => {
    dispatch({ type: "updated", id: job.id, changes });
    navigate(`/jobs/${job.id}`);
  };

  return (
    <>
      <h1>Edit job</h1>
      <JobForm initial={job} submitLabel="Save changes" onSave={handleSave} />
    </>
  );
}
