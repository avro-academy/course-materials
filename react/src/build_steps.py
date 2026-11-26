"""Builds step-1-start ... step-8-final of the Job Tracker from final/, overrides/ and pkg/. Usage: python build_steps.py <out>"""
import os, shutil, sys
H = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(H, "final"); OUT = sys.argv[1]
STEPS = ["step-1-start", "step-2-components", "step-3-state", "step-4-forms", "step-5-effects", "step-6-router", "step-7-context", "step-8-final"]
VITE_PLAIN = '''import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
});
'''
def cp(step, rel, src=F, dest=None):
    s = os.path.join(src, rel); d = os.path.join(OUT, step, dest or rel); os.makedirs(os.path.dirname(d), exist_ok=True)
    (shutil.copytree if os.path.isdir(s) else shutil.copy)(s, d, **({"dirs_exist_ok": True} if os.path.isdir(s) else {}))
def ov(step, key, rel): cp(step, rel, os.path.join(H, "overrides", key))
FINAL_SRC = ["src/types.ts", "src/lib/dates.ts", "src/lib/sampleJobs.ts", "src/components/StatusBadge.tsx"]
for i, step in enumerate(STEPS, 1):
    for f in ["index.html", "public/icon.svg", ".gitignore", ".oxlintrc.json", "tsconfig.app.json", "tsconfig.json", "tsconfig.node.json"]:
        cp(step, f)
    pkg = "base" if i <= 5 else "router" if i <= 7 else "final"
    for f in ["package.json", "package-lock.json"]: cp(step, f, os.path.join(H, "pkg", pkg))
    if i < 8:
        os.makedirs(os.path.join(OUT, step), exist_ok=True); open(os.path.join(OUT, step, "vite.config.ts"), "w").write(VITE_PLAIN)
    if i == 1:
        for f in ["src/main.tsx", "src/App.tsx", "src/index.css"]: ov(step, "s1", f)
        continue
    if i <= 5:
        ov(step, "s1", "src/main.tsx")
        for f in FINAL_SRC + ["src/index.css"]: cp(step, f)
    if i == 2:
        for f in ["src/App.tsx", "src/components/JobCard.tsx"]: ov(step, "s2", f)
    if i == 3:
        for f in ["src/App.tsx", "src/components/JobCard.tsx", "src/lib/stats.ts"]: ov(step, "s3", f)
    if i in (4, 5):
        ov(step, "s3", "src/lib/stats.ts")
        for f in ["src/lib/validate.ts", "src/components/JobForm.tsx"]: cp(step, f)
        for f in ["src/App.tsx", "src/components/JobCard.tsx"]: ov(step, f"s{i}", f)
    if i == 5:
        for f in ["src/hooks/useLocalStorage.ts", "src/components/Tips.tsx"]: ov(step, "s5", f)
        cp(step, "public/tips.json")
    if i == 6:
        cp(step, "src"); cp(step, "public")
        shutil.rmtree(os.path.join(OUT, step, "src/state")); os.remove(os.path.join(OUT, step, "src/lib/storage.ts"))
        shutil.rmtree(os.path.join(OUT, step, "src/test"))
        for t in ["src/App.test.tsx", "src/lib/stats.test.ts", "src/lib/validate.test.ts"]: os.remove(os.path.join(OUT, step, t))
        for f in ["src/main.tsx", "src/App.tsx", "src/hooks/useLocalStorage.ts", "src/pages/DashboardPage.tsx", "src/pages/JobsPage.tsx",
                  "src/pages/NewJobPage.tsx", "src/pages/EditJobPage.tsx", "src/pages/JobDetailPage.tsx"]:
            ov(step, "s6", f)
    if i == 7:
        cp(step, "src"); cp(step, "public")
        shutil.rmtree(os.path.join(OUT, step, "src/test"))
        for root, _, files in os.walk(os.path.join(OUT, step, "src")):
            for f in files:
                if ".test." in f: os.remove(os.path.join(root, f))
    if i == 8:
        for f in ["src", "public", "vite.config.ts", "vercel.json"]: cp(step, f)
print("built", len(STEPS), "steps")
