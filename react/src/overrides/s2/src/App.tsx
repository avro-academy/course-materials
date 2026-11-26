import JobCard from "./components/JobCard";
import { sampleJobs } from "./lib/sampleJobs";

// For now the list is fixed. In the next step it becomes state, so it can change.
const jobs = sampleJobs();

export default function App() {
  return (
    <>
      <header className="site-header">
        <span className="logo">📋 Job Tracker</span>
      </header>
      <main>
        <h1>My jobs</h1>
        <ul className="cards">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </ul>
      </main>
      <footer className="site-footer">A practice app from Avro Academy</footer>
    </>
  );
}
