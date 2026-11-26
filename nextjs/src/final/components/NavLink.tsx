"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

// A Client Component: it needs the browser's current URL to highlight the active link.
export default function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  const pathname = usePathname();
  const active = href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <Link
      href={href}
      aria-current={active ? "page" : undefined}
      className={`rounded-full px-3 py-1.5 transition ${
        active ? "bg-amber-400 text-stone-900" : "text-stone-100 hover:bg-white/10"
      }`}
    >
      {children}
    </Link>
  );
}
