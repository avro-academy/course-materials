import Link from "next/link";

export default function NotFound() {
  return (
    <div className="py-16 text-center">
      <p className="text-5xl">🥐</p>
      <h1 className="mt-4 text-3xl font-extrabold">We couldn&apos;t find that page</h1>
      <p className="mt-2 text-stone-600">Maybe it sold out? Try the menu instead.</p>
      <Link
        href="/menu"
        className="mt-6 inline-block rounded-full bg-stone-900 px-5 py-2.5 font-semibold text-white hover:bg-stone-700"
      >
        See the menu
      </Link>
    </div>
  );
}
