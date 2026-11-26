import { NavLink, Outlet } from "react-router";

// The frame around every page. <Outlet /> is where the current page appears.
export default function Layout() {
  return (
    <>
      <header className="site-header">
        <NavLink to="/" className="logo">
          📋 Job Tracker
        </NavLink>
        <nav>
          <NavLink to="/" end>
            Dashboard
          </NavLink>
          <NavLink to="/jobs" end>
            My jobs
          </NavLink>
          <NavLink to="/jobs/new" className="button">
            + Add a job
          </NavLink>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer className="site-footer">Saved in this browser only · A practice app from Avro Academy</footer>
    </>
  );
}
