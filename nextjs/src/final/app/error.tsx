"use client"; // Error pages must be Client Components

export default function ErrorPage({ error, retry }: { error: unknown; retry: () => void }) {
  console.error(error);

  return (
    <div className="py-16 text-center">
      <h1 className="text-3xl font-extrabold">Something went wrong</h1>
      <p className="mt-2 text-stone-600">Sorry — that page had a problem. Please try again.</p>
      <button
        onClick={() => retry()}
        className="mt-6 rounded-full bg-stone-900 px-5 py-2.5 font-semibold text-white hover:bg-stone-700"
      >
        Try again
      </button>
    </div>
  );
}
