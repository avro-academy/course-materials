// A different special every day of the week, by menu slug.
export const SPECIALS: Record<string, { slug: string; deal: string }> = {
  Monday: { slug: "banana-bread", deal: "Banana bread and any coffee for $9" },
  Tuesday: { slug: "toastie", deal: "Toastie Tuesday: $2 off every toastie" },
  Wednesday: { slug: "berry-smoothie", deal: "Large smoothie for the price of a regular" },
  Thursday: { slug: "chai-latte", deal: "Chai latte with a free lemon slice" },
  Friday: { slug: "veggie-wrap", deal: "Veggie wrap and orange juice for $14" },
  Saturday: { slug: "muffin", deal: "Fresh raspberry muffins, two for $8" },
  Sunday: { slug: "hot-chocolate", deal: "Kids' hot chocolates half price" },
};
