import MenuCard from "@/components/MenuCard";
import { FEATURED, getItem, type MenuItem } from "@/lib/menu";

export default function HomePage() {
  const featured = FEATURED.map((slug) => getItem(slug)).filter((item): item is MenuItem => item !== undefined);

  return (
    <>
      <h1>Corner Café</h1>
      <p>Good coffee. Good company.</p>

      <h2>Customer favourites</h2>
      {featured.map((item) => (
        <MenuCard key={item.slug} item={item} />
      ))}
    </>
  );
}
