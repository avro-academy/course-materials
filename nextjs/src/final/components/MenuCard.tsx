import Image from "next/image";
import Link from "next/link";
import { formatPrice, type MenuItem } from "@/lib/menu";
import VegBadge from "./VegBadge";

type Props = {
  item: MenuItem;
  eager?: boolean; // load the image straight away (for cards at the top of the page)
};

export default function MenuCard({ item, eager = false }: Props) {
  return (
    <Link
      href={`/menu/${item.slug}`}
      className="group block overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-stone-200 transition hover:shadow-md"
    >
      <Image
        src={`/menu/${item.slug}.jpg`}
        alt={item.name}
        width={800}
        height={600}
        className="aspect-[4/3] w-full object-cover"
        loading={eager ? "eager" : "lazy"}
      />
      <div className="p-4">
        <div className="flex items-baseline justify-between gap-2">
          <h3 className="font-semibold group-hover:text-amber-700">{item.name}</h3>
          <span className="font-semibold text-stone-700">{formatPrice(item.price)}</span>
        </div>
        <p className="mt-1 text-sm text-stone-600">{item.description}</p>
        {item.vegetarian && (
          <p className="mt-2">
            <VegBadge />
          </p>
        )}
      </div>
    </Link>
  );
}
