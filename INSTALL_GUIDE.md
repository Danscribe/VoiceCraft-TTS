# 🎙 VoiceCraft TTS — Installation Guide

You have **three ways** to get VoiceCraft running. Pick the one that fits you best.

---

## 🥇 Option 1: Download Ready-Made .exe (Zero Build, Zero Config)

**Best for:** Users who just want to install and go.

### How it works
We use **GitHub Actions** (free cloud servers) to automatically build the `.exe` and installer for you every time a release is published.

### Steps
1. **Upload this project to GitHub** (create a new repo, drag-and-drop these files).
2. Go to **Actions → Build VoiceCraft Installer → Run workflow** (or push a tag like `v1.0.0`).
3. Wait ~10 minutes.
4. Go to **Releases** and download `VoiceCraft_Setup.exe`.
5. Run it on any Windows PC — it installs like any normal program.

> ✅ **Works offline immediately** — 30+ voices are bundled inside.

---

## 🥈 Option 2: One-Click Build on Windows

**Best for:** Users who want to customize or build locally.

### Steps
1. Copy this `tts_app` folder to your Windows PC.
2. Double-click **`bundle/ONE_CLICK_BUILD_WINDOWS.bat`**.
3. Wait 5–10 minutes (it auto-downloads Python if needed, installs deps, downloads voices, builds the `.exe`, and creates the installer).
4. Find your finished installer at `Output/VoiceCraft_Setup.exe`.

> ✅ **Fully automated.** You literally just double-click and wait.

---

## 🥉 Option 3: Run from Source (Any OS)

**Best for:** Developers or Linux/Mac users.

```bash
cd tts_app
pip install -r requirements.txt
python main.py
```

> ⚠️ This requires Python and internet for downloading voices on first use.

---

## 📦 What the Installer Includes

When you run `VoiceCraft_Setup.exe`, you get:

- ✅ A single `.exe` app — no Python needed on the target PC
- ✅ **30+ Piper voices** pre-loaded (English, Spanish, French, German, Japanese, Chinese, Arabic, Hindi, and more)
- ✅ Full mood controls (speed, pitch, emotion)
- ✅ Desktop & Start Menu shortcuts
- ✅ Windows Control Panel uninstall entry
- ✅ Optional cloud providers (Deepgram, Fish Audio, TopMedia AI) — just add API keys in Settings

---

## 🔑 API Keys (Optional)

Cloud voices are **optional**. The app works 100% offline with Piper voices.

If you want premium cloud voices:
- **Deepgram** → Get key at [console.deepgram.com](https://console.deepgram.com)
- **Fish Audio** → Get key at [fish.audio](https://fish.audio)
- **TopMedia AI** → Get key at [topmedia.ai](https://topmedia.ai)

Paste them in the app under **Settings → API Keys**.

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | The batch script auto-installs it. If it fails, install manually from [python.org](https://python.org). |
| "Inno Setup not found" | Download & install from [jrsoftware.org](https://jrsoftware.org/isdl.php), then re-run the batch. The portable `.exe` still works without Inno Setup. |
| Voice download fails | Some voices are hosted on HuggingFace. If a download fails, the app will try again next time you select it. Bundled voices work offline regardless. |
| App won't launch | Make sure you're on Windows 10/11. The `.exe` requires 64-bit Windows. |

---

## 🏗 Technical Notes

- **Build tool:** PyInstaller (onefile + bundled data)
- **Installer tool:** Inno Setup 6 (professional wizard)
- **CI/CD:** GitHub Actions (free for public repos)
- **Offline voices:** Piper TTS models from `rhasspy/piper-voices` on HuggingFace
- **Total installer size:** ~150–400 MB depending on how many voices are bundled

---

## 🚀 Next Steps

1. **Want to distribute it?** Use Option 1 (GitHub Actions) and share the Release link.
2. **Want to customize voices?** Edit `bundle/prepare_offline_voices.py` and add more voice IDs to the `ESSENTIAL_VOICES` list.
3. **Want to rebrand?** Replace `assets/icon.ico` and edit `bundle/installer.iss` with your name/URL.

---

**Questions?** The app is fully open-source. Check the code in `ui/main_app.py` and `tts/piper_engine.py`.
