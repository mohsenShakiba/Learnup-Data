param(
    [int]$Start = 19,
    [int]$End = 64,
    [int]$MaxRuns = 46,
    [int]$DelaySeconds = 60,
    [string]$AuditLog = "conversation_audit_plan.csv",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$promptPath = Join-Path $repo "scripts\conversation_audit_prompt.md"
$auditPath = Join-Path $repo $AuditLog

if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw "codex CLI was not found on PATH."
}

if (-not (Test-Path $promptPath)) {
    throw "Missing prompt file: $promptPath"
}

if (-not (Test-Path $auditPath)) {
    New-Item -ItemType File -Path $auditPath | Out-Null
}

Push-Location $repo
try {
    for ($i = 1; $i -le $MaxRuns; $i++) {
        $logged = Get-Content $auditPath |
            Where-Object { $_ -match "^\d+," } |
            ForEach-Object { [int](($_ -split ",")[0]) }

        $next = $null
        foreach ($n in $Start..$End) {
            if ($logged -notcontains $n) {
                $next = $n
                break
            }
        }

        if ($null -eq $next) {
            Write-Host "Audit loop complete: $Start-$End are logged in $AuditLog."
            break
        }

        $today = Get-Date -Format "yyyy-MM-dd"

        Write-Host "Run ${i}/${MaxRuns}: auditing conversation $next..."

        $prompt = @"
Use conversation_revision.md and agent.md.

Important: this is an audit loop because plan.csv may already contain bulk-added entries.
Use $AuditLog, not plan.csv, to decide audit progress.

Process exactly one conversation: a1/$next*.json.
Do a real native-speaker revision pass for that one file only.
If wording changes, update Persian translations, focus words, Level, estimatedDuration, and append added/removed word logs.
If the conversation already passes, leave the JSON unchanged.
Append "$next,$today" to $AuditLog when the audit for this one conversation is complete.
Do not edit any other conversation.
Stop after this one conversation.
"@

        if ($DryRun) {
            Write-Host "Dry run prompt:"
            Write-Host $prompt
            break
        }

        $prompt | codex exec --sandbox workspace-write -

        if ($LASTEXITCODE -ne 0) {
            throw "codex exec failed while auditing conversation $next."
        }

        if ($DelaySeconds -gt 0 -and $i -lt $MaxRuns) {
            Write-Host "Waiting $DelaySeconds seconds before the next conversation..."
            Start-Sleep -Seconds $DelaySeconds
        }
    }
}
finally {
    Pop-Location
}
