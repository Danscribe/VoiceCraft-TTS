# 🎙 VoiceCraft TTS — Offline Voice Pack Guide

## The Problem

The **GitHub Actions "Simple" build** creates a portable `.exe` but does **not** include voice models inside it. When you run the app on an offline PC, it has no voices to use.

## The Solution: Voice Pack System

We use a **two-step process**:

1. **Online PC** → Run `download_voices_pack.bat` → Downloads 30 voices → Creates `VoiceCraft_Voices.zip`
2. **Offline PC** → Extract voices to `~/.voicecraft_tts/piper_voices/` → Launch app → Works offline!

---

## Step 1: Download Voice Pack (ONLINE PC with Internet)

1. Copy the `bundle/` folder from this project to any Windows PC with internet.
2. Double-click **`bundle/download_voices_pack.bat`**
3. Wait 5–10 minutes while it downloads 30 essential Piper voices.
4. It will create a file called **`VoiceCraft_Voices.zip`** in the same folder.

**What gets downloaded?** 30 high-quality voices covering:
- English (US, UK, AU, CA) — 5 voices
- Spanish, French, German, Italian, Portuguese
- Russian, Chinese, Japanese, Korean
- Arabic, Hindi, Dutch, Polish, Turkish, Swedish
- Plus emotional and neutral variants

**ZIP size:** ~150–300 MB (varies by voice quality)

---

## Step 2: Transfer to Offline PC

Copy these two files to your offline PC:
- `VoiceCraft_TTS.exe` (the app, built from GitHub Actions)
- `VoiceCraft_Voices.zip` (the voice pack, created above)

Use a **USB drive**, **external hard drive**, **DVD**, **email attachment** (if under 25 MB), or **network share**.

---

## Step 3: Install Voices on Offline PC

### Option A: Run the Auto-Installer (Easiest)

1. Place `VoiceCraft_Voices.zip` and `install_voices_offline.bat` in the same folder.
2. Double-click **`install_voices_offline.bat`**
3. It extracts all voices to the correct cache folder automatically.
4. Done! Launch `VoiceCraft_TTS.exe`.

### Option B: Manual Extraction

1. Extract `VoiceCraft_Voices.zip` using Windows Explorer or any ZIP tool.
2. Open the extracted folder — you should see `.onnx` and `.onnx.json` files.
3. Move all these files to:
   ```
   C:\Users\[YourUsername]\.voicecraft_tts\piper_voices\
   ```
   (Create the folders if they don't exist.)
4. Launch `VoiceCraft_TTS.exe`.

---

## Step 4: Verify Offline Mode

1. Open VoiceCraft TTS.
2. In the voice list, look for the ✅ (checkmark) icon — these are the voices you just installed.
3. Select any ✅ voice, type text, and click **Generate Speech**.
4. It works **without any internet connection**!

---

## For Distributors: How to Share the Complete Package

If you want to give someone else a fully offline-ready setup, prepare:

```
VoiceCraft_Offline_Package/
├── VoiceCraft_TTS.exe          ← Build this from GitHub Actions
├── VoiceCraft_Voices.zip        ← Create this with download_voices_pack.bat
├── install_voices_offline.bat   ← Included in bundle/
├── README.txt                   ← Quick instructions
└── (optional) VoiceCraft icon   ← For branding
```

**Recipient instructions:**
1. Extract the ZIP somewhere.
2. Double-click `install_voices_offline.bat` (this unpacks the voices).
3. Double-click `VoiceCraft_TTS.exe` to launch the app.

---

## Frequently Asked Questions

**Q: Do I need to download voices again for every new PC?**
A: Yes, each PC needs its own voice cache. Or you can copy the `piper_voices` folder from one PC to another via USB.

**Q: Can I add more voices later?**
A: Yes! On an online PC, run the app, select any voice with the ⬇ (download) icon, and generate once. It downloads the model. Then copy the `piper_voices` folder to your offline PC.

**Q: What if the voice pack ZIP is too large for email?**
A: Use a cloud storage link (Google Drive, Dropbox, WeTransfer), a USB drive, or split the ZIP with a tool like 7-Zip.

**Q: Can I choose which voices to download?**
A: Yes. Open `bundle/download_voices_pack.bat` in a text editor. Find the `ESSENTIAL_VOICES` list and delete the lines you don't want, or add new ones from `config/voice_data.py`.

**Q: Do I need Python on the offline PC?**
A: **No.** The `.exe` is a standalone app. The voice pack is just data files (`.onnx` models). No Python needed on the offline PC.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Script file main.py does not exist" | Rebuild the `.exe` from GitHub Actions (Simple workflow) |
| "Voice not available" error | Make sure voices are in `~\.voicecraft_tts\piper_voices\` |
| App shows ⬇ icon instead of ✅ | Voice hasn't been downloaded yet. Run on an online PC first, or use the voice pack. |
| ZIP extraction fails | Make sure the ZIP is fully copied. Use `install_voices_offline.bat` instead. |
| Only a few voices work | Some voices may have failed to download. Check the `download_voices_pack.bat` output. |
