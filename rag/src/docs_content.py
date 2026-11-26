"""The words of the seven made-up Corner Café documents. make_docs.py turns them into PDF, Word and Markdown.

In the page lists, each page is a list of blocks: ("h1"|"h2"|"p"|"li", text), ("table", [rows]) or ("cover", lines).
"""

HANDBOOK_2026 = [
    [("cover", ["Corner Café", "Staff Handbook", "Version 4 · July 2026",
                "This handbook replaces Version 3 (July 2024).",
                "12 Example Street, Sydney NSW 2000 · (02) 5550 0000",
                "Approved by Tom Nguyen, Café Manager"])],
    [("h1", "Welcome to Corner Café"),
     ("p", "Thanks for joining the team. Corner Café has served coffee and food on the corner of Example Street and Example "
           "Lane since 2015."),
     ("p", "This handbook explains how we work: your pay, rosters and breaks, what to wear, how to stay safe, and what to do when "
           "something goes wrong. Our other documents (the Food Safety Program, "
           "the Espresso Machine Guide, our policies and the Staff FAQ) are in the staff folder and in Deputy."),
     ("p", "This is Version 4, from July 2026. If anything here doesn't match what you've been told, this handbook is right. "
           "Your first shifts are with a buddy, an experienced team member."),
     ("h2", "Contents"),
     ("toc", ["1. Your employment", "2. Rosters and shifts", "3. Leave and time off", "4. Uniform and presentation",
              "5. Health and safety", "6. Food safety", "7. Customers", "8. Cash handling", "9. Leaving Corner Café",
              "10. Who to ask"])],
    [("h1", "1. Your employment"),
     ("h2", "1.1 Types of employment"),
     ("p", "Most of our team are casual employees. Casual staff are paid a casual loading of 25% on top of the base rate instead "
           "of paid leave. A few senior staff are part-time, with set hours and paid leave. Your contract says which you are. "
           "Everyone starts with 3 months of probation."),
     ("h2", "1.2 Pay rates"),
     ("p", "Corner Café pays above the minimum rates in the Restaurant Industry Award. Our base hourly rates from 1 July 2026 are "
           "below. Casual rates already include the 25% casual loading."),
     ("table", [["Level", "Role", "Part-time (per hour)", "Casual (per hour)"],
                ["Level 1", "New starter, front of house", "$25.40", "$31.75"],
                ["Level 2", "Barista", "$26.60", "$33.25"],
                ["Level 3", "Senior barista", "$28.20", "$35.25"],
                ["Level 4", "Shift supervisor", "$29.80", "$37.25"]]),
     ("p", "Saturday work is paid at 125% of your rate, Sunday work at 150% and public holidays at 225%. Work before 7am or after 7pm "
           "is paid an extra $2.70 an hour."),
     ("h2", "1.3 Pay day and payslips"),
     ("p", "We pay every week, on Wednesday, directly into your bank account. Each pay covers Monday to Sunday of the week "
           "before. Your payslip is emailed to you on pay day through our payroll app, KeyPay. If you think your pay is wrong, "
           "tell the café manager within 14 days and we will fix it in the next pay."),
     ("h2", "1.4 Superannuation"),
     ("p", "We pay superannuation into your chosen super fund every month, at the rate the law requires (12% from 1 July 2025). You can choose your own fund when you start; if you "
           "don't, we pay into our default fund.")],
    [("h1", "2. Rosters and shifts"),
     ("h2", "2.1 Rosters"),
     ("p", "The roster is published in the Deputy app every Thursday by 5pm, for the week starting the following Monday. Check "
           "it every week. Tell your manager in Deputy at least 2 weeks ahead if you can't work certain days. We do our best to "
           "work around study and other commitments. Shifts are usually between 4 and 8 hours. The roster shows your start and "
           "finish times and your role for each shift."),
     ("h2", "2.2 Swapping shifts"),
     ("p", "You can swap a shift with a trained team member. Post the swap request in Deputy at least 24 hours before the shift. "
           "The swap only counts once a manager approves it in Deputy. If nobody else can take your shift, you are still "
           "rostered on and you must work it."),
     ("h2", "2.3 Breaks"),
     ("p", "If you work more than 5 hours, you get a 30-minute unpaid meal break, which must start before the end of your 5th "
           "hour. If you work 4 hours or more, you also get a paid 10-minute rest break. Your manager will tell you when to take "
           "them. On shifts of 6 hours or more you get a free staff meal from the menu and a non-alcoholic drink. On shorter "
           "shifts you get 50% off food and one free coffee."),
     ("h2", "2.4 Being late or sick"),
     ("p", "If you're going to be late, call (don't text) the shift supervisor on the café phone, (02) 5550 0000, as soon "
           "as you know. If you're sick and can't work, call the café manager at least 2 hours before your shift starts. "
           "Don't just message the group chat. For an absence of 2 or more days in a row, part-time staff need a medical "
           "certificate or statutory declaration. Casual staff don't need one, but must still call. If you have vomiting or "
           "diarrhoea, you must not work with food until you have had no symptoms for 48 hours (see Food safety).")],
    [("h1", "3. Leave and time off"),
     ("h2", "3.1 Annual leave"),
     ("p", "Part-time staff get 4 weeks of paid annual leave a year. Apply in Deputy at least 4 weeks ahead. December and January "
           "are our busiest months, so leave then is hard to approve."),
     ("h2", "3.2 Time off for casual staff"),
     ("p", "Casual staff don't get paid leave. Mark the days you can't work as unavailable in Deputy, at least 2 weeks ahead, "
           "and we won't roster you on."),
     ("h1", "4. Uniform and presentation"),
     ("p", "Wear the Corner Café black apron (we give you two), a plain black or white T-shirt or shirt, long black pants or "
           "jeans, and closed, non-slip black shoes. No open shoes, ever. Long hair must be tied back. Keep jewellery to a "
           "plain band ring and small stud earrings when working with food. Your name badge must be worn on every shift. "
           "A replacement badge costs nothing — ask the manager.")],
    [("h1", "5. Health and safety"),
     ("h2", "5.1 Lifting and hot equipment"),
     ("p", "Lift with your legs, not your back, and ask for help with anything over 15 kg, like milk crates. Never carry hot "
           "drinks above a customer's head. The steam wands and the oven get very hot: always use a cloth."),
     ("h2", "5.2 Burns, cuts and first aid"),
     ("p", "The first aid kit is on the wall next to the back door, and the burns kit is under the coffee machine. Shift "
           "supervisors hold current first aid certificates. For a burn: cool it under cool running water for 20 minutes. "
           "Don't use ice or butter. For a cut: wash it, cover it with a blue detectable band-aid and wear a glove when "
           "handling food."),
     ("h2", "5.3 Reporting incidents"),
     ("p", "Report every injury, near miss or customer incident to the shift supervisor straight away, even if it seems minor. "
           "Then fill in an incident report (form 7B, in the red folder behind the counter) before you leave. The café manager "
           "reviews every report within 2 days."),
     ("h2", "5.4 Emergencies"),
     ("p", "If the fire alarm sounds, stop the espresso machine, turn off the gas and help customers out through the front door. "
           "Meet at the bus stop across the road. The shift supervisor checks that everyone is out. Learn the way out in your first "
           "week, and where the fire extinguishers and the fire blanket are.")],
    [("h1", "6. Food safety"),
     ("p", "Every food handler must complete the free online food safety course (DoFoodSafely) in their first week and give the "
           "café manager the certificate. Our Food Safety Supervisor is Priya Sharma. Read the Food Safety Program before your "
           "first kitchen shift. The main rules:"),
     ("li", "Wash your hands before handling food, and after touching your face, phone, money or rubbish."),
     ("li", "Keep cold food at 5°C or colder and hot food at 60°C or hotter."),
     ("li", "Never work with food when you're unwell (see 2.4)."),
     ("li", "Label everything you put in the cool room with what it is and the date."),
     ("h2", "6.1 Allergies"),
     ("p", "Take every allergy seriously. Never guess what's in a dish: check the Allergen Matrix, and follow the allergen steps "
           "in the Food Safety Program. If you're not sure, say so and ask the kitchen."),
     ("h2", "6.2 Cleaning"),
     ("p", "Clean as you go. The cleaning schedule is on the kitchen wall: tick each job when it's done and sign at the end of "
           "your shift. At closing time, the shift supervisor checks the cleaning schedule and the cool room temperatures before "
           "locking up for the night.")],
    [("h1", "7. Customers"),
     ("h2", "7.1 Complaints"),
     ("p", "Listen, say sorry and fix it if you can: remake a drink or meal for free. Tell the shift supervisor about every "
           "complaint, and follow the Refunds and Complaints Policy."),
     ("h2", "7.2 Refunds"),
     ("p", "You can give a refund of up to $50 yourself, to the card or cash the customer paid with. A refund over $50 must be "
           "approved by the shift supervisor or the café manager. Write every refund in the refunds book."),
     ("h1", "8. Cash handling"),
     ("p", "Each till starts the day with a $200 float. At closing, count the till with the shift supervisor, fill in the "
           "cash-up sheet and put the takings in the safe. Never leave a till open or unattended, and never take money from "
           "the till for change or purchases. If the till is more than $5 over or under, tell the café manager.")],
    [("h1", "9. Leaving Corner Café"),
     ("p", "Casual staff should give at least 1 week's notice, and part-time staff 2 weeks, in writing to the café manager. "
           "Your final pay, including any unused annual leave, is paid on the next pay day. Please return your aprons and your name "
           "badge on your last day."),
     ("p", "Before your last shift, the café manager will ask you for feedback about working here. It's optional and "
           "confidential. We're happy to give a reference to staff who leave on good terms."),
     ("h1", "10. Who to ask"),
     ("li", "Café manager: Tom Nguyen, 0400 555 012 (pay, rosters, leave, anything else)."),
     ("li", "Food Safety Supervisor: Priya Sharma (food safety and allergies)."),
     ("li", "Shift supervisors: shown on the roster for each shift."),
     ("li", "Employee Assistance Program: free, private counselling for you and your family, on 1800 555 333.")],
]

