# Avro Academy course materials

Source files for the downloads attached to Avro Academy courses, so they can be rebuilt and re-uploaded if a server ever loses them.

| Course | Folder | Uploaded as |
| --- | --- | --- |
| JavaScript for Beginners | `javascript-for-beginners/` | `JavaScript-Course-Starter-Files.zip` (zip of `javascript-course/`) and `JavaScript-Cheat-Sheet.pdf` (printed from `cheat-sheet/javascript-cheat-sheet.html`) |

## Rebuilding the JavaScript downloads

```bash
cd javascript-for-beginners
zip -rqX JavaScript-Course-Starter-Files.zip javascript-course
# Cheat sheet: open cheat-sheet/javascript-cheat-sheet.html in Chrome → Print → Save as PDF (A4, background graphics on)
```
