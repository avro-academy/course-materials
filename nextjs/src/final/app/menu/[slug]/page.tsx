import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { Suspense } from "react";
import { notFound } from "next/navigation";
import VegBadge from "@/components/VegBadge";
import { MENU, formatPrice, getItem } from "@/lib/menu";

// Build a page for every menu item ahead of time.
export function generateStaticParams() {
  return MENU.map((item) => ({ slug: item.slug }));
}

export async function generateMetadata({ params }: PageProps<"/menu/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  const item = getItem(slug);
  if (!item) return { title: "Not found" };
  return {
    title: item.name,
    description: item.description,
    openGraph: { images: [`/menu/${item.slug}.jpg`] },
  };
}

// The page doesn't wait for the URL itself: it hands `params` to a component inside <Suspense>,
// so Next.js can show the page's frame straight away while the item loads.
export default function MenuItemPage({ params }: PageProps<"/menu/[slug]">) {
  return (
    <Suspense fallback={<p className="py-16 text-center text-stone-400">Loading…</p>}>
      <MenuItem params={params} />
    </Suspense>
  );
}

async function MenuItem({ params }: Pick<PageProps<"/menu/[slug]">, "params">) {
  const { slug } = await params;
  const item = getItem(slug);

  if (!item) {
    notFound();
  }

  return (
    <article className="grid gap-8 py-4 md:grid-cols-2">
      <Image
        src={`/menu/${item.slug}.jpg`}
        alt={item.name}
        width={800}
        height={600}
        className="aspect-[4/3] w-full rounded-2xl object-cover shadow-sm"
        loading="eager"
      />
      <div>
        <Link href="/menu" className="text-sm font-semibold text-amber-700 hover:underline">
          ← Back to the menu
        </Link>
        <p className="mt-4 text-sm font-bold uppercase tracking-wide text-stone-500">{item.category}</p>
        <h1 className="mt-1 text-4xl font-extrabold">{item.name}</h1>
        <p className="mt-2 text-2xl font-semibold text-stone-700">{formatPrice(item.price)}</p>
        <p className="mt-4 text-lg text-stone-700">{item.description}</p>
        {item.vegetarian && (
          <p className="mt-4">
            <VegBadge />
          </p>
        )}
      </div>
    </article>
  );
}
