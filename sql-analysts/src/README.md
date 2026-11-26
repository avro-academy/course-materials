`harbour_home.sql` was recovered from the SQL playground page on avro.academy, which embeds the course database (gzipped, base64) in `window.AVRO_SQL_DATA`. `playground-exercises.json` is the page's `window.AVRO_SQL_EXERCISES` (26 exercises with answers). All answers run against the database, and the lesson figures match exactly.

Rebuild: `sqlite3 harbour_home.sqlite < harbour_home.sql`, then `sqlite3 -header -csv harbour_home.sqlite "select * from <table>" > csv/<table>.csv`.
