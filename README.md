# VoiceCraft TTS 🎙

A modern, dark-themed desktop Text-to-Speech application with **300+ voices**, mood controls, emotion reactions, and multi-provider support. Works **fully offline** with bundled voices, and expands with cloud APIs when you're online.

## 🚀 Zero-Build Installation (Recommended)

You have **two ways** to get a ready-made `.exe` without building anything yourself:

### Option A: Download from GitHub Releases (Easiest — Zero Build)
We use GitHub Actions (free cloud servers) to build the `.exe` automatically for you. You just download the finished installer.

**Step-by-step guide:** See [`GITHUB_BUILD_GUIDE.md`](GITHUB_BUILD_GUIDE.md) for a complete walkthrough with screenshots. In short:
1. Upload this project to a new **public** GitHub repository
2. Go to **Actions → Build VoiceCraft (Simple) → Run workflow**
3. Wait ~3 minutes while a free Windows server builds the portable `.exe`
4. Download `VoiceCraft_TTS_Portable.zip` from **Artifacts**
5. Run it on any Windows PC!

> ⚠️ **Note:** The "Simple" build creates a **portable `.exe` without voices bundled**. See the **Offline Voice Pack** section below to download voices for offline use.

> For an installer with voices pre-bundled, use the `Build VoiceCraft Installer` workflow (may take 10–15 min and can fail on voice downloads).

### Option B: One-Click Build on Your PC
If you want to build it yourself or customize the voice pack:

1. **Download this repository** (or clone it)
2. On Windows, double-click **`bundle/ONE_CLICK_BUILD_WINDOWS.bat`**
3. Wait 5–10 minutes while it automatically:
   - Downloads & installs Python (if missing)
   - Installs all dependencies
   - Downloads the offline voice pack
   - Builds the `.exe` with PyInstaller
   - Creates a professional `VoiceCraft_Setup.exe` installer
4. Find your installer in `Output/VoiceCraft_Setup.exe`

> **Requirements:** Windows 10/11. The script will download everything else automatically.

---

## 🖥 Run from Source (Developers)

```bash
cd tts_app
pip install -r requirements.txt
python main.py
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **300+ Voices** | Piper (offline), Deepgram Aura, Fish Audio, TopMedia AI |
| **Offline Mode** | 30+ bundled Piper voices — works without internet or API keys |
| **Mood Controls** | Speed (0.5x–2.0x), Pitch shift, 10 emotion presets |
| **Modern Dark UI** | Built with CustomTkinter — smooth, responsive, native feel |
| **One-Click Download** | Save audio as MP3, WAV, OGG, or FLAC |
| **Auto-Play Preview** | Listen instantly after generation |
| **Favorites & History** | Save your most-used voices and recent texts |
| **Voice Search & Filter** | Find voices by provider, language, gender, or name |
| **Voice Status Icons** | ✅ Bundled offline • 🆓 Downloaded • ⬇ Needs download • ☁ Cloud |

---

## 🔌 API Keys (Optional)

For cloud voices, add your keys in **Settings → API Keys**:

- **Deepgram** → [console.deepgram.com](https://console.deepgram.com)
- **Fish Audio** → [fish.audio](https://fish.audio)
- **TopMedia AI** → [topmedia.ai](https://topmedia.ai)

Piper voices (🆓/✅ icons) work **without any API keys or internet**.

---

## 📦 Offline Voice Pack (For PCs Without Internet)

The **GitHub Actions "Simple" build** creates a portable `.exe` but does **not** include voice models inside it. To use the app on a PC with **no internet**, you need to download the voices separately on an **online PC** and transfer them.

### Quick Steps
1. **Online PC:** Run `bundle/download_voices_pack.bat` → Creates `VoiceCraft_Voices.zip` (~150–300 MB)
2. **Transfer:** Copy `VoiceCraft_TTS.exe` + `VoiceCraft_Voices.zip` to the offline PC (USB, email, etc.)
3. **Offline PC:** Run `bundle/install_voices_offline.bat` (or extract ZIP manually to `~/.voicecraft_tts/piper_voices/`)
4. **Launch:** Open `VoiceCraft_TTS.exe` — all voices show the ✅ icon and work offline!

**Full guide:** See [`OFFLINE_VOICE_PACK_GUIDE.md`](OFFLINE_VOICE_PACK_GUIDE.md)

---

## 📁 Project Structure

```
tts_app/
├── main.py                      # Launch the app
├── requirements.txt             # Dependencies
│
├── ui/
│   ├── main_app.py              # Full GUI (sidebar, controls, settings)
│   └── welcome_dialog.py        # First-run offline welcome
│
├── tts/
│   ├── piper_engine.py          # Offline synthesis + auto-download
│   ├── api_providers.py         # Deepgram / Fish Audio / TopMedia AI
│   └── audio_player.py          # Playback engine
│
├── config/
│   ├── settings.py              # User config & API keys storage
│   └── voice_data.py            # 300+ voice registry
│
├── bundle/
│   ├── ONE_CLICK_BUILD_WINDOWS.bat   # Windows auto-builder
│   ├── download_voices_pack.bat      # Download voice pack for offline PCs
│   ├── install_voices_offline.bat    # Install voice pack on offline PC
│   ├── prepare_offline_voices.py     # Pre-download voice pack
│   ├── pyinstaller_offline.spec      # PyInstaller spec (bundles voices)
│   └── installer.iss                 # Inno Setup professional installer
│
├── .github/
│   └── workflows/
│       └── build-release.yml    # GitHub Actions CI/CD — auto-builds releases
│
└── README.md
```

---

## 🏗 Build Details

### What the build does
1. **Freezes Python** into a single `.exe` via PyInstaller
2. **Bundles 30+ Piper voice models** (≈ 300–800 MB) so the app works offline
3. **Packages everything** into a Windows installer using Inno Setup
4. **Creates shortcuts** on Desktop & Start Menu
5. **Registers uninstaller** in Control Panel / Settings

### CI/CD (GitHub Actions)
Push a tag like `v1.0.0` and GitHub automatically:
- Builds the `.exe` on a Windows runner
- Bundles the offline voice pack
- Creates a release with the installer attached
- **You just download the `.exe` from the Releases page**

---

## 📝 License

MIT License — free for personal and commercial use.
