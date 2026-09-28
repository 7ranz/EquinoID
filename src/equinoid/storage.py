"""Registro SQLite por ejecución. Las identidades requieren evidencia del operador."""
import csv,json,sqlite3
from datetime import datetime,timezone
from pathlib import Path

def utcnow(): return datetime.now(timezone.utc).isoformat()

class Store:
    def __init__(self,path,registry=None):
        self.db=sqlite3.connect(path)
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS horses(horse_id TEXT PRIMARY KEY,name TEXT NOT NULL,tag TEXT,fictional INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS events(event_id INTEGER PRIMARY KEY,track_id INTEGER,sequence INTEGER,video_seconds REAL,direction TEXT,
        occupancy INTEGER,warning TEXT,confidence REAL,snapshot TEXT,horse_id TEXT REFERENCES horses(horse_id),UNIQUE(track_id,sequence));
        CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,event_id INTEGER REFERENCES events(event_id),old_horse_id TEXT,new_horse_id TEXT,operator TEXT,evidence TEXT,created_utc TEXT);
        ''')
        if registry:
            for h in registry:
                self.db.execute('INSERT OR IGNORE INTO horses VALUES (?,?,?,?)',(h['horse_id'],h['name'],h.get('tag',''),int(h.get('fictional',True))))
            self.db.commit()

    def record(self,e):
        with self.db:
            cur=self.db.execute('''INSERT INTO events(track_id,sequence,video_seconds,direction,occupancy,warning,confidence,snapshot)
             VALUES (?,?,?,?,?,?,?,?)''',tuple(e[k] for k in ['track_id','sequence','video_seconds','direction','occupancy','warning','confidence','snapshot']))
        return cur.lastrowid

    def identify(self,event_id,horse_id,operator,evidence):
        if not operator.strip() or not evidence.strip(): raise ValueError('Operador y evidencia son obligatorios.')
        old=self.db.execute('SELECT horse_id FROM events WHERE event_id=?',(event_id,)).fetchone()
        if old is None: raise ValueError('Evento inexistente.')
        if not self.db.execute('SELECT 1 FROM horses WHERE horse_id=?',(horse_id,)).fetchone(): raise ValueError('Caballo no incluido en el catálogo.')
        with self.db:
            self.db.execute('UPDATE events SET horse_id=? WHERE event_id=?',(horse_id,event_id))
            self.db.execute('INSERT INTO audit(event_id,old_horse_id,new_horse_id,operator,evidence,created_utc) VALUES (?,?,?,?,?,?)',
                            (event_id,old[0],horse_id,operator.strip(),evidence.strip(),utcnow()))

    def events(self):
        self.db.row_factory=sqlite3.Row
        return [dict(r) for r in self.db.execute('''SELECT e.*,h.name,h.fictional FROM events e LEFT JOIN horses h USING(horse_id) ORDER BY video_seconds,event_id''')]

    def export(self,path):
        rows=self.events()
        headers=['event_id','track_id','sequence','video_seconds','direction','occupancy','warning','confidence','snapshot','horse_id','name','fictional']
        with Path(path).open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=headers); w.writeheader();w.writerows(rows)

    def close(self): self.db.close()
