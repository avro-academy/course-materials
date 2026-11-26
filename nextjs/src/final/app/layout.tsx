import type { Metadata } from "next";
import { Nunito } from "next/font/google";
import SiteHeader from "@/components/SiteHeader";
import SiteFooter from "@/components/SiteFooter";
import "./globals.css";

const nunito = Nunito({
  variable: "--font-nunito",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.SITE_URL ?? "http://localhost:3000"),
  title: {
    template: "%s | Corner Café",
    default: "Corner Café — coffee, food and good company",
  },
  description: "A friendly neighbourhood café in Sydney. See the menu, today's special and book a table.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${nunito.variable} antialiased`}>
      <body className="font-sans">
        <SiteHeader />
        <main className="mx-auto max-w-5xl p-4">{children}</main>
        <SiteFooter />
      </body>
    </html>
  );
}
