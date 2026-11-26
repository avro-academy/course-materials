import { useNavigate, useParams } from "react-router";
import JobForm from "../components/JobForm";
import type { Job, JobInput } from "../types";
import NotFoundPage from "./NotFoundPage";

type Props = {
  jobs: Job[];
  onUpdate: (id: string, changes: JobInput) => void;
};

export default function EditJobPage({ jobs, onUpdate }: Props) {
  const { id } = useParams();
  const navigate = useNavigate();
  const job = jobs.find((j) => j.id === id);

  if (!job) return <NotFoundPage />;

  const handleSave = (changes: JobInput) => {
    onUpdate(job.id, changes);
    navigate(`/jobs/${job.id}`);
  };

  return (
    <>
      <h1>Edit job</h1>
      <JobForm initial={job} submitLabel="Save changes" onSave={handleSave} />
    </>
  );
}
