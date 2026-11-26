import { describe, expect, it } from "vitest";
import { sampleJobs } from "./sampleJobs";
import { countByStatus, filterJobs, followUpsDue } from "./stats";

const jobs = sampleJobs("2026-03-10");

describe("filterJobs", () => {
  it("returns everything with no search or filter", () => {
    expect(filterJobs(jobs, "", "")).toHaveLength(3);
  });
  it("searches company, role and place, ignoring case and spaces", () => {
    expect(filterJobs(jobs, "  SYDNEY ", "").map((j) => j.id)).toEqual(["sample-1", "sample-3"]);
    expect(filterJobs(jobs, "barista", "")).toHaveLength(1);
  });
  it("combines the search with the status filter", () => {
    expect(filterJobs(jobs, "sydney", "Saved").map((j) => j.company)).toEqual(["Local library"]);
  });
});

describe("countByStatus", () => {
  it("counts every status, including zeros", () => {
    expect(countByStatus(jobs)).toEqual({ Saved: 1, Applied: 1, Interview: 1, Offer: 0, Rejected: 0 });
  });
});

describe("followUpsDue", () => {
  it("lists follow-ups in the next 7 days, soonest first", () => {
    expect(followUpsDue(jobs, "2026-03-10").map((j) => j.id)).toEqual(["sample-1"]);
  });
  it("includes overdue ones but skips offers and rejections", () => {
    const old = jobs.map((j) => ({ ...j, followUp: "2026-03-01" }));
    old[1].status = "Rejected";
    expect(followUpsDue(old, "2026-03-10").map((j) => j.id)).toEqual(["sample-1", "sample-3"]);
  });
});
