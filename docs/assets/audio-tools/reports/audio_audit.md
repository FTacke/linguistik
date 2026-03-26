# Audio Audit Report

- Audio root: `C:\dev\linguistik.hispanistica\docs\assets\audiofiles`
- Files scanned: 64
- ffprobe: `C:\Users\Felix Tacke\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffprobe.exe`
- ffmpeg: `C:\Users\Felix Tacke\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe`
- Pass: 63
- Warn: 1
- Fail: 0

## Manual Review Files

- `audio_audit.csv`: technical audit with manual review columns.
- `audio_manual_review.csv`: identical checklist copy for hands-on QA updates.

## Flagged Files

| File | Status | Notes |
| --- | --- | --- |
| `corapan/URY8b580411c.mp3` | warn | bitrate outside 48-320 kbps: 33.1 |
