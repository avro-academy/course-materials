import { describe, expect, it } from "vitest";
import { EMPTY_JOB } from "../types";
import { validateJob } from "./validate";

const ok = { ...EMPTY_JOB, company: "Corner Café", role: "Barista" };

describe("validateJob", () => {
  it("accepts a job with a company and a title", () => {
    expect(validateJob(ok)).toEqual({});
  });
  it("needs a company and a job title", () => {
    expect(Object.keys(validateJob(EMPTY_JOB)).sort()).toEqual(["company", "role"]);
  });
  it("only accepts web links", () => {
    expect(validateJob({ ...ok, link: "www.seek.com.au" }).link).toBeDefined();
    expect(validateJob({ ...ok, link: "https://www.seek.com.au/job/1" })).toEqual({});
  });
  it("needs an applied date once you've applied", () => {
    expect(validateJob({ ...ok, status: "Applied" }).appliedOn).toBe("Add the date you applied.");
  });
  it("won't follow up before you applied", () => {
    const job = { ...ok, status: "Applied" as const, appliedOn: "2026-03-10", followUp: "2026-03-01" };
    expect(validateJob(job).followUp).toBeDefined();
  });
});
