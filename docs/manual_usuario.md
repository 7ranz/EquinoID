# Manual de uso de EquinoID

## 1 Preparación

| Elemento | Requisito |
|---|---|
| Entorno probado | Windows y Python 3.13, CPU |
| Instalación | Ejecutar INSTALAR.cmd desde la carpeta del proyecto |
| Acceso inicial a internet | Instalación de paquetes y descarga del modelo si no está presente |
| Espacio sugerido | 3 GB libres como mínimo orientativo; conservar espacio adicional para grabaciones |
| Cámara | USB o URL RTSP compatible con OpenCV; aún no probada en campo |
| Operador | Responsable de revisar evidencia y confirmar identidades |

El perfil instala PyTorch para CPU. Una GPU puede requerir un perfil de dependencias diferente. El video de muestra es un recurso de prueba, no una cámara real de la hacienda.

## 2 Ejecutar la muestra

Abrir `DEMO.cmd` o ejecutar desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m equinoid analyze --source data/video_equino.mp4 --config config/demo.json --output results/nueva_prueba
```

El directorio de salida debe ser nuevo. No se reemplazan ejecuciones previas. El primer arranque puede tardar; la consola muestra el avance cada 60 cuadros. `--show` muestra la ventana, `q` finaliza conservando resultados parciales y `--max-seconds 10` limita una prueba. Ctrl+C también conserva una ejecución parcial una vez iniciado el procesamiento.

## 3 Configurar otra cámara

```powershell
.\.venv\Scripts\python.exe -m equinoid calibrate --source data/video_equino.mp4 --output config/otra_camara.json
```

Hacer dos clics sobre la imagen, Enter para guardar o Esc para cancelar. El archivo de configuración debe ser nuevo. Después editarlo: la herramienta solo define la línea; no determina el sentido, aforo ni umbrales.

| Parámetro | Cómo decidirlo |
|---|---|
| line | Dos puntos normalizados de 0 a 1; evitar zonas de oclusión |
| anchor | center o bottom_center; el ejemplo usa centro de caja |
| invert | Invierte qué sentido significa entrada; comprobar con un paso conocido |
| initial_occupancy | Número de caballos realmente presentes al iniciar, o null si se desconoce |
| confidence | Confianza mínima de YOLO, no garantía de exactitud |
| stable_frames | Observaciones consecutivas del lado nuevo; 2 en la muestra |
| deadband | Banda alrededor de la línea para ignorar oscilaciones pequeñas |
| max_gap | Interrupción máxima del seguimiento antes de reiniciar el estado de cruce |
| device | cpu en el perfil probado; cambiar solo con un entorno GPU compatible |

En el ejemplo, la línea vertical x=0,65 registra pasos hacia la derecha como entradas. Es una convención de la demostración, no una afirmación sobre la orientación real del acceso. Para una webcam usar `--source 0`. Para RTSP usar una URL autorizada; no incluir credenciales en documentos ni compartir la consola que las contenga. Usar `--max-seconds 60` para una primera prueba de cámara.

## 4 Revisar resultados

| Resultado | Uso |
|---|---|
| panel.html | Resumen de pasos y acceso a imágenes |
| annotated.mp4 | Video con cajas, ID temporales y línea |
| events.csv | Tabla exportable con tiempo relativo al video y dirección |
| events.sqlite | Registro principal y auditoría de nombres confirmados |
| evidence | Fotograma fuente completo de cada evento |
| tracks.jsonl | Detecciones y trayectorias para reproducir el análisis técnico |
| summary.json | Estado completo o parcial, rendimiento, versiones y huellas SHA256 |
| config_used.json | Configuración que produjo esta ejecución |

Si el navegador no reproduce MP4V, abrir annotated.mp4 con un reproductor compatible. El panel no requiere servidor, internet ni carga de videos a terceros. Es estático: volver a generarlo después de una actualización externa de la base.

## 5 Confirmar un nombre

Primero revisar el evento y contrastarlo con una ficha real, marca o registro autorizado. Los EQ y nombres entregados son ejemplos ficticios. Para practicar sobre una copia de los resultados:

```powershell
.\.venv\Scripts\python.exe -m equinoid identify --run results/copia_para_practica --event 1 --horse EQ-001 --operator "Operador de prueba" --evidence "SIMULACION: asignacion ficticia a Saturno para practicar"
```

La asignación corresponde a un evento de una ejecución, no se propaga automáticamente a futuros videos. Cada cambio guarda operador, evidencia, identidad anterior y nueva, y fecha UTC. Repetir el comando permite corregir con auditoría. Para uso real, sustituir el catálogo ficticio antes de una nueva ejecución y registrar nombres verificados.

## 6 Operación y solución de problemas

| Síntoma | Acción |
|---|---|
| No abre el video | Verificar ruta, permisos o conexión de cámara |
| Cuenta al revés | Revisar invert con un paso conocido |
| Caballos omitidos | Revisar oclusión, posición de cámara, línea y modelo; comparar con conteo manual |
| Duplicados | Revisar fragmentación de ID y cruces inversos por oscilación |
| Aforo negativo | Conciliar aforo inicial y errores; no ocultar la discrepancia |
| Lento | Comparar processing_fps con FPS de fuente; probar menor resolución o GPU y volver a validar |
| Sin nombre | Estado esperado hasta confirmación manual |
| Ejecución parcial | Revisar status y error en summary.json antes de usar los totales |

Al cierre del turno: revisar pasos pendientes, conciliar inventario físico, copiar la carpeta de resultados a un respaldo y registrar incidentes. Política propuesta, aún no implementada: conservar videos 30 días y registros 12 meses según necesidades y autorizaciones de la hacienda. La versión 1.0 no aplica eliminación automática, usuarios ni cifrado de base de datos.
