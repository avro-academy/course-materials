// Draws the menu pictures, app icon and share image for Corner Café. Usage: node make_images.js <app folder>
const { chromium } = require("playwright");
const path = require("path");
const out = process.argv[2];
const ITEMS = [
  ["flat-white", "☕", "#7c4a2d", "#f3d9b1"], ["latte", "☕", "#a0673f", "#fbe7c6"], ["cappuccino", "☕", "#5b3a29", "#e9c9a0"],
  ["long-black", "☕", "#2b1d16", "#c79a6b"], ["chai-latte", "🍵", "#b45309", "#fde3b0"], ["english-breakfast", "🫖", "#7f1d1d", "#fecaca"],
  ["hot-chocolate", "🍫", "#3f2a1e", "#d9b38c"], ["berry-smoothie", "🍓", "#9d174d", "#fbcfe8"], ["orange-juice", "🍊", "#c2410c", "#fed7aa"],
  ["banana-bread", "🍌", "#92400e", "#fde68a"], ["toastie", "🥪", "#a16207", "#fef3c7"], ["veggie-wrap", "🌯", "#3f6212", "#d9f99d"],
  ["lemon-slice", "🍋", "#a16207", "#fef9c3"], ["muffin", "🧁", "#be185d", "#fce7f3"],
];
const page = (w, h, body) => `<html><body style="margin:0;width:${w}px;height:${h}px;overflow:hidden;font-family:'Nunito','DejaVu Sans',sans-serif">${body}</body></html>`;
(async () => {
  const browser = await chromium.launch();
  const p = await browser.newPage();
  for (const [slug, emoji, dark, light] of ITEMS) {
    await p.setViewportSize({ width: 800, height: 600 });
    await p.setContent(page(800, 600, `<div style="width:800px;height:600px;position:relative;background:radial-gradient(circle at 30% 25%, ${light}, ${dark} 120%)">
      <div style="position:absolute;width:520px;height:520px;border-radius:50%;left:140px;top:40px;background:rgba(255,255,255,.35)"></div>
      <div style="position:absolute;width:420px;height:420px;border-radius:50%;left:190px;top:90px;background:rgba(255,255,255,.55);box-shadow:0 30px 60px rgba(0,0,0,.18)"></div>
      <div style="position:absolute;left:0;right:0;top:150px;text-align:center;font-size:250px;line-height:1;font-family:'Noto Color Emoji'">${emoji}</div>
      <div style="position:absolute;width:90px;height:90px;border-radius:50%;left:60px;top:440px;background:${dark};opacity:.25"></div>
      <div style="position:absolute;width:50px;height:50px;border-radius:50%;left:680px;top:70px;background:${dark};opacity:.2"></div></div>`));
    await p.screenshot({ path: path.join(out, "public/menu", slug + ".jpg"), type: "jpeg", quality: 82 });
  }
  await p.setViewportSize({ width: 512, height: 512 });
  await p.setContent(page(512, 512, `<div style="width:512px;height:512px;border-radius:112px;background:#fbbf24;display:flex;align-items:center;justify-content:center;font-size:330px;font-family:'Noto Color Emoji'">☕</div>`));
  await p.screenshot({ path: path.join(out, "app/icon.png"), omitBackground: true });
  await p.setViewportSize({ width: 1200, height: 630 });
  await p.setContent(page(1200, 630, `<div style="width:1200px;height:630px;background:#1c1917;color:#fff;position:relative">
    <div style="position:absolute;left:80px;top:150px"><div style="font-size:30px;font-weight:800;color:#fbbf24;letter-spacing:2px">NEWTOWN · SYDNEY</div>
    <div style="font-size:92px;font-weight:900;margin-top:10px">Corner Café</div>
    <div style="font-size:40px;color:#d6d3d1;margin-top:10px">Good coffee. Good company.</div>
    <div style="display:inline-block;margin-top:40px;background:#fbbf24;color:#1c1917;font-size:30px;font-weight:800;padding:14px 30px;border-radius:999px">Open every day from 7am</div></div>
    <div style="position:absolute;right:60px;top:160px;width:300px;height:300px;border-radius:50%;background:#fbbf24;display:flex;align-items:center;justify-content:center;font-size:180px;font-family:'Noto Color Emoji'">☕</div></div>`));
  await p.screenshot({ path: path.join(out, "app/opengraph-image.png") });
  await browser.close();
  console.log("images done");
})();