HANDBOOK_2024 = [
    [("cover", ["Corner Café", "Staff Handbook", "Version 3 · July 2024",
                "12 Example Street, Sydney NSW 2000"])],
    [("h1", "1. Pay day and payslips"),
     ("p", "We pay every fortnight, on Thursday, directly into your bank account. Your payslip is emailed to you on pay day. "
           "Casual staff are paid a casual loading of 25%. The base rate for a barista is $25.10 an hour."),
     ("h1", "2. Rosters"),
     ("p", "The roster is put up on the staff noticeboard every Friday, for the following week. Tell your manager two weeks "
           "ahead if you can't work certain days. Shifts are 4 to 8 hours. To swap a shift, ask your manager in person. Check the noticeboard before you leave each shift."),
     ("h1", "3. Breaks"),
     ("p", "If you work more than 5 hours, you get a 30-minute unpaid meal break. Staff get one free coffee per shift."),
     ("h1", "4. Uniform"),
     ("p", "Wear a black top, black pants and closed shoes. Aprons are provided free. Wash your hands often, and tell your "
           "manager if you're sick.")],
]

FOOD_SAFETY = [
    [("cover", ["Corner Café", "Food Safety Program", "Updated March 2026",
                "Keep a copy in the kitchen. Every food handler must read it."])],
    [("lead", "About this program"),
     ("p", "This program explains how Corner Café keeps food safe, as required by the NSW Food Authority. It covers hygiene, "
           "temperatures, deliveries, allergens and cleaning. Our Food Safety Supervisor is Priya Sharma (certificate "
           "FSS-208841). Ask her if you're unsure about anything in it."),
     ("h1", "1. Personal hygiene"),
     ("p", "Wash and dry your hands at the hand basin (not the sink) before you start, after a break, and after touching raw "
           "food, your face, your phone, money or rubbish. Wear a clean apron, tie back long hair and cover cuts with a blue "
           "band-aid and a glove. Don't handle food if you're unwell: tell the café manager."),
     ("h1", "2. Temperature control"),
     ("p", "Check and write down the cool room, fridge and display temperatures at opening and at 2pm, on the temperature log. Use the probe thermometer; clean it between foods."),
     ("table", [["Food", "Keep it at", "If it isn't"],
                ["Cold food (fridge, cool room, display)", "5°C or colder", "Tell the supervisor; throw out food above 5°C for more than 4 hours"],
                ["Frozen food", "-15°C or colder", "Use within 24 hours if it has thawed; never refreeze"],
                ["Hot food (soups, pies)", "60°C or hotter", "Reheat to 75°C once, or throw it out"],
                ["Cooked food you are cooling", "Below 21°C within 2 hours, below 5°C within 6 hours", "Throw it out"]]),
     ("h1", "3. Deliveries and storage"),
     ("p", "Check every delivery: cold food must arrive at 5°C or colder, packaging must be undamaged and dates must be in date. "
           "Refuse anything that isn't, and write it on the delivery sheet. Store raw meat on the bottom shelf, below ready-to-eat "
           "food. Dry goods go in sealed containers on shelves in the store room, at least 15 cm off the floor. "
           "Label and date everything, and use the oldest stock first.")],
    [("h1", "4. Allergens"),
     ("p", "Food allergies can kill. The Allergen Matrix on the kitchen wall lists which menu items contain each of the common "
           "allergens: peanuts, tree nuts, milk, egg, gluten, soy, sesame, fish, shellfish and lupin. When a customer tells you "
           "about an allergy:"),
     ("li", "Check the Allergen Matrix to confirm which menu items contain it. Never guess."),
     ("li", "Tell the kitchen, and write 'ALLERGY' and the allergen on the docket."),
     ("li", "The kitchen cleans the bench, uses clean utensils and a fresh chopping board, and makes the dish separately."),
     ("li", "The person who made it delivers it to the customer, and confirms the allergy."),
     ("p", "If we can't be sure a dish is safe, tell the customer honestly. Never promise a dish is completely free of an "
           "allergen."),
     ("h1", "5. Cleaning and pest control"),
     ("p", "Follow the cleaning schedule on the kitchen wall and sign it. Sanitise benches and chopping boards after every use. "
           "Empty the bins twice a day, and wash the bin area at closing. "
           "Pest Pros check the café every month; their next visit is on the schedule. If you see signs of pests, tell the café "
           "manager straight away, and call Pest Pros on (02) 5550 0199 if the manager isn't there."),
     ("h1", "6. Records"),
     ("p", "Keep the temperature log, delivery sheets and cleaning schedule for 12 months. Priya Sharma, our Food Safety "
           "Supervisor, checks them every week. An inspector from the council can ask to see them at any time.")],
]

