# Manual del desarrollo

## Base y decisiones

El proyecto 01-contador-personas aportó el patrón video, detección, seguimiento, línea de cruce y CSV. EquinoID reimplementa esa arquitectura por módulos: cambia persona por horse, utiliza YOLO11s y ByteTrack, agrega banda de tolerancia y permite pasos posteriores en sentido inverso. El contador inicial marcaba cada persona como contada una sola vez; aquí se registran cruces, no individuos únicos permanentes.

## Estructura

| Módulo | Responsabilidad | Dependencias directas |
|---|---|---|
| cli.py | Comandos y validación de argumentos | argparse, json, pathlib, sys |
| pipeline.py | Captura, YOLO, ByteTrack, imágenes, video y ejecución | OpenCV, NumPy, Ultralytics, PyTorch y módulos estándar |
| counting.py | Estado por ID, geometría y sentido | dataclasses, math |
| storage.py | Eventos, catálogo, transacciones y auditoría | sqlite3, csv, datetime, pathlib |
| reporting.py | Panel HTML y exportación | html, json, pathlib |
| evaluation.py | Emparejar eventos con referencia temporal | csv, json, pathlib |
| economics.py | Calcular únicamente el escenario simulado | json, pathlib |

## Flujo del procesamiento

1. Validar configuración, catálogo, fuente y destino nuevo.
2. Cargar YOLO11s y buscar la clase cuyo nombre es horse, en lugar de asumir un número fijo.
3. Procesar todos los cuadros con model.track y ByteTrack, persistiendo su estado dentro de la ejecución.
4. Obtener centro o centro inferior de cada caja, normalizado por dimensiones del video.
5. Calcular distancia firmada a la línea. Ignorar la banda, exigir estabilidad y verificar que el trayecto interseca el segmento.
6. Crear evento cuando cambia de lado, respetando intervalo mínimo. Reiniciar estado ante una ausencia larga.
7. Guardar fotograma, evento SQLite y evidencia técnica. Terminar liberando captura y escritor incluso ante errores del bucle.

## Datos y semántica

| Tabla | Clave y contenido |
|---|---|
| horses | horse_id, nombre, etiqueta de ejemplo y marca fictional |
| events | event_id, track_id, secuencia de cruce, segundo, dirección, aforo, confianza, imagen, horse_id opcional |
| audit | Identidades anterior y nueva, operador, evidencia y fecha UTC |

Restricción única: track_id y sequence dentro de cada archivo de ejecución. SQLite impone integridad del horse_id. Cada confirmación manual y su auditoría se guardan en una misma transacción. No existe usuario autenticado: operator es texto declarado. Esta auditoría aporta trazabilidad, pero no es inmutable frente a quien tenga permiso de escritura al archivo.

Tiempo de eventos en archivo: índice de cuadro / FPS. En cámara: reloj monotónico. Las marcas UTC describen la ejecución y la revisión, no la fecha original de grabación. Aforo = inicial + entradas − salidas. Sin inicial confirmado devuelve null. Un resultado negativo se conserva y marca para investigar.

## Pruebas y evaluación

Ejecutar `python -m unittest discover -s tests -v`. Las pruebas desacoplan la geometría del detector, cubren cruces y auditoría, y verifican la aritmética económica. Para evaluar el video: `python -m equinoid evaluate --run results/piloto_v1 --reference data/reference_events.csv`.

Las métricas comparan pasos, no identidades ni píxeles segmentados. El número de ID distintos no equivale al número de caballos. La referencia temporal es provisional, de un observador. No se entrenó un modelo personalizado y no existe conjunto de prueba independiente.

## Extensión y riesgos técnicos

| Necesidad futura | Cambio propuesto | Evidencia requerida |
|---|---|---|
| Identidad automática permanente | Lector RFID y conciliación temporal, o modelo ReID con datos etiquetados | Lecturas y fichas reales por animal |
| Mayor robustez | Cámara elevada lateral, iluminación y dataset propio | Videos independientes diurnos y nocturnos |
| Varias cámaras | Servicio por cámara y base central | Pruebas de concurrencia y sincronización |
| Operación continua | Cola de captura, watchdog y reconexión RTSP | Ensayo de 24 h y cortes de red |
| Control de acceso | Usuarios, permisos, cifrado y auditoría protegida | Pruebas de acceso y recuperación |

El modo --replay-tracks es una herramienta de desarrollo para el mismo video; sirve para explorar la línea sin repetir inferencia. Las cifras de velocidad de un replay no miden velocidad de YOLO. La grabación de fuente en vivo aún no tiene reconexión ni garantía de tiempo real.
