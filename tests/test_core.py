import unittest,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from equinoid.counting import LineCounter
from equinoid.storage import Store

class CountingTests(unittest.TestCase):
    def counter(self,**kw): return LineCounter((.1,.5),(.9,.5),stable_frames=2,**kw)
    def feed(self,c,points,track=1,start=0):
        return [e for i,p in enumerate(points) if (e:=c.update(track,p,start+i*.1))]
    def test_entry(self):
        c=self.counter();e=self.feed(c,[(.5,.4)]*3+[(.5,.6)]*3)
        self.assertEqual(len(e),1);self.assertEqual(c.entries,1)
    def test_exit(self):
        c=self.counter();self.feed(c,[(.5,.6)]*3+[(.5,.4)]*3);self.assertEqual(c.exits,1)
    def test_no_jitter(self):
        c=self.counter();self.feed(c,[(.5,.499),(.5,.501)]*15);self.assertEqual(c.entries+c.exits,0)
    def test_no_birth_count(self):
        c=self.counter();self.feed(c,[(.5,.8)]*8);self.assertEqual(c.entries,0)
    def test_outside_segment(self):
        c=self.counter();self.feed(c,[(.99,.4)]*3+[(.99,.6)]*3);self.assertEqual(c.entries,0)
    def test_occlusion_reset(self):
        c=self.counter(max_gap=.4);self.feed(c,[(.5,.4)]*3);self.feed(c,[(.5,.6)]*3,start=2);self.assertEqual(c.entries,0)
    def test_recross(self):
        c=self.counter(cooldown=.1);self.feed(c,[(.5,.4)]*3+[(.5,.6)]*3+[(.5,.4)]*3)
        self.assertEqual((c.entries,c.exits),(1,1))
    def test_invert(self):
        c=self.counter(invert=True);self.feed(c,[(.5,.4)]*3+[(.5,.6)]*3);self.assertEqual(c.exits,1)
    def test_unknown_occupancy(self):
        c=self.counter();self.feed(c,[(.5,.4)]*3+[(.5,.6)]*3);self.assertIsNone(c.occupancy)
    def test_negative_flag(self):
        c=self.counter(initial_occupancy=0);events=self.feed(c,[(.5,.6)]*3+[(.5,.4)]*3)
        self.assertEqual(c.occupancy,-1);self.assertEqual(events[0]['warning'],'AFORO_NEGATIVO_REVISAR')
    def test_independent_tracks(self):
        c=self.counter()
        for tid in (1,2): self.feed(c,[(.5,.4)]*3+[(.5,.6)]*3,track=tid)
        self.assertEqual(c.entries,2)
    def test_invalid_line(self):
        with self.assertRaises(ValueError): LineCounter((0,0),(0,0))
    def test_invalid_initial(self):
        with self.assertRaises(ValueError): self.counter(initial_occupancy=-1)
    def test_time_reversal(self):
        c=self.counter();c.update(1,(.5,.4),3)
        with self.assertRaises(ValueError): c.update(1,(.5,.4),2)
    def test_single_frame_spike(self):
        c=self.counter();self.feed(c,[(.5,.4)]*3+[(.5,.7)]+[(.5,.4)]*3);self.assertEqual(c.entries,0)

class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.s=Store(Path(self.tmp.name)/'e.sqlite',[{'horse_id':'EQ-001','name':'Saturno'}])
        self.s.record(dict(track_id=1,sequence=1,video_seconds=.5,direction='ENTRADA',occupancy=None,warning='',confidence=.9,snapshot='a.jpg'))
    def tearDown(self): self.s.close();self.tmp.cleanup()
    def test_unassigned_by_default(self): self.assertIsNone(self.s.events()[0]['horse_id'])
    def test_audited_confirmation(self):
        self.s.identify(1,'EQ-001','Operador','Marca visual confirmada manualmente')
        self.assertEqual(self.s.events()[0]['name'],'Saturno');self.assertEqual(self.s.db.execute('SELECT count(*) FROM audit').fetchone()[0],1)
    def test_unknown_horse_rejected(self):
        with self.assertRaises(ValueError): self.s.identify(1,'X','Op','evidencia')
    def test_evidence_required(self):
        with self.assertRaises(ValueError): self.s.identify(1,'EQ-001','Op','')
    def test_event_required(self):
        with self.assertRaises(ValueError): self.s.identify(12,'EQ-001','Op','Test')
    def test_duplicate_event_rejected(self):
        import sqlite3
        with self.assertRaises(sqlite3.IntegrityError): self.s.record(dict(track_id=1,sequence=1,video_seconds=.6,direction='ENTRADA',occupancy=None,warning='',confidence=.8,snapshot='b.jpg'))

if __name__=='__main__': unittest.main()
