import { useNavigate } from "react-router";
import JobForm from "../components/JobForm";
import { EMPTY_JOB, type Job, type JobInput } from "../types";

export default function NewJobPage({ onAdd }: { onAdd: (job: Job) => void }) {
  const navigate = useNavigate();

  function handleSave(input: JobInput) {
    const job = { ...input, id: crypto.randomUUID() }; // a unique id for the new job
    onAdd(job);
    navigate(`/jobs/${job.id}`);
  }

  return (
    <>
      <h1>Add a job</h1>
      <JobForm initial={EMPTY_JOB} submitLabel="Save job" onSave={handleSave} />
    </>
  );
}
