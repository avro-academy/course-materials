import { useEffect, useState } from "react";

type Tip = { title: string; text: string };

// Loads job-hunting tips from a JSON file, showing what's happening while it waits.
export default function Tips() {
  const [tip, setTip] = useState<Tip | null>(null);
  const [status, setStatus] = useState<"loading" | "error" | "done">("loading");

  useEffect(() => {
    let ignore = false; // if the component goes away before the data arrives, don't update it

    fetch("/tips.json")
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json() as Promise<Tip[]>;
      })
      .then((tips) => {
        if (!ignore) {
          setTip(tips[new Date().getDate() % tips.length]); // a different tip each day
          setStatus("done");
        }
      })
      .catch(() => {
        if (!ignore) setStatus("error");
      });

    return () => {
      ignore = true;
    };
  }, []);

  if (status === "loading") return <p className="muted">Loading tips…</p>;
  if (status === "error" || tip === null) return <p className="muted">Couldn't load tips right now.</p>;

  return (
    <div className="tip">
      <strong>💡 {tip.title}</strong>
      <p>{tip.text}</p>
    </div>
  );
}
