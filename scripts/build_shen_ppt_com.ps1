param(
  [Parameter(Mandatory = $true)][string]$Cards,
  [Parameter(Mandatory = $true)][string]$OutPptx,
  [string]$SkillRoot = '',
  [string]$PreviewDir = '',
  [string]$LatexPptRoot = 'D:\shen\test\latex-ppt'
)

$ErrorActionPreference = 'Stop'

if (-not $SkillRoot) {
  $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
  $SkillRoot = (Resolve-Path (Join-Path $scriptDir '..')).Path
}

try { Add-Type -AssemblyName System.Drawing } catch {}

$ppLayoutBlank = 12
$msoFalse = 0
$msoTrue = -1
$msoShapeRectangle = 1
$msoShapeRoundedRectangle = 5
$msoShapeLine = 9
$msoShapeRightArrow = 33
$msoShapeDownArrow = 36
$ppEffectNone = 0
$LatexAddinPath = Join-Path $LatexPptRoot 'latex.ppam'
$LatexModeEnabled = $false
$EquationFallbacks = New-Object System.Collections.Generic.List[string]

function ToPt([double]$px) { return $px * 0.75 }
function HexToRgb([string]$hex) {
  $h = $hex.TrimStart('#')
  return [int]("0x$($h.Substring(0,2))") + ([int]("0x$($h.Substring(2,2))") * 256) + ([int]("0x$($h.Substring(4,2))") * 65536)
}

$C = @{
  Base = HexToRgb '#07100F'
  Base2 = HexToRgb '#0A1513'
  Panel = HexToRgb '#0E1E1A'
  PanelDark = HexToRgb '#0C1D19'
  Panel2 = HexToRgb '#132A24'
  Line = HexToRgb '#24443B'
  Text = HexToRgb '#EAF4EF'
  Muted = HexToRgb '#A4B7B0'
  Amber = HexToRgb '#F2B84B'
  Blue = HexToRgb '#58C4D8'
  Dark = HexToRgb '#07100F'
}

$FontTitle = 'Microsoft YaHei'
$FontBody = [string]::Concat([char]0x65B9, [char]0x6B63, [char]0x5C0F, [char]0x6807, [char]0x5B8B, [char]0x7B80, [char]0x4F53)
$FontNumber = 'Times New Roman'

function Set-TextBox($shape, [string]$text, [int]$fontSize, [int]$color, [string]$fontName, [bool]$bold = $false, [string]$align = 'left') {
  $shape.TextFrame2.TextRange.Text = $text
  $shape.TextFrame2.TextRange.Font.Size = $fontSize
  $shape.TextFrame2.TextRange.Font.Name = $fontName
  try { $shape.TextFrame2.TextRange.Font.NameFarEast = $fontName } catch {}
  try { $shape.TextFrame.TextRange.Font.Name = $fontName } catch {}
  try { $shape.TextFrame.TextRange.Font.NameFarEast = $fontName } catch {}
  try { $shape.TextFrame.TextRange.Font.Color.RGB = $color } catch {}
  $shape.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $color
  $shape.TextFrame2.TextRange.Font.Bold = if ($bold) { $msoTrue } else { $msoFalse }
  $shape.TextFrame2.MarginLeft = 0
  $shape.TextFrame2.MarginRight = 0
  $shape.TextFrame2.MarginTop = 0
  $shape.TextFrame2.MarginBottom = 0
  $shape.TextFrame2.WordWrap = $msoTrue
  switch ($align) {
    'center' { $shape.TextFrame2.TextRange.ParagraphFormat.Alignment = 2 }
    'right' { $shape.TextFrame2.TextRange.ParagraphFormat.Alignment = 3 }
    default { $shape.TextFrame2.TextRange.ParagraphFormat.Alignment = 1 }
  }
  try { $shape.ZOrder(0) } catch {}
}

function Add-Text($slide, [double]$x, [double]$y, [double]$w, [double]$h, [string]$text, [int]$fontSize, [int]$color, [string]$fontName, [bool]$bold = $false, [string]$align = 'left') {
  $shape = $slide.Shapes.AddTextbox(1, (ToPt $x), (ToPt $y), (ToPt $w), (ToPt $h))
  Set-TextBox $shape $text $fontSize $color $fontName $bold $align
  return $shape
}

