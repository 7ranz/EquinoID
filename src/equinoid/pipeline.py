"""YOLO + ByteTrack. Archivos por ejecución, métricas y evidencia auditable."""
import hashlib,json,time,platform,sys
from datetime import datetime,timezone
from pathlib import Path
from .counting import LineCounter
from .storage import Store
from .reporting import make_report

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def load_config(file):
    cfg=json.loads(Path(file).read_text(encoding='utf-8-sig'))
    if not 0<cfg['confidence']<=1: raise ValueError('confidence debe estar entre 0 y 1.')
    if not isinstance(cfg['image_size'],int) or cfg['image_size']<128: raise ValueError('image_size inválido.')
    if cfg.get('anchor') not in ('bottom_center','center'): raise ValueError('anchor inválido.')
    counter=LineCounter(*cfg['line'],**{k:cfg[k] for k in ['deadband','stable_frames','cooldown','max_gap','invert','initial_occupancy']})
    return cfg,counter

def analyze(source,config,output,*,show=False,max_seconds=None,replay=None):
    import cv2,numpy as np
    cfg,counter=load_config(config)
    folder=Path(output)
    if folder.exists(): raise ValueError('El directorio de salida ya existe. Elige uno nuevo para no sobrescribir evidencia.')
    registry=json.loads(Path(cfg['registry']).read_text(encoding='utf-8-sig'))
    local=Path(str(source)).is_file()
    if replay:
        metadata=Path(replay).parent/'summary.json'
        if not local or not metadata.is_file(): raise ValueError('Replay requiere video local y summary.json original.')
        original=json.loads(metadata.read_text(encoding='utf-8'))
        if original.get('source_sha256')!=digest(source): raise ValueError('Replay rechazado: la huella del video no coincide.')
    cap=cv2.VideoCapture(int(source) if str(source).isdigit() else str(source))
    if not cap.isOpened(): raise ValueError('No se pudo abrir el video o cámara.')
    fps=cap.get(cv2.CAP_PROP_FPS)
    if fps<=0 or not np.isfinite(fps): fps=30.0
    w,h=int(cap.get(3)),int(cap.get(4)); expected=int(cap.get(7)) if local else None
    if not w or not h: cap.release();raise ValueError('Dimensiones de video inválidas.')
    model=None
    if not replay:
        import torch,ultralytics
        torch.set_num_threads(cfg.get('threads',4))
        model=ultralytics.YOLO(cfg['model'])
        horse_ids=[k for k,v in model.names.items() if v=='horse']
        if len(horse_ids)!=1: cap.release();raise ValueError('El modelo debe incluir exactamente la clase horse.')
        versions={'python':sys.version.split()[0],'ultralytics':ultralytics.__version__,'torch':torch.__version__,'opencv':cv2.__version__,'numpy':np.__version__}
        detections=None
    else:
        detections={d['frame']:d for d in (json.loads(line) for line in Path(replay).read_text(encoding='utf-8').splitlines())}
        versions={'python':sys.version.split()[0],'opencv':cv2.__version__,'numpy':np.__version__,'mode':'replay_same_video_only'}
    folder.mkdir(parents=True);(folder/'evidence').mkdir()
    (folder/'config_used.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8')
    db=Store(folder/'events.sqlite',registry)
    writer=None;frames=0;detect_frames=0;ids=set();start=time.perf_counter();error=None;status='COMPLETO';clock=start
    trace=(folder/'tracks.jsonl').open('w',encoding='utf-8')
    summary={'farm':cfg['farm'],'camera':cfg['camera'],'source_name':Path(str(source)).name if local else 'camera_or_stream',
             'source_sha256':digest(source) if local else None,'created_utc':datetime.now(timezone.utc).isoformat(),'source_fps':fps,
             'width':w,'height':h,'expected_frames':expected,'versions':versions,'platform':platform.platform(),
             'model_sha256':digest(cfg['model']) if Path(cfg['model']).is_file() else None}
    try:
        if cfg.get('write_video',True):
            writer=cv2.VideoWriter(str(folder/'annotated.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
            if not writer.isOpened(): raise RuntimeError('No se pudo crear el video de salida.')
        while True:
            t=frames/fps if local else time.perf_counter()-clock
            if max_seconds is not None and t>=max_seconds: status='PARCIAL_LIMITE';break
            ok,frame=cap.read()
            if not ok:
                if (local and expected and frames<expected-1) or not local: status='INTERRUMPIDO_FUENTE'
                break
            frame_number=frames;frames+=1
            if replay:
                if frame_number not in detections: raise ValueError('La caché de detecciones no cubre este video completo.')
                obs=detections[frame_number]['observations']
            else:
                res=model.track(frame,persist=True,classes=horse_ids,conf=cfg['confidence'],imgsz=cfg['image_size'],
                                device=cfg['device'],tracker=cfg['tracker'],verbose=False)[0]
                obs=[]
                if res.boxes.id is not None:
                    for box,tid,score in zip(res.boxes.xyxy.cpu().tolist(),res.boxes.id.int().cpu().tolist(),res.boxes.conf.cpu().tolist()):
                        obs.append({'track_id':tid,'bbox':box,'confidence':round(score,5)})
            trace.write(json.dumps({'frame':frame_number,'seconds':round(t,5),'observations':obs})+'\n')
            if obs: detect_frames+=1
            fresh=[]
            for o in obs:
                tid=o['track_id'];ids.add(tid); x1,y1,x2,y2=o['bbox']
                anchor=((x1+x2)/2/w,(y2 if cfg['anchor']=='bottom_center' else (y1+y2)/2)/h)
                event=counter.update(tid,anchor,t)
                if event:
                    event.update(confidence=o['confidence'],snapshot=f'evidence/T{tid}_{event["sequence"]}.jpg')
                    cv2.imwrite(str(folder/event['snapshot']),frame)
                    event_id=db.record(event);fresh.append((event_id,event))
                cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(70,220,90),2)
                cv2.putText(frame,f'T{tid} horse {o["confidence"]:.2f}',(max(0,int(x1)),max(85,int(y1)-7)),cv2.FONT_HERSHEY_SIMPLEX,.48,(40,230,80),1,cv2.LINE_AA)
                cv2.circle(frame,(int(anchor[0]*w),int(anchor[1]*h)),4,(0,220,255),-1)
            a,b=[(int(p[0]*w),int(p[1]*h)) for p in cfg['line']]
            cv2.line(frame,a,b,(0,230,255),2)
            cv2.rectangle(frame,(0,0),(w,75),(25,48,34),-1)
            cv2.putText(frame,f'EquinoID | EN {counter.entries}  SA {counter.exits}',(10,24),cv2.FONT_HERSHEY_SIMPLEX,.6,(255,255,255),2)
            aforo='ND' if counter.occupancy is None else str(counter.occupancy)
            cv2.putText(frame,f'Aforo {aforo} | {t:.2f}s | identidad por confirmar',(10,50),cv2.FONT_HERSHEY_SIMPLEX,.4,(240,240,240),1)
            if frames in (30,90,180,300): cv2.imwrite(str(folder/f'frame_{frames:04d}.jpg'),frame)
            if writer: writer.write(frame)
            if show:
                cv2.imshow('EquinoID - q termina',frame)
                if cv2.waitKey(1)&255==ord('q'): status='PARCIAL_USUARIO';break
            if frames%60==0: print(f'{frames}/{expected or "camara"} cuadros | entradas={counter.entries} salidas={counter.exits}',flush=True)
            if frames%300==0: counter.prune(t)
    except KeyboardInterrupt:
        status='PARCIAL_USUARIO'
    except Exception as exc:
        status='ERROR';error=str(exc)
    finally:
        elapsed=time.perf_counter()-start
        cap.release();trace.close()
        if writer: writer.release()
        if show: cv2.destroyAllWindows()
        summary.update(status=status,error=error,processed_frames=frames,frames_with_tracks=detect_frames,distinct_track_ids=len(ids),
                       entries=counter.entries,exits=counter.exits,occupancy=counter.occupancy,video_seconds=frames/fps if local else elapsed,
                       elapsed_seconds=round(elapsed,3),processing_fps=round(frames/elapsed,2),
                       permanent_identity='MANUAL_CONFIRMATION_ONLY',real_farm_deployment=False)
        (folder/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
        db.export(folder/'events.csv');db.close();make_report(folder)
    if error: raise RuntimeError(error)
    return summary

def calibrate(source,output):
    import cv2
    cap=cv2.VideoCapture(int(source) if str(source).isdigit() else str(source));ok,frame=cap.read();cap.release()
    if not ok: raise ValueError('No se pudo leer un cuadro para calibrar.')
    cfg=json.loads(Path('config/demo.json').read_text(encoding='utf-8'));points=[];h,w=frame.shape[:2]
    def click(event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDOWN and len(points)<2: points.append([x/w,y/h])
    cv2.namedWindow('Dos clics: linea. ENTER guarda. ESC cancela.');cv2.setMouseCallback('Dos clics: linea. ENTER guarda. ESC cancela.',click)
    while True:
        show=frame.copy()
        for p in points: cv2.circle(show,(int(p[0]*w),int(p[1]*h)),6,(0,255,255),-1)
        if len(points)==2: cv2.line(show,tuple(int(v*s) for v,s in zip(points[0],(w,h))),tuple(int(v*s) for v,s in zip(points[1],(w,h))),(0,255,255),2)
        cv2.imshow('Dos clics: linea. ENTER guarda. ESC cancela.',show);key=cv2.waitKey(30)&255
        if key==27: break
        if key in (10,13) and len(points)==2:
            cfg['line']=points
            LineCounter(*points)
            # x-mode prevents accidental overwrite of a validated camera config.
            with Path(output).open('x',encoding='utf-8') as f: json.dump(cfg,f,ensure_ascii=False,indent=2)
            break
    cv2.destroyAllWindows()
