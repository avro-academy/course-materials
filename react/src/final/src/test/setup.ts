import "@testing-library/jest-dom/vitest"; // adds checks like toBeInTheDocument()
import { cleanup } from "@testing-library/react";
import { afterEach, beforeEach } from "vitest";

beforeEach(() => localStorage.clear()); // every test starts with no saved jobs
afterEach(() => cleanup()); // remove what the last test rendered
