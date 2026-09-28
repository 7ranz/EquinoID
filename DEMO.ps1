$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) { throw 'Ejecuta primero INSTALAR.cmd.' }
$equinoRun = 'results/local_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff')
& './.venv/Scripts/python.exe' -m equinoid analyze --source data/video_equino.mp4 --config config/demo.json --output $equinoRun
if ($LASTEXITCODE -ne 0) { throw 'El análisis no terminó correctamente. Revisa la consola y summary.json.' }
Start-Process -FilePath (Join-Path $PSScriptRoot ($equinoRun + '/panel.html'))
