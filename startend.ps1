function Get-TStart {
    $utcNow = [DateTime]::UtcNow
    $utcStart = $utcNow.AddMinutes(-15)
    return ($utcStart.ToString("yyyy-MM-ddTHH:mm:ss"))+"Z"
}

function Get-TEnd {
  $utcNow = [DateTime]::UtcNow
  return ($utcNow.ToString("yyyy-MM-ddTHH:mm:ss"))+"Z"
}

# # Example usage
# $currentUtcDateTime = Get-CurrentUtcDateTime
# Write-Output $currentUtcDateTime
