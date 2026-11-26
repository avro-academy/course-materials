import { Link } from "react-router";

export default function NotFoundPage() {
  return (
    <div className="empty">
      <h1>Page not found</h1>
      <p>That page or job doesn&apos;t exist. It might have been deleted.</p>
      <p>
        <Link to="/jobs">Go to My jobs</Link>
      </p>
    </div>
  );
}