function Add-Panel($slide, [double]$x, [double]$y, [double]$w, [double]$h, [int]$fill, [int]$lineColor = $C.Line, [double]$lineWeight = 1.0) {
  $shape = $slide.Shapes.AddShape($msoShapeRoundedRectangle, (ToPt $x), (ToPt $y), (ToPt $w), (ToPt $h))
  $shape.Fill.ForeColor.RGB = $fill
  $shape.Line.ForeColor.RGB = $lineColor
  $shape.Line.Weight = $lineWeight
  return $shape
}

function Add-Line($slide, [double]$x1, [double]$y1, [double]$x2, [double]$y2, [int]$color = $C.Line, [double]$weight = 1.2) {
  $shape = $slide.Shapes.AddLine((ToPt $x1), (ToPt $y1), (ToPt $x2), (ToPt $y2))
  $shape.Line.ForeColor.RGB = $color
  $shape.Line.Weight = $weight
  return $shape
}

function Add-Icon($slide, [string]$icon, [double]$x, [double]$y, [double]$size) {
  $iconPath = Join-Path $SkillRoot "references\icons\apple-svg\generated\$icon.svg"
  if (-not (Test-Path -LiteralPath $iconPath)) { return $null }
  return $slide.Shapes.AddPicture($iconPath, $msoFalse, $msoTrue, (ToPt $x), (ToPt $y), (ToPt $size), (ToPt $size))
}

function Add-PictureContained($slide, [string]$path, [double]$x, [double]$y, [double]$w, [double]$h) {
  if (-not $path -or $path -eq 'none' -or -not (Test-Path -LiteralPath $path)) { return $null }
  Add-Panel $slide $x $y $w $h $C.PanelDark $C.Line 1 | Out-Null
  $img = [System.Drawing.Image]::FromFile($path)
  try {
    $scale = [Math]::Min(($w - 16) / $img.Width, ($h - 16) / $img.Height)
    $pw = $img.Width * $scale
    $ph = $img.Height * $scale
  } finally {
    $img.Dispose()
  }
  $px = $x + ($w - $pw) / 2
  $py = $y + ($h - $ph) / 2
  return $slide.Shapes.AddPicture($path, $msoFalse, $msoTrue, (ToPt $px), (ToPt $py), (ToPt $pw), (ToPt $ph))
}

function Add-FigureBlock($slide, [string]$path, [string]$caption, [double]$x, [double]$y, [double]$w, [double]$h) {
  if ($path -and $path -ne 'none' -and -not $caption) {
    $caption = [System.IO.Path]::GetFileNameWithoutExtension($path).Replace('_', ' ').Replace('-', ' ')
  }
  $capH = if ($caption) { 34 } else { 0 }
  Add-PictureContained $slide $path $x $y $w ($h - $capH) | Out-Null
  if ($caption) {
    Add-Text $slide ($x + 8) ($y + $h - $capH + 6) ($w - 16) 24 $caption 11 $C.Muted $FontNumber $false 'center' | Out-Null
  }
}

