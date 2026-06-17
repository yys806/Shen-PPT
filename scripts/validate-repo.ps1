param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

function Assert-Path {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$Message
  )
  if (-not (Test-Path -LiteralPath $Path)) {
    throw $Message
  }
}

function Assert-Count {
  param(
    [Parameter(Mandatory = $true)][int]$Actual,
    [Parameter(Mandatory = $true)][int]$Expected,
    [Parameter(Mandatory = $true)][string]$Message
  )
  if ($Actual -ne $Expected) {
    throw "$Message Actual=$Actual Expected=$Expected"
  }
}

$rootItem = Get-Item -LiteralPath $Root
$references = Join-Path $rootItem.FullName 'references'
$sampleRoot = Join-Path $references 'style-samples-v2-20260606'
$sampleDecks = Join-Path $sampleRoot 'sample-decks'
$highest = Join-Path $references 'highest-references\orangepi-defense-final-v9-20260607'

Assert-Path (Join-Path $rootItem.FullName 'SKILL.md') 'Missing SKILL.md'
Assert-Path (Join-Path $rootItem.FullName 'README.md') 'Missing README.md'
Assert-Path $references 'Missing references directory'
Assert-Path (Join-Path $references 'parameter-spec.md') 'Missing references/parameter-spec.md'
Assert-Path $sampleDecks 'Missing style sample deck directory'
Assert-Path (Join-Path $sampleDecks 'style-samples-v2-general-overview.png') 'Missing general overview image'
Assert-Path (Join-Path $sampleDecks 'style-samples-v2-tongji-overview.png') 'Missing Tongji overview image'
Assert-Path (Join-Path $sampleRoot 'sample-deck-map.json') 'Missing sample-deck-map.json'
Assert-Path (Join-Path $sampleRoot 'style-manifest.json') 'Missing style-manifest.json'
Assert-Path $highest 'Missing highest reference directory'
Assert-Path (Join-Path $highest 'reference.pptx') 'Missing highest reference PPTX'
Assert-Path (Join-Path $highest 'contact-sheet.png') 'Missing highest reference contact sheet'
Assert-Path (Join-Path $highest 'accepted-standard.md') 'Missing highest reference accepted-standard.md'

$topLevelReferenceFiles = Get-ChildItem -LiteralPath $rootItem.FullName -File |
  Where-Object { $_.Extension -in @('.pptx', '.png') -or $_.Name -eq 'parameter-spec.md' }
if ($topLevelReferenceFiles.Count -gt 0) {
  $names = ($topLevelReferenceFiles | Select-Object -ExpandProperty Name) -join ', '
  throw "Reference files must live under references/, not repository root: $names"
}

$samplePptx = Get-ChildItem -LiteralPath $sampleDecks -File -Filter '*.pptx'
Assert-Count $samplePptx.Count 15 'Wrong number of editable sample PPTX decks.'

$map = Get-Content -LiteralPath (Join-Path $sampleRoot 'sample-deck-map.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$expectedSlugs = @(
  'academic-minimal',
  'business-roadshow',
  'chinese-academic',
  'dark-engineering',
  'data-analytics',
  'education-clean',
  'research-blue',
  'tech-launch',
  'tongji-blue-clean',
  'tongji-green-academic',
  'tongji-green-vitality',
  'tongji-guangying',
  'tongji-guangying-jiyi',
  'tongji-sakura',
  'tongji-study-space'
)

$resolved = @()
foreach ($slug in $expectedSlugs) {
  $group = if ($slug.StartsWith('tongji-')) { 'tongji' } else { 'general' }
  $path = $map.$group.$slug
  if (-not $path) {
    throw "Missing sample deck map entry for slug: $slug"
  }
  $full = Join-Path $rootItem.FullName $path
  Assert-Path $full "Mapped sample deck does not exist for slug: $slug"
  $resolved += $full
}

Assert-Count (($resolved | Sort-Object -Unique).Count) 15 'Sample deck map should resolve to 15 unique PPTX files.'

Write-Host 'Shen-PPT repository validation passed.'
