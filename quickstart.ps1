# Vector Explorer - Quick Start Script
# This script helps set up the extension for first-time use

Write-Host "🔍 Vector Explorer - Quick Start Setup" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check Node.js
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install from https://www.python.org/" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Install Node dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install Node.js dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Node.js dependencies installed" -ForegroundColor Green
Write-Host ""

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r python/requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install Python dependencies" -ForegroundColor Red
    Write-Host "  Try manually: pip install faiss-cpu chromadb numpy" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Python dependencies installed" -ForegroundColor Green
Write-Host ""

# Compile extension
Write-Host "Compiling extension..." -ForegroundColor Yellow
npm run compile
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to compile extension" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Extension compiled successfully" -ForegroundColor Green
Write-Host ""

# Create sample data
Write-Host "Creating sample data..." -ForegroundColor Yellow
Write-Host "  Generating sample FAISS database..." -ForegroundColor Cyan
python examples/create_sample_faiss.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠ Failed to create FAISS sample (faiss-cpu may not be installed)" -ForegroundColor Yellow
}

Write-Host "  Generating sample Chroma database..." -ForegroundColor Cyan
python examples/create_sample_chroma.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠ Failed to create Chroma sample (chromadb may not be installed)" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Press F5 in VS Code to launch the extension" -ForegroundColor White
Write-Host "2. In the new window, press Ctrl+Shift+P" -ForegroundColor White
Write-Host "3. Type: Vector Explorer: Open Vector Database" -ForegroundColor White
Write-Host "4. Select: examples/sample_faiss/index.faiss" -ForegroundColor White
Write-Host ""
Write-Host "📚 For more information, see:" -ForegroundColor Yellow
Write-Host "   - README.md - Overview and features" -ForegroundColor White
Write-Host "   - SETUP.md - Detailed setup guide" -ForegroundColor White
Write-Host ""
Write-Host "Happy exploring! 🚀" -ForegroundColor Cyan
