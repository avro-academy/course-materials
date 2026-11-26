import type { Metadata } from "next";
import MenuFilter from "@/components/MenuFilter";
import { MENU } from "@/lib/menu";

export const metadata: Metadata = {
  title: "Menu",
  description: "Coffee, tea, cold drinks and food at Corner Café.",
};

export default function MenuPage() {
  return (
    <>
      <h1 className="text-3xl font-extrabold">Our menu</h1>
      <p className="mt-2 text-stone-600">Everything is made fresh in our kitchen. Prices include GST.</p>
      <div className="mt-6">
        <MenuFilter items={MENU} />
      </div>
    </>
  );
}