ESPRESSO = [
    [("cover", ["Corner Café", "Espresso Machine Guide", "(2026)"]),
     ("h1", "1. Our machine"),
     ("p", "We use a three-group La Spaziale machine and two grinders: the left grinder is our house blend, the right one is "
           "decaf. Only trained baristas may ever adjust the grinders."),
     ("h1", "2. The recipe"),
     ("table", [["", "House blend", "Decaf"],
                ["Dose (ground coffee)", "20 g", "19 g"],
                ["Yield (in the cup)", "40 g", "38 g"],
                ["Time", "25 to 30 seconds", "25 to 30 seconds"]]),
     ("p", "If shots run faster than 25 seconds, make the grind finer; slower than 30 seconds, make it coarser. Taste a shot yourself at "
           "the start of every shift. Weigh every shot: put the cup on the scale under the group, start the shot and stop it when "
           "the scale reads the yield.")],
    [("h1", "3. Milk"),
     ("p", "Purge the steam wand before and after every jug. Stretch the milk until the jug feels warm, then texture it to "
           "about 60°C: too hot to hold for more than a second. Never reheat milk. Wipe the wand with its own damp cloth after "
           "every jug. Use full cream milk unless the customer asks for something else. We also have skim, lactose-free, soy, "
           "oat and almond milk; oat and almond are 70c extra. Plant milks stretch differently: stretch them less and pour them a "
           "little cooler."),
     ("h1", "4. Daily cleaning"),
     ("p", "At closing, backflush each group head: put the blind basket in, add one Cafetto tablet, and run the group for 10 "
           "seconds on, 10 seconds off, five times. Rinse with five more runs without the tablet. Soak the baskets and handles "
           "in Cafetto solution overnight. Scrub the group seals with the brush and empty the drip trays.")],
    [("h1", "5. Troubleshooting"),
     ("table", [["Problem", "Likely cause", "What to do"],
                ["Shots run too fast or too slow", "Grind is off", "Adjust the grind and taste again"],
                ["Water leaking around the group head", "Worn group seal", "Tell the supervisor; use another group"],
                ["No steam from the wand", "Blocked tip", "Soak the tip in hot water and clear the holes with a pin"],
                ["Sour or weak taste", "Shot ran too fast", "Make the grind finer"],
                ["Machine won't heat", "Power or water off", "Check the switch and the water tap under the counter"]]),
     ("p", "For anything else, or if the machine leaks under the counter, turn it off and call Café Tech Services on "
           "1300 555 870. Don't open the machine yourself.")],
]

