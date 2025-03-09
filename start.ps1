# Deactivate any active virtual environment
if (Test-Path env:VIRTUAL_ENV) {
    deactivate
}

# Load environment variables from local.settings.json
$localSettings = Get-Content -Raw -Path "local.settings.json" | ConvertFrom-Json
foreach ($key in $localSettings.PSObject.Properties.Name) {
    $value = $localSettings.$key
    [System.Environment]::SetEnvironmentVariable($key, $value)
}

# Activate the virtual environment
$venvPath = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
} else {
    Write-Host "Virtual environment not found. Creating a new one..."
    python -m venv .venv
    & $venvPath
}

# Install requirements
pip install -r requirements.txt

# Run the FastAPI app with uvicorn
uvicorn api.app:app --host 0.0.0.0 --port 9000 --reload