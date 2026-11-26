// A component is a function that returns what should appear on the screen.
export default function App() {
  // Ordinary JavaScript can go here, before the return.
  const name = "Job Tracker";
  const tagline = "Keep track of every job you apply for — all in one place.";

  return (
    <main>
      <h1>📋 {name}</h1>
      <p>{tagline}</p>
      <p className="small">Your first React component. Edit src/App.tsx and save to see it change.</p>
    </main>
  );
}
