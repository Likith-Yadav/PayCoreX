# Script to update PostgreSQL password in .env file
param(
    [Parameter(Mandatory=$true)]
    [string]$Password
)

$envFile = ".env"

if (-not (Test-Path $envFile)) {
    Write-Host "Error: .env file not found!" -ForegroundColor Red
    exit 1
}

$content = Get-Content $envFile
$updated = $content | ForEach-Object {
    if ($_ -match "^DB_PASSWORD=") {
        "DB_PASSWORD=$Password"
    } else {
        $_
    }
}

$updated | Set-Content $envFile
Write-Host "✓ Updated DB_PASSWORD in .env file" -ForegroundColor Green
Write-Host "`nNext: Run 'python manage.py migrate' to create database tables"

