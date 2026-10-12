Add-Type -AssemblyName System.Drawing
$assetDir = Join-Path $PSScriptRoot 'assets'
$results = foreach ($file in Get-ChildItem -LiteralPath $assetDir -Filter '*.png') {
  $bitmap = [System.Drawing.Bitmap]::new($file.FullName)
  $rect = [System.Drawing.Rectangle]::new(0,0,$bitmap.Width,$bitmap.Height)
  $bits = $bitmap.LockBits($rect,[System.Drawing.Imaging.ImageLockMode]::ReadOnly,[System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $bytes = [byte[]]::new([Math]::Abs($bits.Stride)*$bitmap.Height)
  [System.Runtime.InteropServices.Marshal]::Copy($bits.Scan0,$bytes,0,$bytes.Length)
  $transparent=0; $partial=0; $solid=0; $borderSolid=0; $strong=0; $maxAlpha=0
  for($y=0;$y -lt $bitmap.Height;$y++) {
    for($x=0;$x -lt $bitmap.Width;$x++) {
      $a=$bytes[$y*[Math]::Abs($bits.Stride)+$x*4+3]
      if($a -gt 128){$strong++}; if($a -gt $maxAlpha){$maxAlpha=$a}
      if($a -eq 0){$transparent++}elseif($a -eq 255){$solid++}else{$partial++}
      if(($x -eq 0 -or $y -eq 0 -or $x -eq $bitmap.Width-1 -or $y -eq $bitmap.Height-1) -and $a -gt 128){$borderSolid++}
    }
  }
  $bitmap.UnlockBits($bits)
  [pscustomobject]@{file=$file.Name;width=$bitmap.Width;height=$bitmap.Height;format=$bitmap.PixelFormat.ToString();fullyTransparentPixels=$transparent;partialAlphaPixels=$partial;opaquePixels=$solid;strongAlphaPixels=$strong;maxAlpha=$maxAlpha;solidBorderPixels=$borderSolid;sha256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash;status= $(if($transparent -gt 0 -and $strong -gt 0){'rgba_content_verified'}else{'inspect_required'})}
  $bitmap.Dispose()
}
$results | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'asset-verification.json') -Encoding utf8
$results | Select-Object file,width,height,status,solidBorderPixels | Format-Table -AutoSize
$manifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'asset-manifest.json') -Raw | ConvertFrom-Json
$bounds=foreach($asset in $manifest.assets){
  $bitmap=[System.Drawing.Bitmap]::new((Join-Path $PSScriptRoot $asset.file))
  $rect=[System.Drawing.Rectangle]::new(0,0,$bitmap.Width,$bitmap.Height)
  $bits=$bitmap.LockBits($rect,[System.Drawing.Imaging.ImageLockMode]::ReadOnly,[System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $bytes=[byte[]]::new([Math]::Abs($bits.Stride)*$bitmap.Height)
  [System.Runtime.InteropServices.Marshal]::Copy($bits.Scan0,$bytes,0,$bytes.Length)
  foreach($pose in $asset.poses){
    $r=$pose.sourceRect; $minX=$r[2];$minY=$r[3];$maxX=-1;$maxY=-1;$boundary=0
    for($y=0;$y -lt $r[3];$y++){for($x=0;$x -lt $r[2];$x++){
      $a=$bytes[($y+$r[1])*[Math]::Abs($bits.Stride)+($x+$r[0])*4+3]
      if($a -gt 32){$minX=[Math]::Min($minX,$x);$maxX=[Math]::Max($maxX,$x);$minY=[Math]::Min($minY,$y);$maxY=[Math]::Max($maxY,$y)}
      if($a -gt 128 -and ($x -eq 0 -or $y -eq 0 -or $x -eq $r[2]-1 -or $y -eq $r[3]-1)){$boundary++}
    }}
    [pscustomobject]@{id=$pose.id;localAlphaBounds=@($minX,$minY,($maxX-$minX+1),($maxY-$minY+1));localBottomCenter=@((($minX+$maxX)/2),$maxY);strongPixelsOnCropBoundary=$boundary;note='Alpha bounds are measured. Bottom-center is NOT a verified anatomical foot pivot.'}
  }
  $bitmap.UnlockBits($bits);$bitmap.Dispose()
}
$bounds | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'pose-bounds.json') -Encoding utf8
$bounds | Where-Object {$_.strongPixelsOnCropBoundary -gt 0} | Select-Object id,strongPixelsOnCropBoundary | Format-Table -AutoSize
