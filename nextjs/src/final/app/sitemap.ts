import type { MetadataRoute } from "next";
import { MENU } from "@/lib/menu";

const SITE = process.env.SITE_URL ?? "http://localhost:3000";

export default function sitemap(): MetadataRoute.Sitemap {
  const pages = ["", "/menu", "/book", "/about"].map((path) => ({ url: `${SITE}${path}` }));
  const items = MENU.map((item) => ({ url: `${SITE}/menu/${item.slug}` }));
  return [...pages, ...items];
}
