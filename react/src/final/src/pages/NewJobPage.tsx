import { useNavigate } from "react-router";
import JobForm from "../components/JobForm";
import { useJobs } from "../state/useJobs";
import { EMPTY_JOB, type JobInput } from "../types";

export default function NewJobPage() {
  const { dispatch } = useJobs();
  const navigate = useNavigate();

  function handleSave(input: JobInput) {
    const job = { ...input, id: crypto.randomUUID() }; // a unique id for the new job
    dispatch({ type: "added", job });
    navigate(`/jobs/${job.id}`);
  }

  return (
    <>
      <h1>Add a job</h1>
      <JobForm initial={EMPTY_JOB} submitLabel="Save job" onSave={handleSave} />
    </>
  );
}
