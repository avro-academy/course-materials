CORNER CAFÉ: starter files
Avro Academy · Next.js Foundations: Build a Café Website (Next.js 16)

Each folder is a complete, working app at the end of one module:

  step-1-start          Module 1  A plain page and layout
  step-2-components     Module 2  Menu data, MenuCard, props, lists
  step-3-routing        Module 3  Menu, About and item pages, header, not-found
  step-4-styling        Module 4  Tailwind, images, the Nunito font, a CSS Module
  step-5-server-client  Module 5  Menu filter, active links, "Open now",
                                  today's special, error page
  step-6-forms          Module 6  Book a table (Server Action) and /api/menu
  step-7-final          Modules 7-8  Metadata, sitemap, robots, icon and
                                  share image, environment variables

RUN ONE
  You need Node.js 20.9 or newer (nodejs.org, LTS version).
  cd step-7-final
  npm install        (once per folder; takes a minute)
  npm run dev        then open http://localhost:3000   (Ctrl + C stops it)

  npm run build      the production version (Module 8)
  npm start

ENVIRONMENT VARIABLES (step 7)
  Copy .env.example to .env.local and change the values.

The menu pictures in public/menu are illustrations, free to use in your
own practice projects.
