import Link from "next/link";
import NavLink from "./NavLink";

export default function SiteHeader() {
  return (
    <header className="bg-stone-900">
      <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-3 px-4 py-3">
        <Link href="/" className="text-lg font-extrabold text-amber-400">
          ☕ Corner Café
        </Link>
        <nav className="flex flex-wrap gap-1 text-sm font-semibold">
          <NavLink href="/">Home</NavLink>
          <NavLink href="/menu">Menu</NavLink>
          <NavLink href="/book">Book a table</NavLink>
          <NavLink href="/about">About</NavLink>
        </nav>
      </div>
    </header>
  );
}
