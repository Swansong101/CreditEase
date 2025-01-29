# Remove node_modules
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force "node_modules"
    Write-Host "Deleted node_modules folder."
} else {
    Write-Host "node_modules folder does not exist."
}

# Remove dist folder
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "Deleted dist folder."
} else {
    Write-Host "dist folder does not exist."
}

# Remove .cache folder
if (Test-Path ".cache") {
    Remove-Item -Recurse -Force ".cache"
    Write-Host "Deleted .cache folder."
} else {
    Write-Host ".cache folder does not exist."
}

# Clear npm cache
Write-Host "Clearing npm cache..."
npm cache clean --force

# Reinstall dependencies
Write-Host "Reinstalling dependencies..."
npm install

# Rebuild the project
Write-Host "Rebuilding the project..."
npm run build

# Serve the project
Write-Host "Starting the server..."
npm run serve
