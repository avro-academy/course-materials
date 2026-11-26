"use client";

import { useState } from "react";
import { CATEGORIES, type Category, type MenuItem } from "@/lib/menu";
import MenuCard from "./MenuCard";

// Runs in the browser, so it can use state: the list updates as you type or click.
export default function MenuFilter({ items }: { items: MenuItem[] }) {
  const [category, setCategory] = useState<Category | "All">("All");
  const [search, setSearch] = useState("");

  const shown = items.filter(
    (item) =>
      (category === "All" || item.category === category) &&
      item.name.toLowerCase().includes(search.trim().toLowerCase()),
  );

  return (
    <div>
      <div className="flex flex-wrap items-center gap-2">
        {(["All", ...CATEGORIES] as const).map((c) => (
          <button
            key={c}
            type="button"
            onClick={() => setCategory(c)}
            aria-pressed={category === c}
            className={`rounded-full px-4 py-1.5 text-sm font-medium ring-1 ring-stone-300 ${
              category === c ? "bg-stone-900 text-white" : "bg-white hover:bg-stone-100"
            }`}
          >
            {c}
          </button>
        ))}
        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search the menu…"
          aria-label="Search the menu"
          className="ml-auto w-full rounded-full border border-stone-300 px-4 py-1.5 text-sm sm:w-56"
        />
      </div>

      <p className="mt-4 text-sm text-stone-600" aria-live="polite">
        Showing {shown.length} of {items.length} items
      </p>

      {shown.length > 0 ? (
        <div className="mt-4 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {shown.map((item, index) => (
            <MenuCard key={item.slug} item={item} eager={index < 3} />
          ))}
        </div>
      ) : (
        <p className="mt-8 text-center text-stone-600">Nothing matches — try another search.</p>
      )}
    </div>
  );
}
