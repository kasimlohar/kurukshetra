# ConfluxAI Project Cleanup Script
# Run this script to clean up the project directory

Write-Host "🧹 ConfluxAI Project Cleanup Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

$projectRoot = "d:\Kurushetra hackathon\kurukshetra\ConfluxAI_hybrid"

# Function to get directory size
function Get-DirectorySize {
    param([string]$Path)
    if (Test-Path $Path) {
        $size = (Get-ChildItem -Path $Path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        return [math]::Round($size/1MB, 2)
    }
    return 0
}

# Check current size
$currentSize = Get-DirectorySize $projectRoot
Write-Host "📊 Current project size: $currentSize MB" -ForegroundColor Yellow

# 1. Clean frontend node_modules (optional - saves most space)
$nodeModulesPath = Join-Path $projectRoot "frontend\node_modules"
if (Test-Path $nodeModulesPath) {
    $nodeSize = Get-DirectorySize $nodeModulesPath
    Write-Host ""
    Write-Host "🗂️  Found node_modules: $nodeSize MB" -ForegroundColor Magenta
    $response = Read-Host "Remove node_modules? (saves ~$nodeSize MB) [y/N]"
    
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "🗑️  Removing node_modules..." -ForegroundColor Red
        Remove-Item -Path $nodeModulesPath -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "✅ node_modules removed. Run 'npm install' in frontend/ to reinstall." -ForegroundColor Green
    }
}

# 2. Clean Python cache (already clean, but check)
Write-Host ""
Write-Host "🐍 Checking Python cache files..." -ForegroundColor Blue
$pycacheFiles = Get-ChildItem -Path $projectRoot -Recurse -Name "__pycache__" -ErrorAction SilentlyContinue
if ($pycacheFiles.Count -gt 0) {
    Write-Host "🗑️  Removing Python cache files..." -ForegroundColor Red
    Get-ChildItem -Path $projectRoot -Recurse -Name "__pycache__" | Remove-Item -Recurse -Force
    Write-Host "✅ Python cache files removed." -ForegroundColor Green
} else {
    Write-Host "✅ No Python cache files found." -ForegroundColor Green
}

# 3. Clean temporary directories
Write-Host ""
Write-Host "📁 Cleaning temporary directories..." -ForegroundColor Blue

$tempDirs = @("temp", "logs", "uploads")
foreach ($dir in $tempDirs) {
    $dirPath = Join-Path $projectRoot $dir
    if (Test-Path $dirPath) {
        $files = Get-ChildItem -Path $dirPath -Recurse
        if ($files.Count -gt 0) {
            Write-Host "🗑️  Cleaning $dir..." -ForegroundColor Red
            Remove-Item -Path "$dirPath\*" -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "✅ $dir cleaned." -ForegroundColor Green
        } else {
            Write-Host "✅ $dir already clean." -ForegroundColor Green
        }
    }
}

# 4. Show final size
Write-Host ""
$finalSize = Get-DirectorySize $projectRoot
$savedSpace = $currentSize - $finalSize
Write-Host "📊 Final project size: $finalSize MB" -ForegroundColor Yellow
Write-Host "💾 Space saved: $savedSpace MB" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Cleanup completed!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 To restore frontend dependencies:" -ForegroundColor Gray
Write-Host "   cd frontend && npm install" -ForegroundColor Gray
