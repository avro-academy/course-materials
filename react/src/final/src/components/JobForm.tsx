import { useState } from "react";
import { validateJob, type Errors } from "../lib/validate";
import { STATUSES, type JobInput, type Status } from "../types";

type Props = {
  initial: JobInput;
  submitLabel: string;
  onSave: (job: JobInput) => void;
};

function Field({ label, error, children }: { label: string; error?: string; children: React.ReactNode }) {
  return (
    <label className={error ? "field has-error" : "field"}>
      <span>{label}</span>
      {children}
      {error && <span className="error">{error}</span>}
    </label>
  );
}

export default function JobForm({ initial, submitLabel, onSave }: Props) {
  const [job, setJob] = useState<JobInput>(initial);
  const [errors, setErrors] = useState<Errors>({});

  // One change handler for every field: copy the job, replacing just the field that changed.
  function update(field: keyof JobInput, value: string) {
    setJob({ ...job, [field]: value });
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); // stop the browser reloading the page
    const found = validateJob(job);
    setErrors(found);
    if (Object.keys(found).length === 0) {
      onSave({ ...job, company: job.company.trim(), role: job.role.trim(), location: job.location.trim() });
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="form">
      {Object.keys(errors).length > 0 && (
        <p role="alert" className="alert">
          Please fix the highlighted fields.
        </p>
      )}
      <div className="form-row">
        <Field label="Job title" error={errors.role}>
          <input value={job.role} onChange={(e) => update("role", e.target.value)} />
        </Field>
        <Field label="Company" error={errors.company}>
          <input value={job.company} onChange={(e) => update("company", e.target.value)} />
        </Field>
      </div>
      <div className="form-row">
        <Field label="Location" error={errors.location}>
          <input value={job.location} onChange={(e) => update("location", e.target.value)} />
        </Field>
        <Field label="Status">
          <select value={job.status} onChange={(e) => update("status", e.target.value as Status)}>
            {STATUSES.map((s) => (
              <option key={s}>{s}</option>
            ))}
          </select>
        </Field>
      </div>
      <div className="form-row">
        <Field label="Date applied" error={errors.appliedOn}>
          <input type="date" value={job.appliedOn} onChange={(e) => update("appliedOn", e.target.value)} />
        </Field>
        <Field label="Follow up on" error={errors.followUp}>
          <input type="date" value={job.followUp} onChange={(e) => update("followUp", e.target.value)} />
        </Field>
      </div>
      <Field label="Link to the job ad" error={errors.link}>
        <input type="url" value={job.link} placeholder="https://" onChange={(e) => update("link", e.target.value)} />
      </Field>
      <Field label={`Notes (${job.notes.length}/500)`} error={errors.notes}>
        <textarea rows={4} value={job.notes} onChange={(e) => update("notes", e.target.value)} />
      </Field>
      <button type="submit" className="button">
        {submitLabel}
      </button>
    </form>
  );
}
