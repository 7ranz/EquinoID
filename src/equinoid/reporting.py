"""Panel estático local, sin servicios externos ni datos económicos simulados."""
import html,json
from pathlib import Path
from .storage import Store

def make_report(folder):
    folder=Path(folder)
    meta=json.loads((folder/'summary.json').read_text(encoding='utf-8'))
    db=Store(folder/'events.sqlite'); events=db.events(); db.export(folder/'events.csv');db.close()
    esc=lambda v: html.escape(str(v if v is not None else 'Sin confirmar'))
    body=''
    for e in events:
        name=e['name'] or 'Pendiente'
        if e['fictional']: name+=' (catálogo ficticio)'
        body+=f'<tr><td>{e["event_id"]}</td><td>T{e["track_id"]}</td><td>{e["video_seconds"]:.2f}</td><td>{e["direction"]}</td><td>{esc(name)}</td><td>{esc(e["horse_id"])}</td><td>{e["confidence"]:.2f}</td><td><a href="{esc(e["snapshot"])}">Ver evidencia</a></td></tr>'
    text=f'''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EquinoID · Registro de pasos</title>
    <style>body{{font:17px/1.5 Segoe UI,Arial;margin:36px;background:#f7f8f4;color:#193932}}h1{{font-size:36px}}table{{border-collapse:collapse;width:100%;background:white}}td,th{{padding:12px;border:1px solid #cad8d0;text-align:left}}th{{background:#224c3a;color:white}}a{{color:#246c55}}video{{max-width:390px;width:100%}}.wrap{{overflow:auto}}small{{color:#4b625a}}</style>
    <h1>EquinoID · {esc(meta['farm'])}</h1><p>Registro de prueba local · cámara {esc(meta['camera'])}</p>
    <p><strong>{meta['entries']} entradas · {meta['exits']} salidas</strong> · Aforo: {esc(meta['occupancy'])} · {len(events)} pasos registrados.</p>
    <p>Los ID T identifican trayectorias de esta ejecución. No identifican de forma permanente un caballo. Un paso pendiente no demuestra una pérdida.</p>
    <p>Estado: {esc(meta['status'])}. Video analizado: {meta['video_seconds']:.2f} s. Rendimiento observado: {meta['processing_fps']:.1f} cuadros/s. Pendientes de identidad: {sum(e['horse_id'] is None for e in events)}.</p>
    <p><a href="annotated.mp4">Abrir video anotado</a> · <a href="events.csv">Descargar CSV</a> · <a href="summary.json">Detalles técnicos</a></p>
    <div class="wrap"><table><tr><th>Evento</th><th>Trayectoria</th><th>Segundo</th><th>Sentido</th><th>Nombre</th><th>ID catálogo</th><th>Conf. detector</th><th>Imagen</th></tr>{body}</table></div>
    <p><small>La confianza del detector no es exactitud validada. El registro económico simulado se entrega aparte y nunca se mezcla con estos eventos.</small></p></html>'''
    (folder/'panel.html').write_text(text,encoding='utf-8')
    return folder/'panel.html'
