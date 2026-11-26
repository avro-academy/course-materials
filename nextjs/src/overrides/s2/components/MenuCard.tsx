import { formatPrice, type MenuItem } from "@/lib/menu";

type Props = {
  item: MenuItem;
};

export default function MenuCard({ item }: Props) {
  return (
    <div className="border p-4">
      <h3>
        {item.name} — {formatPrice(item.price)}
      </h3>
      <p>{item.description}</p>
      {item.vegetarian && <p>Vegetarian</p>}
    </div>
  );
}
