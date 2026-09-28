# Fuentes y licencias

Consulta documental: 23 de septiembre de 2026. El código de EquinoID toma como referencia conceptual `01-contador-personas/contador.py`, proporcionado por el usuario. Las recomendaciones de despliegue y los riesgos del caso son análisis técnico propio, no promesas de los fabricantes.

| Componente | Función | Licencia y costo de software | Fuente primaria |
|---|---|---|---|
| Ultralytics 8.3.221 y YOLO11s | Detección de la clase horse y motor de seguimiento | AGPL-3.0 o Enterprise; modalidad comercial por cotización | https://docs.ultralytics.com/models/yolo11/ y https://www.ultralytics.com/license |
| ByteTrack integrado | Asignación temporal de ID | Implementación distribuida por Ultralytics bajo sus términos; no se instaló otro paquete ByteTrack | https://github.com/ultralytics/ultralytics/blob/v8.3.221/ultralytics/cfg/trackers/bytetrack.yaml |
| PyTorch 2.9.0 y torchvision 0.24.0 | Inferencia y operaciones de visión | BSD, con avisos de terceros; sin tarifa del núcleo | https://github.com/pytorch/pytorch/blob/main/LICENSE y https://github.com/pytorch/vision/blob/main/LICENSE |
| OpenCV 4.14.0.94 | Captura, cajas y grabación | Núcleo Apache-2.0, empaquetado MIT; binarios con licencias adicionales | https://opencv.org/license/ y https://pypi.org/project/opencv-python/ |
| NumPy 2.5.3 | Arreglos y validación numérica | BSD-3-Clause, sin tarifa | https://numpy.org/doc/stable/license.html |
| lap 0.5.12 | Asignación lineal que utiliza el rastreador | BSD-2-Clause según repositorio, sin tarifa | https://github.com/gatagat/lap |
| Python y módulos estándar | CLI, JSON, CSV, geometría, tiempos y archivos | PSF y avisos aplicables; sin tarifa por módulo | https://docs.python.org/3/license.html |
| sqlite3 | Base local y transacciones | Módulo de Python; SQLite en dominio público | https://docs.python.org/3/library/sqlite3.html y https://sqlite.org/copyright.html |

Las versiones son el perfil probado; no se afirma que sean las más recientes ni que carezcan de vulnerabilidades. El archivo `environment_snapshot.txt` registra el entorno utilizado, incluyendo paquetes auxiliares preexistentes que no son todos necesarios para EquinoID. `requirements.txt` fija las dependencias principales. ByteTrack es un algoritmo de seguimiento, no identifica por nombre ni ofrece identidad persistente entre cámaras.

El código nuevo se entrega bajo AGPL-3.0-only, cuyo texto figura en LICENSE. Esto no cambia la licencia de datos, videos, modelos ni dependencias. Se requiere revisar las obligaciones de distribución y acceso por red antes de una integración propietaria. El proveedor ofrece Enterprise para esa modalidad; los USD 1800 del caso económico son una provisión ficticia, no una cotización. No se compró ninguna licencia.

## Fuentes de datos

| Dato | Procedencia y límite |
|---|---|
| Video de prueba | Archivo aportado por el usuario. Marca de agua visible de TikTok y cuenta countrysidestablespenang. No se verificó autoría ni relación con Hacienda Chamusca |
| Fotogramas y video anotado | Derivados del video aportado para la evaluación local. Se conserva la atribución visible |
| Referencia de 13 pasos | Inspección visual provisional por un observador; protocolo en data/reference_protocol.md |
| Nombres EQ y RFID de ejemplo | Inventados para explicar el catálogo; no corresponden a identidades comprobadas del video |
| Pérdidas, precios y ahorros | Supuestos educativos autorizados por el usuario; no provienen de la contabilidad de una hacienda real |
| Pruebas técnicas | Ejecución local documentada en results/piloto_v1 y tests |

Documentación adicional: https://docs.ultralytics.com/modes/track/ y https://docs.ultralytics.com/datasets/detect/coco/. La documentación en línea evoluciona; la configuración de ByteTrack se referencia con la etiqueta de la versión instalada.
