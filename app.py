from pathlib import Path
import os
from flask import Flask, jsonify, request, render_template
from core import analyze
BASE=Path(__file__).resolve().parent
app=Flask(__name__)
app.config.update(MAX_CONTENT_LENGTH=1048576)
@app.before_request
def guard():
    if request.method not in ('GET','HEAD','OPTIONS'):
        if request.headers.get('X-Portfolio-Request')!='1': return jsonify(error='Missing same-origin request header'),403
        if request.headers.get('Origin') and request.headers['Origin'] != request.host_url.rstrip('/'): return jsonify(error='Cross-origin request rejected'),403
@app.after_request
def headers(response):
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'"
    response.headers['Cache-Control']='no-store'
    return response
@app.get('/')
def home(): return render_template('index.html')
@app.get('/health')
def health(): return jsonify(status='ok')
@app.post('/api/run')
def run():
    try:
        payload=request.get_json()
        if not isinstance(payload,dict): raise ValueError('Expected a JSON object')
        return jsonify(analyze(payload))
    except (ValueError,KeyError,TypeError,OverflowError,FileNotFoundError) as exc: return jsonify(error=str(exc)),400

from core import read,save,history,Conflict
import json,time
from flask import Response
@app.get('/api/notes/<room>')
def get_note(room):
 try:return jsonify(read(room))
 except ValueError as e:return jsonify(error=str(e)),400
@app.put('/api/notes/<room>')
def put_note(room):
 try:
  p=request.get_json();return jsonify(save(room,p['body'],p['revision'],p['author']))
 except Conflict as e:return jsonify(error=str(e),current=read(room)),409
 except (ValueError,TypeError,KeyError) as e:return jsonify(error=str(e)),400
@app.get('/api/notes/<room>/history')
def get_history(room):
 try:return jsonify(history(room))
 except ValueError as e:return jsonify(error=str(e)),400
@app.get('/api/notes/<room>/events')
def events(room):
 try:read(room)
 except ValueError as e:return jsonify(error=str(e)),400
 def stream():
  last=-1
  for _ in range(60):
   item=read(room)
   if item['revision']!=last:
    last=item['revision'];yield 'data: '+json.dumps(item)+'\n\n'
   else:yield ': heartbeat\n\n'
   time.sleep(.5)
 return Response(stream(),mimetype='text/event-stream',headers={'X-Accel-Buffering':'no'})
if __name__=='__main__':app.run(host='127.0.0.1',port=int(os.environ.get('PORT','8080')),threaded=True)
