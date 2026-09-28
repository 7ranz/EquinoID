# EquinoID

**Hacienda Chamusca · versión 1.0 · piloto local sobre video**

Detecta caballos con YOLO11s, sigue trayectorias con ByteTrack y registra entradas y salidas al cruzar una línea. Incluye evidencia por evento, SQLite, CSV, video anotado y panel HTML local. La identidad permanente se confirma manualmente con evidencia; un ID de seguimiento no equivale al nombre del animal.

## Inicio rápido en Windows

1. Abrir `results/piloto_v1/panel.html` para consultar la prueba ya realizada.
2. Para repetirla, instalar Python 3.13 y ejecutar `INSTALAR.cmd` una vez. Requiere internet para paquetes y, si falta, el modelo.
3. Ejecutar `DEMO.cmd`. Cada ejecución crea una carpeta nueva y abre el panel al terminar.

Desde PowerShell, en esta carpeta:

```powershell
.\.venv\Scripts\python.exe -m equinoid analyze --source data/video_equino.mp4 --config config/demo.json --output results/mi_prueba
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Entregables

| Archivo o carpeta | Contenido |
|---|---|
| `docs/EquinoID_Dossier.pdf` | Problema, solución, manuales, evaluación, costos simulados e informe final |
| `docs/EquinoID_Accionistas.pptx` | Presentación ejecutiva editable |
| `docs/manual_usuario.md` | Instalación, calibración, ejecución y revisión de identidades |
| `docs/manual_desarrollo.md` | Módulos, algoritmos, esquema de datos y extensión |
| `docs/informe_final.md` | Cumplimiento y limitaciones verificadas |
| `src/equinoid` | Código Python modular |
| `tests` | Pruebas de conteo, auditoría y cálculos económicos |
| `data` | Video aportado, catálogo ficticio, referencia manual y escenario económico |
| `config/demo.json` | Configuración ajustada a este clip |
| `results/piloto_v1` | Salida real del análisis y evaluación descriptiva |
| `assets` | Esquemas e imágenes explicativas |

## Límites que afectan el uso

- El video tiene marca de agua de una cuenta de terceros. Es material aportado para pruebas, no evidencia de una instalación en Hacienda Chamusca.
- Catálogo, RFID de ejemplo y cifras económicas son ficticios. No se conectó un lector RFID ni se entrenó reconocimiento biométrico individual.
- Un conteo pendiente o una salida no autorizada por revisión humana no demuestra robo. El conteo ayuda a investigar y conciliar el inventario.
- La prueba es diurna, corta y sobre el mismo clip usado para ajustar la línea. Se necesita un conjunto independiente y pruebas de campo antes del uso operativo.
- El aforo queda sin confirmar cuando se desconoce la ocupación inicial. Si se configura y resulta negativo, se conserva la discrepancia para revisión.

Consulta `docs/fuentes_y_licencias.md` para atribuciones y condiciones de distribución. La carpeta `.venv` es local y no forma parte del ZIP entregable.
