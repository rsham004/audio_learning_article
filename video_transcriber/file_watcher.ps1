# File watcher script for automatic transcription
# This script monitors the InputVideos folder for new MP4 files and automatically processes them

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InputPath = Join-Path $ScriptDir "InputVideos"

Write-Host "Audio Learning Article - File Watcher" -ForegroundColor Green
Write-Host "Monitoring folder: $InputPath" -ForegroundColor Yellow
Write-Host "Watching for: *.mp4 files" -ForegroundColor Yellow
Write-Host ""

# Create file system watcher
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $InputPath
$watcher.Filter = "*.mp4"
$watcher.EnableRaisingEvents = $true
$watcher.IncludeSubdirectories = $false

# Define the action to take when a file is created
$action = {
    $path = $Event.SourceEventArgs.FullPath
    $name = $Event.SourceEventArgs.Name
    $changeType = $Event.SourceEventArgs.ChangeType
    
    if ($changeType -eq "Created") {
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - New video file detected: $name" -ForegroundColor Cyan
        
        # Wait for file to be fully copied (important for large files)
        Write-Host "Waiting for file to be fully copied..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # Verify file is not locked (still being copied)
        $maxRetries = 10
        $retryCount = 0
        $fileReady = $false
        
        while (-not $fileReady -and $retryCount -lt $maxRetries) {
            try {
                $fileStream = [System.IO.File]::Open($path, 'Open', 'Read', 'None')
                $fileStream.Close()
                $fileReady = $true
                Write-Host "File is ready for processing." -ForegroundColor Green
            }
            catch {
                $retryCount++
                Write-Host "File still being copied, waiting... (attempt $retryCount/$maxRetries)" -ForegroundColor Yellow
                Start-Sleep -Seconds 3
            }
        }
        
        if ($fileReady) {
            # Run the transcriber
            Write-Host "Starting transcription process..." -ForegroundColor Green
            Set-Location $ScriptDir
            
            try {
                & ".\run_transcriber.bat"
                Write-Host "Transcription completed successfully!" -ForegroundColor Green
            }
            catch {
                Write-Host "Error during transcription: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        else {
            Write-Host "File could not be accessed after $maxRetries attempts. Skipping." -ForegroundColor Red
        }
        
        Write-Host "Ready for next file..." -ForegroundColor White
        Write-Host ""
    }
}

# Register the event handler
Register-ObjectEvent -InputObject $watcher -EventName "Created" -Action $action

Write-Host "File watcher started successfully!" -ForegroundColor Green
Write-Host "Drop MP4 files into the InputVideos folder to automatically process them." -ForegroundColor White
Write-Host "Press Ctrl+C to stop monitoring." -ForegroundColor Yellow
Write-Host ""

# Keep the script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
catch [System.Management.Automation.PipelineStoppedException] {
    Write-Host ""
    Write-Host "File watcher stopped by user." -ForegroundColor Yellow
}
finally {
    # Clean up
    $watcher.Dispose()
    Write-Host "File watcher disposed. Goodbye!" -ForegroundColor Green
}
