import Link from "next/link";
import { Suspense } from "react";
import { notFound } from "next/navigation";
import { MENU, formatPrice, getItem } from "@/lib/menu";

// Build a page for every menu item ahead of time.
export function generateStaticParams() {
  return MENU.map((item) => ({ slug: item.slug }));
}

// The page doesn't wait for the URL itself: it hands `params` to a component inside <Suspense>,
// so Next.js can show the page's frame straight away while the item loads.
export default function MenuItemPage({ params }: PageProps<"/menu/[slug]">) {
  return (
    <Suspense fallback={<p>Loading…</p>}>
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
    <article>
      <Link href="/menu">← Back to the menu</Link>
      <p>{item.category}</p>
      <h1>{item.name}</h1>
      <p>{formatPrice(item.price)}</p>
      <p>{item.description}</p>
      {item.vegetarian && <p>Vegetarian</p>}
    </article>
  );
}
