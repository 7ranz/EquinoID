# Informe final de cumplimiento

Hacienda Chamusca · EquinoID 1.0 · 23 de septiembre de 2026

**Conclusión:** proyecto entregado como prototipo local funcional, con programa, manuales, evidencias y presentación. El piloto no supera todavía los criterios propuestos para operar sin supervisión: omite dos pasos de la referencia provisional y procesa a menor velocidad que la fuente. No se realizó una instalación física ni se demostraron ahorros reales.

## Cumplimiento

| Solicitud | Entrega | Estado |
|---|---|---|
| Plantear problema y solución | Dossier, secciones 1–3 | Cumplido |
| Esquemas e imágenes explicativas | Arquitectura, identidad y fotogramas reales | Cumplido |
| Desarrollo Python con YOLO | src/equinoid, configuración y lanzadores | Cumplido |
| Manual de uso | manual_usuario.md y dossier | Cumplido |
| Manual técnico | manual_desarrollo.md y dossier | Cumplido |
| Probar video aportado | results/piloto_v1 con 425 cuadros procesados | Cumplido con limitaciones |
| Identificar por nombre | Catálogo ficticio y confirmación manual auditada | Implementado como flujo asistido |
| Presentar beneficios y costos | Caso económico con fórmulas y sensibilidad | Cumplido como simulación |
| Presentación a accionistas | EquinoID_Accionistas.pptx, 12 diapositivas | Cumplido |
| Instalación en una cámara de campo | Instrucciones y plan | No ejecutada |

## Resultados medidos

| Indicador | Resultado |
|---|---:|
| Duración de la muestra | 14,1667 s |
| Resolución | 478 × 850 |
| Cuadros / FPS de fuente | 425 / 30 |
| Entradas / salidas registradas | 11 / 0 |
| Pasos de referencia provisional | 13 |
| TP / FP / FN por emparejamiento temporal | 11 / 0 / 2 |
| Sensibilidad descriptiva | 84,6% |
| Precisión descriptiva | 100% en este clip |
| F1 descriptivo | 91,7% |
| Error absoluto del total | 2 pasos |
| Tiempo de procesamiento | 258,879 s |
| Rendimiento del análisis completo | 1,64 FPS |
| ID temporales distintos | 19, no equivalen a 19 caballos |
| Pruebas automatizadas aprobadas | 22 |

Referencia visual de un observador con incertidumbre temporal aproximada ±0,3 s. Se emparejó por sentido y tolerancia de 0,6 s. Se usó el mismo clip para calibrar y evaluar; los porcentajes no estiman el desempeño en videos nuevos. Se requiere otro observador y material independiente. No se midió exactitud de nombres.

R06 y R07 no se emparejaron, alrededor de 4,12 y 4,70 s. El grupo presenta oclusiones. La traza muestra pérdida y posible intercambio de ID. Explorar x=0,50 a 0,75 sobre las mismas detecciones no superó 11 entradas; no se alteraron manualmente los resultados para alcanzar 13.

## Beneficios del caso simulado

| Concepto | Supuesto |
|---|---:|
| Inversión inicial | USD 4.800 |
| Operación y provisión de licencia por año | USD 3.000 |
| Costo anual antes | USD 20.320 |
| Costo anual después | USD 9.912 |
| Beneficio neto anual | USD 10.408 |
| Flujo neto del primer año | USD 5.608 |
| Recuperación simple | 5,53 meses |
| ROI del primer año | 116,8% |

Datos inventados por solicitud del usuario. No son cotizaciones ni metas realmente obtenidas. La reducción supuesta de seis a dos pérdidas requiere gestión de accesos y respuesta humana. Si no se evita ninguna pérdida y solo se logra el ahorro laboral supuesto, el saldo anual sería negativo en USD 792.

## Recomendación de cierre

Aceptar los entregables del prototipo. Mantener pendientes la aceptación operativa y la validación empresarial. La siguiente etapa debe mejorar la posición de cámara, reunir al menos 500 pasos independientes con dos revisores, evaluar día y noche, optimizar hardware y confirmar presupuesto y licencia. La identificación RFID se propone para una versión futura; las etiquetas entregadas no corresponden a dispositivos reales.

## Trazabilidad

- Video SHA256: `4990f920e74d65faaf0755ad5ce27d8dd83ed26354d3986a8c04e0875c6ecc4e`.
- Modelo SHA256: `85a76fe86dd8afe384648546b56a7a78580c7cb7b404fc595f97969322d502d5`.
- Configuración exacta: `results/piloto_v1/config_used.json`.
- Versiones y tiempos: `results/piloto_v1/summary.json`.
- Eventos y evidencia: `events.sqlite`, `events.csv`, `evidence` y `annotated.mp4`.
- Método y referencias: `data/reference_protocol.md` y `reference_events.csv`.
- Fuentes externas: `docs/fuentes_y_licencias.md`.
