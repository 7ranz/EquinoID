"""Comparación uno a uno de eventos contra referencias manuales del mismo video."""
import csv,json
from pathlib import Path

def evaluate(folder,reference,tolerance=0.6):
    if tolerance<=0: raise ValueError('La tolerancia debe ser positiva.')
    with (Path(folder)/'events.csv').open(encoding='utf-8-sig') as f: predicted=list(csv.DictReader(f))
    with Path(reference).open(encoding='utf-8-sig') as f: truth=list(csv.DictReader(f))
    # Matching por menor diferencia temporal, independiente del ID del tracker.
    candidates=sorted((abs(float(p['video_seconds'])-float(g['video_seconds'])),i,j)
                      for i,p in enumerate(predicted) for j,g in enumerate(truth)
                      if p['direction']==g['direction'] and abs(float(p['video_seconds'])-float(g['video_seconds']))<=tolerance)
    matched_p=set();matched_g=set();pairs=[]
    for dt,i,j in candidates:
        if i not in matched_p and j not in matched_g:
            matched_p.add(i);matched_g.add(j);pairs.append({'event_id':predicted[i]['event_id'],'reference_id':truth[j]['reference_id'],'delta_seconds':round(dt,3)})
    tp=len(pairs);fp=len(predicted)-tp;fn=len(truth)-tp
    metrics={'scope':'Descriptivo sobre el mismo clip usado para ajustar la línea. No es validación independiente.',
             'reference_type':'manual_visual_single_reviewer','reference_events':len(truth),'predicted_events':len(predicted),
             'true_positive':tp,'false_positive':fp,'false_negative':fn,'precision':tp/(tp+fp) if tp+fp else None,
             'recall':tp/(tp+fn) if tp+fn else None,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None,
             'absolute_count_error':abs(len(predicted)-len(truth)),'tolerance_seconds':tolerance,'pairs':pairs,
             'unmatched_predictions':[predicted[i] for i in range(len(predicted)) if i not in matched_p],
             'unmatched_reference':[truth[j] for j in range(len(truth)) if j not in matched_g]}
    (Path(folder)/'evaluation.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    return metrics