REFUNDS = [
    ("title", "Refunds and Complaints Policy"),
    ("p", "Corner Café · Updated November 2025"),
    ("h", "Our promise"),
    ("p", "If something isn't right, we always fix it. Every customer who complains should leave happier than they arrived."),
    ("h", "Handling a complaint"),
    ("p", "Listen without interrupting, say sorry and thank the customer for telling you. Offer to remake the drink or meal "
          "straight away, at no charge. Tell the shift supervisor about every complaint, even if you fixed it."),
    ("h", "Refunds"),
    ("p", "Any staff member can give a refund of up to $50, to the card or cash the customer paid with. Refunds over $50 need "
          "the shift supervisor or the café manager to approve them. Write every refund in the refunds book: the date, the "
          "amount, the reason and your name. We don't give refunds as gift cards unless the customer asks."),
    ("h", "Serious complaints"),
    ("p", "If a customer says they became ill after eating with us, or had an allergic reaction, get the shift supervisor "
          "straight away. Write down what they ate, when, and their phone number. The café manager will call them back within "
          "one day."),
    ("h", "Online reviews"),
    ("p", "Don't reply to online reviews yourself. The café manager replies to every review, usually within two days."),
]

PRIVACY = [
    ("title", "Privacy and CCTV Policy"),
    ("p", "Corner Café · Updated November 2025"),
    ("h", "CCTV"),
    ("p", "Cameras record the counter, the till and the front door, for safety and security. There are no cameras in the "
          "toilets or the staff room. Recordings are kept for 30 days and only the café manager can view them."),
    ("h", "Customer information"),
    ("p", "We only keep customers' details when they book a table or order catering. Never share a customer's name, phone "
          "number or booking with anyone else."),
    ("h", "Staff information"),
    ("p", "Your personal details are kept in our payroll and rostering apps, and only the café manager can see them. Tell the café manager "
          "straight away if your details change. We never sell or share information for marketing."),
    ("p", "If you have a question about privacy, or think someone's information has been misused, talk to the café manager "
          "straight away."),
]

FAQ = """# Staff FAQ

Quick answers to the questions new staff ask most. For more detail, see the Staff Handbook.

## Where do I find my roster?
In the Deputy app. It's published every Thursday by 5pm, for the week starting the following Monday.

## Who do I talk to about a pay problem?
Tom Nguyen, the café manager, within 14 days of pay day. Check your payslip first.

## Can I have a coffee on my shift?
Yes: one free coffee every shift. On shifts of 6 hours or more you also get a free staff meal.

## I've lost my apron or name badge. What do I do?
Tell the café manager. Your first replacement is free, and it's ready within days.

## How do I get trained on the espresso machine?
Ask the café manager to roster you on with a senior barista, and read the Espresso Machine Guide.

## How do I get a discount when I'm not working?
Show your name badge at the till when you pay. You get 25% off food and drinks for yourself.

"""
