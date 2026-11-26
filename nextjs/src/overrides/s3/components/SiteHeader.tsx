import Link from "next/link";

export default function SiteHeader() {
  return (
    <header>
      <nav className="flex gap-4 p-4">
        <Link href="/">Home</Link>
        <Link href="/menu">Menu</Link>
        <Link href="/about">About</Link>
      </nav>
    </header>
  );
}
