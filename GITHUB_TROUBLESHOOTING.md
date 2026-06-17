# GitHub Actions Build Troubleshooting

## Your Error: Build failed in 29 seconds

The logs you showed only had the **cleanup phase** (git config, Node warnings). The actual error happened **before** that but wasn't visible in your snippet. Here are the most common causes and fixes.

---

## 🔍 Quick Diagnosis Checklist

### 1. Did you upload files to the **root** of the repo?

**WRONG structure** (build will fail):
```
VoiceCraft-TTS/
  └── tts_app/           ← ❌ Don't put everything in a subfolder
      ├── main.py
      ├── requirements.txt
      └── ...
```

**CORRECT structure** (build works):
```
VoiceCraft-TTS/
  ├── main.py             ← ✅ At root
  ├── requirements.txt    ← ✅ At root
  ├── bundle/
  ├── ui/
  ├── tts/
  ├── config/
  └── .github/
      └── workflows/
          └── build-release.yml
```

**Fix:** Move all files from `tts_app/` up to the repo root. Or use the new **auto-detect** workflow I just added below.

---

### 2. Which workflow did you use?

I created **two workflow files** for you. Pick the one that matches your situation:

| Workflow | Best for | File |
|----------|----------|------|
| **Full** | Files at root, wants bundled voices | `.github/workflows/build-release.yml` |
| **Simple** | Files in subfolder, or quick test | `.github/workflows/build-simple.yml` |

---

## ✅ FIX: Copy these updated files to your repo

### Step 1: Update your main workflow file

Copy the contents below and paste it into your repo at:
**`.github/workflows/build-release.yml`**

(Use the file from the updated `tts_app/.github/workflows/build-release.yml` I just created — it auto-detects if your files are in a `tts_app/` subfolder.)

### Step 2: Alternative: Use the simple workflow

If the full build keeps failing, use this simpler one instead. It skips the voice bundling (voices download on first app use).

Create this file in your repo:
**`.github/workflows/build-simple.yml`**

```yaml
name: Build VoiceCraft Installer (Simple)

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version tag (e.g., v1.0.0)'
        required: true
        default: 'v1.0.0'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Detect project root
        id: detect
        run: |
          if (Test-Path "tts_app/main.py") {
            "root=tts_app" | Out-File -FilePath $env:GITHUB_OUTPUT -Append
          } else {
            "root=." | Out-File -FilePath $env:GITHUB_OUTPUT -Append
          }

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        working-directory: ${{ steps.detect.outputs.root }}
        run: |
          python -m pip install --upgrade pip
          pip install customtkinter pygame pydub requests pyperclip Pillow soundfile numpy pyinstaller

      - name: Build EXE
        working-directory: ${{ steps.detect.outputs.root }}
        run: |
          pyinstaller main.py --name=VoiceCraft_TTS --onefile --windowed --clean --noconfirm `
            --hidden-import=customtkinter --hidden-import=pygame --hidden-import=pydub `
            --hidden-import=requests --hidden-import=pyperclip --hidden-import=PIL `
            --hidden-import=soundfile --hidden-import=numpy

      - name: Upload EXE
        uses: actions/upload-artifact@v4
        with:
          name: VoiceCraft_TTS_Portable
          path: ${{ steps.detect.outputs.root }}/dist/VoiceCraft_TTS.exe
```

---

## 🔧 If you want to see the ACTUAL error

Your log only showed the cleanup phase. To find the real error:

1. Go to your repo: `github.com/Danscribe/VoiceCraft-TTS/actions`
2. Click the **failed run** (the one with the red X)
3. Click **"build-windows"** on the left
4. Look for the step with a **red X** icon (not the last one — scroll up!)
5. Expand that step by clicking the arrow next to it
6. The error message will be in red text

**Common errors you'll see:**

| Error | Meaning | Fix |
|-------|---------|-----|
| `FileNotFoundError: requirements.txt` | Files in wrong folder | Move files to root or use simple workflow |
| `No module named 'piper'` | Can't install piper-tts | Use simple workflow (skips piper) |
| `Failed to download voice` | HuggingFace timeout | Re-run workflow or use simple workflow |
| `ISCC.exe not found` | Inno Setup failed | Download portable EXE from Artifacts instead |
| `Error: No .py files found` | Wrong directory structure | Move files to root of repo |

---

## 🚀 FASTEST WORKAROUND (Recommended)

If the build keeps failing, do this **3-minute manual fix**:

1. On your repo page, click **"Add file" → "Create new file"**
2. Name it: `.github/workflows/build-simple.yml`
3. Paste the YAML code above
4. Click **"Commit changes..."** → **"Commit directly to main branch"**
5. Go to **Actions** tab → click **"Build VoiceCraft Installer (Simple)"** on the left
6. Click **"Run workflow"** → type `v1.0.0` → **Run**
7. Wait 3–5 minutes
8. Download the `.exe` from the **Artifacts** section

This version:
- ✅ Works with files in `tts_app/` subfolder OR root
- ✅ Skips problematic voice bundling
- ✅ Voices download automatically when you first use the app
- ✅ Still works 100% offline after first voice download

---

## 📝 Still not working? Check this list

1. [ ] Is your repo **Public**? (Private repos have limited free Actions minutes)
2. [ ] Is `main.py` at the repo root or in `tts_app/`?
3. [ ] Is `.github/workflows/` at the repo root (not inside `tts_app/`)?
4. [ ] Did you click **Actions → Run workflow** (not just wait for a push)?
5. [ ] Did you scroll UP in the logs to find the red error message?

---

## 📎 Download the finished EXE

If the build fails at the Inno Setup step, **don't worry** — the portable `.exe` is still uploaded:

1. Go to your **Actions** page
2. Click the completed (or failed) run
3. Scroll to the bottom to **Artifacts**
4. Click **"VoiceCraft_TTS_Portable"** to download the ZIP
5. Extract it — the `.exe` inside works immediately

---

## 🎯 Need help?

Reply with:
- The **exact error text** (in red) from the failed step
- Or a screenshot of the **Actions → build-windows → failed step**

I can then give you a precise fix.
