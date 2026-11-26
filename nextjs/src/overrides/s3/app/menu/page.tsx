import MenuCard from "@/components/MenuCard";
import { MENU } from "@/lib/menu";

export default function MenuPage() {
  return (
    <>
      <h1>Our menu</h1>
      {MENU.map((item) => (
        <MenuCard key={item.slug} item={item} />
      ))}
    </>
  );
}
