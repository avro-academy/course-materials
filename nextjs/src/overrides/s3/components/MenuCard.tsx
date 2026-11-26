import Link from "next/link";
import { formatPrice, type MenuItem } from "@/lib/menu";

type Props = {
  item: MenuItem;
};

export default function MenuCard({ item }: Props) {
  return (
    <Link href={`/menu/${item.slug}`} className="block border p-4">
      <h3>
        {item.name} — {formatPrice(item.price)}
      </h3>
      <p>{item.description}</p>
      {item.vegetarian && <p>Vegetarian</p>}
    </Link>
  );
}
