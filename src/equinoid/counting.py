"""Conteo sin dependencias de visión: banda de tolerancia y cruce del segmento."""
from dataclasses import dataclass
from math import hypot, isfinite

@dataclass
class TrackState:
    point: tuple | None = None
    side: int = 0
    candidate: int = 0
    streak: int = 0
    last_seen: float = -1
    last_event: float = -1e9
    sequence: int = 0

class LineCounter:
    def __init__(self, p1, p2, *, deadband=0.012, stable_frames=2,
                 cooldown=0.7, max_gap=0.6, invert=False, initial_occupancy=None):
        self.a, self.b = tuple(p1), tuple(p2)
        self.v = (p2[0]-p1[0], p2[1]-p1[1])
        self.length = hypot(*self.v)
        if not self.length or not all(isfinite(x) and 0<=x<=1 for p in (p1,p2) for x in p):
            raise ValueError('La línea debe tener dos puntos distintos normalizados entre 0 y 1.')
        if stable_frames < 1 or deadband < 0 or cooldown < 0 or max_gap<=0:
            raise ValueError('Parámetros de conteo inválidos.')
        if initial_occupancy is not None and (not isinstance(initial_occupancy,int) or initial_occupancy<0):
            raise ValueError('El aforo inicial debe ser un entero no negativo o null.')
        self.deadband,self.stable_frames,self.cooldown,self.max_gap=deadband,stable_frames,cooldown,max_gap
        self.invert,self.initial=bool(invert),initial_occupancy
        self.tracks={}; self.entries=0; self.exits=0

    def distance(self,p):
        return (self.v[0]*(p[1]-self.a[1])-self.v[1]*(p[0]-self.a[0]))/self.length

    def intersects(self,p,q):
        d1,d2=self.distance(p),self.distance(q)
        if d1==d2: return False
        ratio=d1/(d1-d2)
        x=p[0]+ratio*(q[0]-p[0]); y=p[1]+ratio*(q[1]-p[1])
        projection=((x-self.a[0])*self.v[0]+(y-self.a[1])*self.v[1])/(self.length**2)
        return 0<=ratio<=1 and -1e-9<=projection<=1+1e-9

    def update(self,track_id,point,t):
        if not all(isfinite(x) for x in (*point,t)): raise ValueError('Coordenada o tiempo no finito.')
        s=self.tracks.setdefault(track_id,TrackState())
        if t<s.last_seen: raise ValueError('El tiempo debe ser creciente.')
        if s.last_seen>=0 and t-s.last_seen>self.max_gap:
            s.point=None; s.side=0; s.candidate=0; s.streak=0
        s.last_seen=t
        d=self.distance(point); side=1 if d>self.deadband else -1 if d < -self.deadband else 0
        if not side:
            s.candidate=0; s.streak=0
            return None
        s.streak=s.streak+1 if side==s.candidate else 1; s.candidate=side
        if s.streak<self.stable_frames: return None
        event=None
        if s.side and side!=s.side and s.point is not None and self.intersects(s.point,point) and t-s.last_event>=self.cooldown:
            entry=(s.side<side) != self.invert
            self.entries+=int(entry); self.exits+=int(not entry)
            s.last_event=t; s.sequence+=1
            event={'track_id':int(track_id),'sequence':s.sequence,'video_seconds':round(t,3),
                   'direction':'ENTRADA' if entry else 'SALIDA','occupancy':self.occupancy,
                   'warning':'AFORO_NEGATIVO_REVISAR' if self.occupancy is not None and self.occupancy<0 else ''}
        s.side=side; s.point=tuple(point)
        return event

    def prune(self,t):
        # No conserva estados perdidos durante toda una jornada de cámara.
        self.tracks={k:v for k,v in self.tracks.items() if t-v.last_seen<max(60,self.max_gap*2)}

    @property
    def occupancy(self):
        return None if self.initial is None else self.initial+self.entries-self.exits
