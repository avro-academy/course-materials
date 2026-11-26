export type Category = "Coffee" | "Tea" | "Drinks" | "Food";

export type MenuItem = {
  slug: string; // used in the URL: /menu/flat-white
  name: string;
  category: Category;
  price: number; // in dollars
  description: string;
  vegetarian: boolean;
};

export const CATEGORIES: Category[] = ["Coffee", "Tea", "Drinks", "Food"];

export const MENU: MenuItem[] = [
  { slug: "flat-white", name: "Flat white", category: "Coffee", price: 4.8, vegetarian: true,
    description: "Our most popular coffee: a double shot with silky steamed milk." },
  { slug: "latte", name: "Latte", category: "Coffee", price: 4.8, vegetarian: true,
    description: "A double shot with plenty of steamed milk and a little foam." },
  { slug: "cappuccino", name: "Cappuccino", category: "Coffee", price: 4.8, vegetarian: true,
    description: "Espresso, steamed milk and a thick layer of foam, dusted with chocolate." },
  { slug: "long-black", name: "Long black", category: "Coffee", price: 4.2, vegetarian: true,
    description: "A double shot poured over hot water. Strong and simple." },
  { slug: "chai-latte", name: "Chai latte", category: "Tea", price: 5.2, vegetarian: true,
    description: "Spiced black tea brewed with honey and steamed milk." },
  { slug: "english-breakfast", name: "English breakfast tea", category: "Tea", price: 4.0, vegetarian: true,
    description: "A pot of strong black tea, with milk on the side." },
  { slug: "hot-chocolate", name: "Hot chocolate", category: "Drinks", price: 5.0, vegetarian: true,
    description: "Real melted chocolate and steamed milk, with a marshmallow." },
  { slug: "berry-smoothie", name: "Mixed berry smoothie", category: "Drinks", price: 7.5, vegetarian: true,
    description: "Strawberries, blueberries, banana and yoghurt, blended to order." },
  { slug: "orange-juice", name: "Orange juice", category: "Drinks", price: 5.5, vegetarian: true,
    description: "Freshly squeezed every morning." },
  { slug: "banana-bread", name: "Banana bread", category: "Food", price: 5.5, vegetarian: true,
    description: "A thick slice, toasted, with butter. Baked here every day." },
  { slug: "toastie", name: "Ham and cheese toastie", category: "Food", price: 9.5, vegetarian: false,
    description: "Leg ham and melted cheddar on sourdough, toasted until crunchy." },
  { slug: "veggie-wrap", name: "Veggie wrap", category: "Food", price: 11.0, vegetarian: true,
    description: "Roast pumpkin, hummus, spinach and feta in a grilled wrap." },
  { slug: "lemon-slice", name: "Lemon slice", category: "Food", price: 4.5, vegetarian: true,
    description: "Zesty lemon on a buttery coconut base." },
  { slug: "muffin", name: "Raspberry muffin", category: "Food", price: 5.0, vegetarian: true,
    description: "Fluffy, fruity and still warm if you're early." },
];

// The "customer favourites" on the home page, by slug.
export const FEATURED: string[] = ["flat-white", "banana-bread", "chai-latte"];

export function getItem(slug: string): MenuItem | undefined {
  return MENU.find((item) => item.slug === slug);
}

export function formatPrice(price: number): string {
  return new Intl.NumberFormat("en-AU", { style: "currency", currency: "AUD" }).format(price);
}
