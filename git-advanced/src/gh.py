import hashlib
def obj(kind, body):
    if isinstance(body, str): body = body.encode()
    return hashlib.sha1(b'%s %d\0' % (kind.encode(), len(body)) + body).hexdigest()
def blob(s): return obj('blob', s)
def tree(files):  # files: name -> content
    body = b''
    for name in sorted(files):
        body += b'100644 ' + name.encode() + b'\0' + bytes.fromhex(blob(files[name]))
    return obj('tree', body)
AUTH = 'Sam Lee <12345678+sam-lee@users.noreply.github.com>'
def ts(day):  # February day at 10:00 +1100
    return 1770937200 + (day - 13) * 86400
def commit(files, parent, day, msg):
    t = tree(files)
    s = f'tree {t}\n' + (f'parent {parent}\n' if parent else '') + f'author {AUTH} {ts(day)} +1100\ncommitter {AUTH} {ts(day)} +1100\n\n{msg}\n'
    return obj('commit', s)
