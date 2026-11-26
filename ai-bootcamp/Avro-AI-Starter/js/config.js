// =====================================================================
//  js/config.js: YOUR APP'S SETTINGS
//  This is the file you change first. After a change: save, refresh
//  (Ctrl+R), test. If the page goes blank, press F12 and read the
//  Console: it's almost always a missing comma, quote or bracket.
// =====================================================================

// Your app: its name, the line under the name, and its main colour.
// (Also change --brand at the top of css/style.css to the same colour.)
export const APP = {
  name: "Harbour Café Helper",
  tagline: "Opening hours, the menu and what's dairy-free.",
  colour: "#ff5a5f",
};

// Your bot: its job, its rules and a few examples of how it talks.
export const BOT = {
  name: "Harbour Café",

  // The first message people see in the chat.
  greeting: "Hi! I'm the Harbour Café helper. Ask me about our hours, the menu or what's dairy-free. ☕",

  // The bot's job: WHO it is, WHAT it does, HOW it sounds, and its LIMITS.
  job: `You are the friendly helper on Harbour Café's website.
WHO you help: customers who want to visit or order.
WHAT you do: answer questions about the café, the menu and opening hours.
HOW you sound: warm and simple. 1 to 3 short sentences.
LIMITS: you don't know prices, specials or bookings unless you are told them; send people to the counter or phone (02) 5550 1234.`,

  // Rules the bot must follow. These are the café's: write your own!
  rules: [
    "Only talk about the café, food and drinks.",
    "Never make up prices, times or ingredients.",
    "If you are not sure, say so and suggest asking at the counter.",
  ],

  // 2 or 3 short examples. The AI copies their length and tone.
  examples: [
    { user: "Do you have Wi-Fi?", bot: "We do! Ask at the counter for today's password. 📶" },
    { user: "Can I bring my dog?", bot: "Dogs are welcome at our outside tables. We'll even bring a water bowl! 🐶" },
  ],

  // What the FAQ bot says when the answer isn't in data/faq.json.
  unknownReply: "Sorry, I don't know that one. Please ask at the counter or call (02) 5550 1234.",
};

// Turn tabs on (true) or off (false).
export const FEATURES = {
  chat: true,
  faq: true,       // week 3: answers only from data/faq.json
  finder: true,    // week 4: picks items from data/products.json
  summarise: true,
};

// Checks in code (js/safety.js). These run before the AI sees anything,
// so they work every time, even when someone tries to trick the bot.
export const SAFETY = {
  maxLength: 500,  // longest message allowed, in characters
  blockedWords: ["password", "credit card"],
  blockedReply: "Sorry, I can't help with that. Ask me about the café instead!",
  tooLongReply: "That's a long message! Please keep it under 500 characters.",
};

// The AI itself. You don't need to change these yet.
export const AI = {
  creativity: 0.3,   // 0 = steady and repeatable, 1 = adventurous (more mistakes)
  maxReplyTokens: 200,
  historyTurns: 6,   // how many earlier messages the AI remembers
};
