import Link from "next/link";

export default function NotFound() {
  return (
    <div>
      <p>🥐</p>
      <h1>We couldn&apos;t find that page</h1>
      <p>Maybe it sold out? Try the menu instead.</p>
      <Link href="/menu">
        See the menu
      </Link>
    </div>
  );
}
