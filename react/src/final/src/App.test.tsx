import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { describe, expect, it } from "vitest";
import App from "./App";
import JobsProvider from "./state/JobsProvider";

function renderApp(path = "/") {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <JobsProvider>
        <App />
      </JobsProvider>
    </MemoryRouter>,
  );
}

describe("Job Tracker", () => {
  it("shows the sample jobs the first time", () => {
    renderApp("/jobs");
    expect(screen.getByText("Showing 3 of 3")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Casual barista" })).toBeInTheDocument();
  });

  it("filters from the address", () => {
    renderApp("/jobs?status=Saved");
    expect(screen.getByText("Showing 1 of 3")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Weekend assistant" })).toBeInTheDocument();
  });

  it("adds a job, shows it, and saves it in the browser", async () => {
    const user = userEvent.setup();
    renderApp("/jobs/new");
    await user.type(screen.getByLabelText("Job title"), "Kitchen hand");
    await user.type(screen.getByLabelText("Company"), "Pizza Place");
    await user.click(screen.getByRole("button", { name: "Save job" }));

    expect(screen.getByRole("heading", { level: 1, name: "Kitchen hand" })).toBeInTheDocument();
    expect(localStorage.getItem("job-tracker.jobs")).toContain("Pizza Place");

    await user.click(screen.getByRole("link", { name: "My jobs" }));
    expect(screen.getByText("Showing 4 of 4")).toBeInTheDocument();
  });

  it("shows what to fix when the form is empty", async () => {
    const user = userEvent.setup();
    renderApp("/jobs/new");
    await user.click(screen.getByRole("button", { name: "Save job" }));
    expect(screen.getByRole("alert")).toHaveTextContent("Please fix the highlighted fields.");
    expect(screen.getByText("Enter the job title.")).toBeInTheDocument();
  });

  it("changes a status from the job's page", async () => {
    const user = userEvent.setup();
    renderApp("/jobs/sample-3");
    const buttons = within(screen.getByRole("group", { name: "Change status" }));
    await user.click(buttons.getByRole("button", { name: "Applied" }));
    expect(buttons.getByRole("button", { name: "Applied" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.queryByText("Not yet")).not.toBeInTheDocument();
  });
});