function Clean-LatexDisplay([string]$latex) {
  if (-not $latex) { return '' }
  $value = $latex
  $value = $value.Replace('\mathbb{E}', 'E')
  $value = $value.Replace('\Theta', [string][char]0x0398)
  $value = $value.Replace('\zeta', [string][char]0x03B6)
  $value = $value.Replace('\gamma', [string][char]0x03B3)
  $value = $value.Replace('\beta', [string][char]0x03B2)
  $value = $value.Replace('\Delta', [string][char]0x0394)
  $value = $value.Replace('\sum', [string][char]0x03A3)
  $value = $value.Replace('\max', 'max')
  $value = $value.Replace('\sim', '~')
  $value = $value.Replace('\in', [string][char]0x2208)
  $value = $value.Replace('\tilde', '')
  $value = $value.Replace('\left', '')
  $value = $value.Replace('\right', '')
  $value = $value.Replace('P_0', 'P0')
  $value = [regex]::Replace($value, '_\{([^{}]+)\}', '_$1')
  $value = [regex]::Replace($value, '\^\{([^{}]+)\}', '^$1')
  $value = $value.Replace('{', '').Replace('}', '').Replace('\', '')
  $value = [regex]::Replace($value, '\s+', ' ')
  return $value.Trim()
}

function Enable-LatexMode($slide) {
  if ($script:LatexModeEnabled) { return $true }
  if (-not (Test-Path -LiteralPath $LatexAddinPath)) { return $false }
  $probe = $null
  try {
    $slide.Select()
    $probe = $slide.Shapes.AddTextbox(1, (ToPt 4), (ToPt 4), (ToPt 8), (ToPt 8))
    $probe.TextFrame.TextRange.Text = ' '
    $probe.TextFrame.TextRange.Select()
    try {
      $ppt.Run('SwitchLatex') | Out-Null
    } catch {
      try { $ppt.Run('latex.ppam!SwitchLatex') | Out-Null } catch {}
    }
    $script:LatexModeEnabled = $true
    return $true
  } catch {
    return $false
  } finally {
    if ($probe -ne $null) { try { $probe.Delete() } catch {} }
  }
}

function Add-LatexEquation($slide, [string]$latex, [string]$display, [double]$x, [double]$y, [double]$w, [double]$h) {
  if (-not $latex) { return $null }
  try {
    $slide.Select()
    Enable-LatexMode $slide | Out-Null
    $seed = Add-Text $slide $x $y $w $h '' 16 $C.Text 'Cambria Math'
    $seed.TextFrame.TextRange.Text = ' '
    $seed.Select()
    $seed.TextFrame.TextRange.Select()
    $ppt.CommandBars.ExecuteMso('EquationInsertNew')
    $range = $ppt.ActiveWindow.Selection.ShapeRange.TextFrame.TextRange
    $insertAt = [Math]::Max(1, [int]$range.Length - 1)
    $range.Characters($insertAt).Text = $latex
    $ppt.CommandBars.ExecuteMso('EquationProfessional')
    $eq = $ppt.ActiveWindow.Selection.ShapeRange.Item(1)
    $eq.Left = ToPt $x
    $eq.Top = ToPt $y
    $eq.Width = ToPt $w
    $eq.Height = ToPt $h
    try { $eq.TextFrame2.TextRange.Font.Size = 13 } catch {}
    try { $eq.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $C.Text } catch {}
    try { $eq.TextFrame.TextRange.Font.Name = 'Cambria Math' } catch {}
    try { $eq.Tags.Add('ShenPPT_LatexSource', $latex) | Out-Null } catch {}
    return $eq
  } catch {
    $fallback = if ($display) { $display } else { Clean-LatexDisplay $latex }
    $script:EquationFallbacks.Add(("{0} :: {1}" -f $latex, $_.Exception.Message)) | Out-Null
    return Add-Text $slide $x $y $w $h $fallback 13 $C.Text $FontNumber
  }
}

function Add-LatexRows($slide, $items, [double]$x, [double]$y, [double]$w, [double]$h, [int]$maxItems = 2) {
  if (-not $items -or $items.Count -le 0) { return }
  $count = [Math]::Min($maxItems, [int]$items.Count)
  Add-Panel $slide $x $y $w $h $C.PanelDark $C.Line 1 | Out-Null
  $rowH = $h / $count
  for ($i = 0; $i -lt $count; $i++) {
    $item = $items[$i]
    $yy = $y + $i * $rowH
    Add-Text $slide ($x + 20) ($yy + 8) 120 ($rowH - 14) ([string]$item.label) 12 $C.Amber $FontBody | Out-Null
    Add-LatexEquation $slide ([string]$item.source) ([string]$item.display) ($x + 146) ($yy + 7) ($w - 178) ($rowH - 12) | Out-Null
  }
}

function Add-Background($slide) {
  $bg = $slide.Shapes.AddShape($msoShapeRectangle, 0, 0, (ToPt 1280), (ToPt 720))
  $bg.Fill.ForeColor.RGB = $C.Base
  $bg.Line.Visible = $msoFalse
  $bg.ZOrder(1)
  for ($x = 40; $x -lt 1280; $x += 80) { Add-Line $slide $x 0 $x 720 (HexToRgb '#0D1A17') 0.4 | Out-Null }
  for ($y = 40; $y -lt 720; $y += 80) { Add-Line $slide 0 $y 1280 $y (HexToRgb '#0D1A17') 0.4 | Out-Null }
  $top = $slide.Shapes.AddShape($msoShapeRectangle, 0, 0, (ToPt 1280), (ToPt 4))
  $top.Fill.ForeColor.RGB = $C.Amber
  $top.Line.Visible = $msoFalse
}

function Clear-Animations($slide) {
  try { $slide.SlideShowTransition.EntryEffect = $ppEffectNone } catch {}
  try { $slide.SlideShowTransition.AdvanceOnTime = $msoFalse } catch {}
  try { $slide.SlideShowTransition.AdvanceOnClick = $msoTrue } catch {}
  try {
    while ($slide.TimeLine.MainSequence.Count -gt 0) {
      $slide.TimeLine.MainSequence.Item(1).Delete()
    }
  } catch {}
}

function Add-Nav($slide, [string]$activeSection, $sections) {
  $startX = 590
  $y = 24
  $w = 98
  $h = 52
  $gap = 8
  $idx = 0
  foreach ($section in $sections) {
    $x = $startX + $idx * ($w + $gap)
    $active = $section[0] -eq $activeSection
    $fill = if ($active) { $C.Amber } else { $C.Panel }
    $text = if ($active) { $C.Dark } else { $C.Muted }
    Add-Panel $slide $x $y $w $h $fill $C.Line 1 | Out-Null
    Add-Text $slide $x 30 $w 18 $section[0] 16 $text $FontNumber $false 'center' | Out-Null
    Add-Text $slide $x 51 $w 16 $section[1].Substring(0, [Math]::Min(4, $section[1].Length)) 12 $text $FontBody $false 'center' | Out-Null
    $idx += 1
  }
}

function Add-Chrome($slide, $card, $sections) {
  Add-Text $slide 54 22 520 38 $card.sectionTitle 30 $C.Text $FontTitle $true | Out-Null
  Add-Text $slide 56 69 760 28 $card.subtitle 21 $C.Muted $FontBody | Out-Null
  Add-Nav $slide $card.section $sections
  Add-Line $slide 54 100 1226 100 $C.Line 1.4 | Out-Null
  Add-Line $slide 54 670 1226 670 $C.Line 1.4 | Out-Null
  Add-Text $slide 54 684 720 18 'DRIFT论文中文讲解' 10 $C.Muted $FontNumber | Out-Null
  Add-Text $slide 1182 676 44 24 ([string]$card.slideNo).PadLeft(2,'0') 14 $C.Amber $FontNumber $false 'right' | Out-Null
}

function Add-Bullets($slide, [double]$x, [double]$y, [double]$w, [double]$rowH, $items, [int]$fontSize = 18) {
  $i = 0
  foreach ($item in $items) {
    $yy = $y + $i * $rowH
    Add-Text $slide $x $yy 42 28 ([string]($i + 1)).PadLeft(2,'0') 22 $C.Blue $FontNumber $true | Out-Null
    Add-Text $slide ($x + 54) ($yy - 2) ($w - 54) ($rowH - 10) $item $fontSize $C.Text $FontBody | Out-Null
    $i += 1
  }
}

function Add-CompactBullets($slide, [double]$x, [double]$y, [double]$w, [double]$rowH, $items, [int]$fontSize = 15, [int]$maxItems = 4) {
  $i = 0
  foreach ($item in $items) {
    if ($i -ge $maxItems) { break }
    $yy = $y + $i * $rowH
    Add-Text $slide $x $yy 42 24 ([string]($i + 1)).PadLeft(2,'0') 20 $C.Blue $FontNumber $true | Out-Null
    Add-Text $slide ($x + 52) ($yy - 2) ($w - 52) ($rowH - 4) $item $fontSize $C.Text $FontBody | Out-Null
    $i += 1
  }
}

function Add-Table($slide, [double]$x, [double]$y, [double]$w, [double]$h, $table) {
  $rows = @($table.rows)
  $cols = @($table.headers)
  $rowCount = $rows.Count + 1
  $colCount = $cols.Count
  if ($rowCount -lt 2 -or $colCount -lt 2) { return }

  Add-Panel $slide $x $y $w $h (HexToRgb '#EEF3EF') (HexToRgb '#A9B9B0') 1 | Out-Null
  $cellW = $w / $colCount
  $headerH = 36
  $rowH = ($h - $headerH) / [Math]::Max(1, $rows.Count)
  for ($c = 0; $c -lt $colCount; $c++) {
    $cx = $x + $c * $cellW
    Add-Text $slide ($cx + 10) ($y + 8) ($cellW - 20) 20 $cols[$c] 13 $C.Amber $FontBody $true 'center' | Out-Null
    if ($c -lt $colCount - 1) {
      Add-Line $slide ($cx + $cellW) $y ($cx + $cellW) ($y + $h) $C.Line 0.8 | Out-Null
    }
  }
  Add-Line $slide $x ($y + $headerH) ($x + $w) ($y + $headerH) $C.Line 0.8 | Out-Null
  for ($r = 0; $r -lt $rows.Count; $r++) {
    $ry = $y + $headerH + $r * $rowH
    if ($r -lt $rows.Count - 1) {
      Add-Line $slide $x ($ry + $rowH) ($x + $w) ($ry + $rowH) $C.Line 0.5 | Out-Null
    }
    for ($c = 0; $c -lt $colCount; $c++) {
      $cx = $x + $c * $cellW
      Add-Text $slide ($cx + 8) ($ry + 6) ($cellW - 16) ($rowH - 8) ([string]$rows[$r][$c]) 12 $C.Dark $FontBody $true 'center' | Out-Null
    }
  }
  if ($table.title) {
    Add-Text $slide ($x + 8) ($y - 28) ($w - 16) 20 $table.title 14 $C.Muted $FontBody $false 'left' | Out-Null
  }
}

function Add-Cover($slide, $card) {
  Add-Background $slide
  $bar = $slide.Shapes.AddShape($msoShapeRectangle, (ToPt 54), (ToPt 86), (ToPt 84), (ToPt 6))
  $bar.Fill.ForeColor.RGB = $C.Amber
  $bar.Line.Visible = $msoFalse
  Add-Text $slide 54 116 460 30 '论文中文讲解' 22 $C.Amber $FontBody | Out-Null
  Add-Text $slide 54 160 560 70 'DRIFT' 64 $C.Text $FontTitle $true | Out-Null
  Add-Text $slide 54 242 560 112 '风险约束扩散模型' 44 $C.Text $FontTitle $true | Out-Null
  Add-Text $slide 54 322 520 72 '与模仿先验' 44 $C.Text $FontTitle $true | Out-Null
  Add-Text $slide 58 430 560 72 'Risk-Constrained Diffusion with Imitation Priors for Mixed Autonomy Traffic Generation' 21 $C.Muted $FontNumber | Out-Null
  if ([string]$card.visualAsset -and [string]$card.visualAsset -ne 'none') {
    Add-FigureBlock $slide ([string]$card.visualAsset) ([string]$card.caption) 700 92 470 420
  } else {
    Add-Panel $slide 720 110 420 420 $C.PanelDark $C.Line 1.2 | Out-Null
    Add-Icon $slide 'route' 790 174 76 | Out-Null
    Add-Icon $slide 'shield' 930 174 76 | Out-Null
    Add-Icon $slide 'algorithm' 860 310 76 | Out-Null
    Add-Text $slide 760 468 340 70 '扩散生成 · 风险约束`n混合自治交通' 25 $C.Text $FontBody $false 'center' | Out-Null
  }
}

function Add-Directory($slide, $card, $sections) {
  Add-Background $slide
  Add-Text $slide 58 44 220 78 '目录' 66 $C.Text $FontTitle $true | Out-Null
  Add-Text $slide 64 136 130 18 'CONTENTS' 11 $C.Amber $FontNumber | Out-Null
  Add-Line $slide 284 64 284 660 $C.Line 1.6 | Out-Null
  $y = 112
  foreach ($section in $sections) {
    Add-Text $slide 330 $y 88 44 $section[0] 34 $C.Blue $FontNumber $true | Out-Null
    Add-Text $slide 430 ($y - 2) 320 42 $section[1] 30 $C.Text $FontTitle $true | Out-Null
    Add-Text $slide 430 ($y + 42) 620 28 $section[2] 18 $C.Muted $FontBody | Out-Null
    $y += 102
  }
}

function Add-Section($slide, $card, $sections) {
  Add-Background $slide
  Add-Nav $slide $card.section $sections
  Add-Text $slide 58 76 132 100 $card.section 82 $C.Amber $FontNumber $true | Out-Null
  Add-Icon $slide $card.icon 208 96 56 | Out-Null
  Add-Text $slide 278 76 720 100 $card.sectionTitle 64 $C.Text $FontTitle $true | Out-Null
  Add-Text $slide 64 188 1060 42 $card.subtitle 28 $C.Text $FontTitle $true | Out-Null
  Add-Line $slide 62 248 1182 248 $C.Line 1.6 | Out-Null
  Add-Bullets $slide 100 300 1040 86 $card.body 24
}

function Add-Body($slide, $card, $sections) {
  Add-Background $slide
  Add-Chrome $slide $card $sections
  $layout = [string]$card.layoutFamily
  if ($layout -eq 'process flow') {
    $count = [Math]::Max(1, [int]$card.body.Count)
    $x = 84; $y = 124; $w = 1060
    $h = if ($count -ge 5) { 66 } else { 82 }
    $gap = if ($count -ge 5) { 16 } else { 24 }
    $i = 0
    foreach ($item in $card.body) {
      $yy = $y + $i * ($h + $gap)
      Add-Panel $slide $x $yy $w $h $C.PanelDark $C.Line 1.2 | Out-Null
      Add-Icon $slide $card.icon ($x + 24) ($yy + (($h - 24) / 2)) 24 | Out-Null
      Add-Text $slide ($x + 68) ($yy + (($h - 30) / 2)) 178 30 ("步骤 " + ($i + 1)) 20 $C.Text $FontBody | Out-Null
      Add-Text $slide ($x + 260) ($yy + (($h - 38) / 2)) 800 38 $item 16 $C.Muted $FontBody | Out-Null
      if ($i -lt $card.body.Count - 1) {
        $arrow = $slide.Shapes.AddShape($msoShapeDownArrow, (ToPt 604), (ToPt ($yy + $h + 2)), (ToPt 36), (ToPt ($gap - 4)))
        $arrow.Fill.ForeColor.RGB = $C.Amber; $arrow.Line.Visible = $msoFalse
      }
      $i += 1
    }
    if ($card.latex.Count -gt 0) {
      Add-LatexRows $slide $card.latex 84 560 1060 80 2
    }
  } elseif ($layout -eq 'architecture map') {
    $labels = @('输入条件','扩散生成','风险约束','模仿先验','输出场景')
    $icons = @('database','route','shield','algorithm','chart')
    for ($i=0; $i -lt $labels.Count; $i++) {
      $x = 78 + $i * 228
      Add-Panel $slide $x 210 172 160 $C.PanelDark $C.Line 1.2 | Out-Null
      Add-Icon $slide $icons[$i] ($x + 60) 238 48 | Out-Null
      Add-Text $slide ($x + 12) 305 148 34 $labels[$i] 22 $C.Text $FontBody $false 'center' | Out-Null
      if ($i -lt $labels.Count - 1) {
        $arr = $slide.Shapes.AddShape($msoShapeRightArrow, (ToPt ($x + 178)), (ToPt 268), (ToPt 46), (ToPt 28))
        $arr.Fill.ForeColor.RGB = $C.Amber; $arr.Line.Visible = $msoFalse
      }
    }
    $panelY = 398
    $panelH = if ($card.latex.Count -gt 0) { 96 } else { 172 }
    Add-Panel $slide 92 $panelY 1096 $panelH $C.Panel $C.Line 1 | Out-Null
    $i = 0
    foreach ($item in $card.body) {
      if (($card.latex.Count -gt 0) -and ($i -ge 4)) { break }
      $col = $i % 2
      $row = [Math]::Floor($i / 2)
      $xx = 126 + $col * 520
      $yy = ($panelY + 20) + $row * 34
      Add-Text $slide $xx $yy 44 24 ([string]($i + 1)).PadLeft(2,'0') 20 $C.Blue $FontNumber $true | Out-Null
      Add-Text $slide ($xx + 54) ($yy - 2) 430 30 $item 14 $C.Text $FontBody | Out-Null
      $i += 1
    }
    if ($card.latex.Count -gt 0) {
      Add-LatexRows $slide $card.latex 92 510 1096 106 2
    }
  } elseif ($layout -eq 'results dominant') {
    Add-FigureBlock $slide ([string]$card.visualAsset) ([string]$card.caption) 84 128 660 292
    Add-Panel $slide 780 128 398 456 $C.Panel $C.Line 1 | Out-Null
    Add-Text $slide 810 156 330 38 '读图重点' 26 $C.Text $FontTitle $true | Out-Null
    Add-CompactBullets $slide 810 210 316 50 $card.body 12 5
    if ($card.latex.Count -gt 0) {
      Add-LatexRows $slide $card.latex 804 470 330 92 2
    }
    if ($card.tables.Count -gt 0) {
      Add-Table $slide 84 444 660 140 $card.tables[0]
    }
  } else {
    if ([string]$card.visualAsset -and [string]$card.visualAsset -ne 'none') {
      Add-FigureBlock $slide ([string]$card.visualAsset) ([string]$card.caption) 70 128 560 456
      Add-Panel $slide 660 128 520 456 $C.Panel $C.Line 1 | Out-Null
      Add-Icon $slide $card.icon 690 158 34 | Out-Null
      Add-Text $slide 736 154 370 42 $card.subtitle 27 $C.Text $FontTitle $true | Out-Null
      Add-CompactBullets $slide 694 220 430 68 $card.body 15 4
    } else {
      Add-Panel $slide 80 132 520 440 $C.PanelDark $C.Line 1.2 | Out-Null
      Add-Icon $slide $card.icon 112 164 56 | Out-Null
      Add-Text $slide 184 158 360 54 $card.subtitle 30 $C.Text $FontTitle $true | Out-Null
      Add-Text $slide 112 250 430 190 $card.claim 22 $C.Muted $FontBody | Out-Null
      Add-Panel $slide 640 132 540 440 $C.Panel $C.Line 1 | Out-Null
      Add-Bullets $slide 684 172 450 82 $card.body 17
    }
  }
}

function Add-Thanks($slide, $card) {
  Add-Background $slide
  $bar = $slide.Shapes.AddShape($msoShapeRectangle, (ToPt 520), (ToPt 94), (ToPt 240), (ToPt 6))
  $bar.Fill.ForeColor.RGB = $C.Amber; $bar.Line.Visible = $msoFalse
  Add-Text $slide 150 138 980 56 'DRIFT论文中文讲解' 36 $C.Text $FontTitle $true 'center' | Out-Null
  Add-Line $slide 54 220 1226 220 $C.Line 1.4 | Out-Null
  Add-Text $slide 90 286 1100 96 '感谢聆听' 72 $C.Text $FontTitle $true 'center' | Out-Null
  Add-Text $slide 390 472 500 44 '请老师和同学批评指正' 32 $C.Muted $FontBody $false 'center' | Out-Null
}

$cardsData = Get-Content -LiteralPath $Cards -Raw -Encoding UTF8 | ConvertFrom-Json
$sections = @()
foreach ($section in $cardsData.sectionRoster) { $sections += ,@([string]$section[0], [string]$section[1], [string]$section[2]) }

$ppt = $null
$pres = $null
try {
  $ppt = New-Object -ComObject PowerPoint.Application
  $ppt.Visible = $msoTrue
  if (Test-Path -LiteralPath $LatexAddinPath) {
    try {
      $addin = $ppt.AddIns.Add($LatexAddinPath)
      $addin.Loaded = $msoTrue
    } catch {}
  }
  $pres = $ppt.Presentations.Add()
  $pres.PageSetup.SlideWidth = ToPt 1280
  $pres.PageSetup.SlideHeight = ToPt 720

  foreach ($card in $cardsData.slides) {
    $slide = $pres.Slides.Add($pres.Slides.Count + 1, $ppLayoutBlank)
    switch ([string]$card.layoutFamily) {
      'cover' { Add-Cover $slide $card }
      'directory' { Add-Directory $slide $card $sections }
      'section divider' { Add-Section $slide $card $sections }
      'thanks' { Add-Thanks $slide $card }
      default { Add-Body $slide $card $sections }
    }
    Clear-Animations $slide
  }

  $outDir = Split-Path -Parent $OutPptx
  if ($outDir -and -not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }
  $pres.SaveAs($OutPptx)
  if ($PreviewDir) {
    if (-not (Test-Path -LiteralPath $PreviewDir)) { New-Item -ItemType Directory -Force -Path $PreviewDir | Out-Null }
    foreach ($slide in $pres.Slides) {
      $previewPath = Join-Path $PreviewDir ("slide-{0:D2}.png" -f [int]$slide.SlideIndex)
      $slide.Export($previewPath, 'PNG', 1280, 720) | Out-Null
    }
  }
} finally {
  if ($pres -ne $null) { try { $pres.Close() } catch {} }
  if ($ppt -ne $null) { try { $ppt.Quit() } catch {} }
}
Write-Host "Saved PPTX: $OutPptx"
if ($PreviewDir) { Write-Host "Saved previews: $PreviewDir" }
if ($EquationFallbacks.Count -gt 0) {
  Write-Warning ("Equation fallbacks: {0}" -f $EquationFallbacks.Count)
  foreach ($fallback in $EquationFallbacks) { Write-Warning $fallback }
}
