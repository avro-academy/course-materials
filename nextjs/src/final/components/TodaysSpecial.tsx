import Image from "next/image";
import Link from "next/link";
import { connection } from "next/server";
import { cafeClock } from "@/lib/hours";
import { formatPrice, getItem } from "@/lib/menu";
import { SPECIALS } from "@/lib/specials";

// The special changes with the day of the week (in Sydney), so it's worked out for each visit.
export default async function TodaysSpecial() {
  await connection();
  const { day } = cafeClock(new Date());
  const special = SPECIALS[day];
  const item = getItem(special.slug);
  if (!item) return null;

  return (
    <Link
      href={`/menu/${item.slug}`}
      className="flex flex-col overflow-hidden rounded-2xl bg-amber-100 ring-1 ring-amber-200 transition hover:shadow-md sm:flex-row"
    >
      <Image
        src={`/menu/${item.slug}.jpg`}
        alt={item.name}
        width={800}
        height={600}
        className="aspect-[4/3] w-full object-cover sm:w-64"
      />
      <div className="p-5">
        <p className="text-sm font-bold uppercase tracking-wide text-amber-800">{day}&apos;s special</p>
        <h2 className="mt-1 text-2xl font-extrabold">{special.deal}</h2>
        <p className="mt-2 text-stone-700">
          {item.name} — usually {formatPrice(item.price)}
        </p>
      </div>
    </Link>
  );
}
