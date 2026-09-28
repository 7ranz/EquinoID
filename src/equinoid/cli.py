import argparse,json,sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='EquinoID 1.0 · Hacienda Chamusca · ejecutar desde la raíz del proyecto')
    sub=ap.add_subparsers(dest='command',required=True)
    a=sub.add_parser('analyze',help='Detectar y contar caballos en archivo, webcam o RTSP')
    a.add_argument('--source',required=True);a.add_argument('--config',default='config/demo.json');a.add_argument('--output',required=True)
    a.add_argument('--show',action='store_true');a.add_argument('--max-seconds',type=float)
    a.add_argument('--replay-tracks',help='Solo desarrollo: detecciones previamente calculadas sobre exactamente el mismo video')
    c=sub.add_parser('calibrate',help='Marcar línea de conteo con dos clics');c.add_argument('--source',required=True);c.add_argument('--output',required=True)
    r=sub.add_parser('report',help='Actualizar panel y CSV desde SQLite');r.add_argument('--run',required=True)
    i=sub.add_parser('identify',help='Confirmar identidad de un evento con evidencia del operador')
    for k in ['run','horse','operator','evidence']: i.add_argument('--'+k,required=True)
    i.add_argument('--event',type=int,required=True)
    e=sub.add_parser('evaluate',help='Comparar pasos con referencia manual')
    e.add_argument('--run',required=True);e.add_argument('--reference',required=True);e.add_argument('--tolerance',type=float,default=.6)
    args=ap.parse_args()
    try:
        if args.command=='analyze':
            from .pipeline import analyze
            if args.max_seconds is not None and args.max_seconds<=0: raise ValueError('max-seconds debe ser positivo.')
            result=analyze(args.source,args.config,args.output,show=args.show,max_seconds=args.max_seconds,replay=args.replay_tracks)
        elif args.command=='calibrate':
            from .pipeline import calibrate
            calibrate(args.source,args.output);result={'config':args.output}
        elif args.command=='report':
            from .reporting import make_report
            result={'panel':str(make_report(args.run))}
        elif args.command=='identify':
            from .storage import Store
            from .reporting import make_report
            database=Path(args.run)/'events.sqlite'
            if not database.is_file(): raise ValueError('No existe la ejecución.')
            db=Store(database)
            try: db.identify(args.event,args.horse,args.operator,args.evidence)
            finally: db.close()
            result={'panel':str(make_report(args.run)),'identity':'Confirmación manual registrada'}
        else:
            from .evaluation import evaluate
            result=evaluate(args.run,args.reference,args.tolerance)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,FileNotFoundError,RuntimeError,KeyError) as exc:
        print(f'EquinoID: {exc}',file=sys.stderr);sys.exit(2)

if __name__=='__main__': main()
