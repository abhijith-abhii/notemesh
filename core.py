from pathlib import Path
from contextlib import contextmanager
from datetime import datetime,timezone
import sqlite3,os,re
class Conflict(Exception):pass
@contextmanager
def db():
 p=Path(os.environ.get('NOTES_DB',Path(__file__).parent/'var/notes.sqlite'));p.parent.mkdir(parents=True,exist_ok=True)
 c=sqlite3.connect(p,timeout=10);c.row_factory=sqlite3.Row
 c.executescript('CREATE TABLE IF NOT EXISTS notes(room TEXT PRIMARY KEY,body TEXT,revision INTEGER,author TEXT,updated TEXT); CREATE TABLE IF NOT EXISTS history(room TEXT,revision INTEGER,body TEXT,author TEXT,updated TEXT,PRIMARY KEY(room,revision));')
 try:
  with c:yield c
 finally:c.close()
def validate(room):
 if not re.fullmatch('[a-z0-9-]{1,40}',room):raise ValueError('Room requires 1–40 lowercase letters, numbers or hyphens')
def read(room):
 validate(room)
 with db() as c:
  row=c.execute('SELECT * FROM notes WHERE room=?',(room,)).fetchone()
 return dict(row) if row else dict(room=room,body='',revision=0,author='',updated='')
def save(room,body,revision,author):
 validate(room)
 if not isinstance(body,str) or len(body)>50000:raise ValueError('Note must contain at most 50,000 characters')
 if not isinstance(author,str) or not 1<=len(author.strip())<=40:raise ValueError('Choose a name of 1–40 characters')
 stamp=datetime.now(timezone.utc).isoformat()
 with db() as c:
  c.execute('BEGIN IMMEDIATE')
  row=c.execute('SELECT revision FROM notes WHERE room=?',(room,)).fetchone();actual=row[0] if row else 0
  if revision!=actual:raise Conflict('A newer revision exists. Copy your draft before loading the latest note.')
  c.execute('INSERT INTO notes VALUES(?,?,?,?,?) ON CONFLICT(room) DO UPDATE SET body=excluded.body,revision=excluded.revision,author=excluded.author,updated=excluded.updated',(room,body,actual+1,author,stamp))
  c.execute('INSERT INTO history VALUES(?,?,?,?,?)',(room,actual+1,body,author,stamp))
 return read(room)
def history(room):
 validate(room)
 with db() as c:return [dict(x) for x in c.execute('SELECT revision,author,updated FROM history WHERE room=? ORDER BY revision DESC LIMIT 100',(room,))]
def analyze(params):return read(params.get('room','study-room'))
