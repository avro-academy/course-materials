How the course data was made (for course authors).
  gen_days.py     -> daily_sales.csv      (python gen_days.py '{}' path.csv)
  gen_members.py  -> loyalty_members.csv
  gen_reviews.py  -> reviews.csv
  mdays.py / mmembers.py / mreviews.py print each lesson's numbers next to the lesson's own, to check the data.
All three are seeded, so they make the same files every time.
