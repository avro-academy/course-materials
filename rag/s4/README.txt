Step 4: better search, measured (Module 4)

  pip install rank-bm25
  python index.py                                   (if you haven't in this folder)
  python search.py "FSS-208841"                     hybrid search, the default
  python search.py "KeyPay" --method keyword        or --method vector
  python eval_search.py                             score all three methods on questions.csv
