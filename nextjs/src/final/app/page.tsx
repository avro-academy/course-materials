import { Suspense } from "react";
import Link from "next/link";
import MenuCard from "@/components/MenuCard";
import OpenNow from "@/components/OpenNow";
import TodaysSpecial from "@/components/TodaysSpecial";
import { FEATURED, getItem, type MenuItem } from "@/lib/menu";

export default function HomePage() {
  const featured = FEATURED.map((slug) => getItem(slug)).filter((item): item is MenuItem => item !== undefined);

  return (
    <>
      <section className="py-8">
        <Suspense fallback={<p className="text-sm text-stone-400">Checking opening hours…</p>}>
          <OpenNow />
        </Suspense>
        <h1 className="mt-3 text-4xl font-extrabold sm:text-5xl">Corner Café</h1>
        <p className="mt-2 text-lg text-stone-600">Good coffee. Good company. Open every day from 7am.</p>
        <div className="mt-5 flex flex-wrap gap-3">
          <Link href="/menu" className="rounded-full bg-stone-900 px-5 py-2.5 font-semibold text-white hover:bg-stone-700">
            See the menu
          </Link>
          <Link href="/book" className="rounded-full bg-white px-5 py-2.5 font-semibold ring-1 ring-stone-300 hover:bg-stone-100">
            Book a table
          </Link>
        </div>
      </section>

      <Suspense fallback={<div className="h-48 rounded-2xl bg-amber-50" />}>
        <TodaysSpecial />
      </Suspense>

      <h2 className="mt-12 text-2xl font-extrabold">Customer favourites</h2>
      <div className="mt-4 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {featured.map((item) => (
          <MenuCard key={item.slug} item={item} />
        ))}
      </div>
    </>
  );
}
