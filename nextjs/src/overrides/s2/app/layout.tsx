import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Corner Café",
  description: "A friendly neighbourhood café in Sydney.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>
        <main className="mx-auto max-w-5xl p-4">{children}</main>
      </body>
    </html>
  );
}
