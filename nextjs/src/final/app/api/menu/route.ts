import { CATEGORIES, MENU, type Category } from "@/lib/menu";

// GET /api/menu            → the whole menu as JSON
// GET /api/menu?category=Tea → just one category
export async function GET(request: Request) {
  const category = new URL(request.url).searchParams.get("category");

  if (category === null) {
    return Response.json(MENU);
  }
  if (!CATEGORIES.includes(category as Category)) {
    return Response.json({ error: `Unknown category. Try one of: ${CATEGORIES.join(", ")}` }, { status: 400 });
  }
  return Response.json(MENU.filter((item) => item.category === category));
}
