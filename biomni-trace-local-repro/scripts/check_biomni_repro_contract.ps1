param(
  [Parameter(Mandatory = $true)]
  [string]$Path
)

$ErrorActionPreference = "Stop"

$resolved = Resolve-Path -LiteralPath $Path
$files = Get-ChildItem -LiteralPath $resolved.Path -Recurse -File |
  Where-Object { $_.Extension -in @(".R", ".r", ".py", ".Rmd", ".qmd", ".md") }

$forbiddenPathPattern = "share_c0aca|share_[0-9A-Za-z]+|\.tmp_|WORKSPACE_DIR|F2_TRACE|F2_BIOMNI|/mnt/|/workspace/"
$errorPathPattern = "DEPRECATED|deprecated|旧公式|near-root|old_tier|old_trajectory|USE_OLD_FORMULA|RUN_DEPRECATED|READ_DEPRECATED|pct_rank_audit"

$issues = New-Object System.Collections.Generic.List[object]

foreach ($file in $files) {
  $lineNumber = 0
  foreach ($line in Get-Content -LiteralPath $file.FullName -Encoding UTF8) {
    $lineNumber += 1
    $trimmed = $line.TrimStart()

    if ($line -match $forbiddenPathPattern) {
      $issues.Add([pscustomobject]@{
        Type = "ForbiddenTraceRuntimePath"
        File = $file.FullName
        Line = $lineNumber
        Text = $line
      })
    }

    if ($line -match $errorPathPattern -and -not $trimmed.StartsWith("#")) {
      $issues.Add([pscustomobject]@{
        Type = "ExecutableDeprecatedOrErrorPath"
        File = $file.FullName
        Line = $lineNumber
        Text = $line
      })
    }
  }
}

if ($issues.Count -gt 0) {
  $issues | Format-Table -AutoSize
  throw "Biomni reproduction contract check failed with $($issues.Count) issue(s)."
}

Write-Output "Biomni reproduction contract check passed for: $($resolved.Path)"

