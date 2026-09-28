import pytest
from core import read,save,history,Conflict
@pytest.fixture(autouse=True)
def isolated(tmp_path,monkeypatch):monkeypatch.setenv('NOTES_DB',str(tmp_path/'notes.db'))
def test_revision_history():
 assert read('demo')['revision']==0
 save('demo','First',0,'Ada');save('demo','Second',1,'Lin')
 assert read('demo')['body']=='Second'
 assert [x['revision'] for x in history('demo')]==[2,1]
def test_stale_write_preserves_winner():
 save('demo','winner',0,'Ada')
 with pytest.raises(Conflict):save('demo','loser',0,'Lin')
 assert read('demo')['body']=='winner'
def test_room_isolation():
 save('one','secret',0,'A');assert read('two')['body']==''
@pytest.mark.parametrize('room',['../secret','A B','', 'x'*41])
def test_bad_room(room):
 with pytest.raises(ValueError):read(room)
def test_event_stream():
 from app import app
 c=app.test_client();r=c.get('/api/notes/demo/events',buffered=False)
 assert b'"revision": 0' in next(r.response);r.close()
def test_api_conflict():
 from app import app
 c=app.test_client();h={'X-Portfolio-Request':'1'}
 assert c.put('/api/notes/demo',json={'body':'a','revision':0,'author':'A'},headers=h).status_code==200
 assert c.put('/api/notes/demo',json={'body':'b','revision':0,'author':'B'},headers=h).status_code==409
