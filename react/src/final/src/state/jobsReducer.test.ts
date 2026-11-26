import { describe, expect, it } from "vitest";
import type { Job } from "../types";
import { jobsReducer } from "./jobsReducer";

const saved: Job = {
  id: "1", company: "Café", role: "Barista", location: "", status: "Saved",
  appliedOn: "", followUp: "", link: "", notes: "",
};

describe("jobsReducer", () => {
  it("adds new jobs to the top", () => {
    const next = jobsReducer([saved], { type: "added", job: { ...saved, id: "2" } });
    expect(next.map((j) => j.id)).toEqual(["2", "1"]);
  });
  it("fills in today's date when a saved job moves to Applied", () => {
    const [job] = jobsReducer([saved], { type: "statusChanged", id: "1", status: "Applied", today: "2026-03-10" });
    expect(job).toMatchObject({ status: "Applied", appliedOn: "2026-03-10" });
  });
  it("keeps the original applied date on later status changes", () => {
    const applied = { ...saved, status: "Applied" as const, appliedOn: "2026-03-01" };
    const [job] = jobsReducer([applied], { type: "statusChanged", id: "1", status: "Interview", today: "2026-03-10" });
    expect(job.appliedOn).toBe("2026-03-01");
  });
  it("never changes the original list (it makes a new one)", () => {
    const list = [saved];
    jobsReducer(list, { type: "deleted", id: "1" });
    expect(list).toEqual([saved]);
  });
});
