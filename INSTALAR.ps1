$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$equinoPython = Join-Path $env:LOCALAPPDATA 'Programs/Python/Python313/python.exe'
if (-not (Test-Path -LiteralPath $equinoPython)) {
    $equinoCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $equinoCommand) { throw 'Instala Python 3.13 de python.org y vuelve a ejecutar.' }
    $equinoPython = $equinoCommand.Source
}
if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
    & $equinoPython -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el entorno Python.' }
}
& './.venv/Scripts/python.exe' -m pip install torch==2.9.0 torchvision==0.24.0 --index-url https://download.pytorch.org/whl/cpu
if ($LASTEXITCODE -ne 0) { throw 'Falló la instalación de PyTorch.' }
& './.venv/Scripts/python.exe' -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Falló la instalación de dependencias.' }
& './.venv/Scripts/python.exe' -m pip install -e . --no-deps
if ($LASTEXITCODE -ne 0) { throw 'Falló la instalación de EquinoID.' }
Write-Host 'Listo. Ejecuta DEMO.cmd o consulta docs/manual_usuario.md.'
