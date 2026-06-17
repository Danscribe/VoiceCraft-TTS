# 🚀 Option A: Build Your `.exe` Automatically on GitHub (Zero Local Setup)

This guide will take you from **zero** to a downloadable `VoiceCraft_Setup.exe` using **GitHub Actions** — free cloud servers that build the app for you. You don't need to install Python, PyInstaller, or anything on your PC.

**Time required:** ~15 minutes of setup, then ~10 minutes of waiting for the cloud build.  
**Cost:** $0 (GitHub Actions is free for public repositories).  
**What you get:** A professional Windows installer (`.exe`) that works offline with 30+ bundled voices.

---

## 📋 Overview of Steps

1. Create a GitHub account (free)
2. Create a new repository
3. Upload the VoiceCraft project files
4. Trigger the automated build
5. Download the finished installer from Releases

---

## Step 1: Create a GitHub Account (Free)

1. Open your browser and go to **[github.com](https://github.com)**.
2. Click the green **"Sign up"** button (top-right corner).
3. Enter your email address and create a password.
4. Choose a username (e.g., `yourname-voicecraft`).
5. Complete the CAPTCHA/puzzle verification.
6. Click **"Create account"**.
7. Check your email inbox for a verification email from GitHub.
8. Click the **"Verify email address"** button in the email.
9. On the welcome page, select **"Just me"** and **"Skip personalization"**.

✅ **You now have a GitHub account.**

---

## Step 2: Create a New Repository (Project Storage)

A "repository" is just a folder on GitHub where your project files live.

1. Make sure you are logged in to **[github.com](https://github.com)**.
2. In the top-right corner, click the **"+"** icon (next to your profile picture).
3. Click **"New repository"** from the dropdown menu.
4. In the **"Repository name"** box, type: `VoiceCraft-TTS`
5. In the **"Description"** box (optional), type: `Offline-ready AI Text-to-Speech app with 300+ voices`
6. Select **"Public"** (this is free and required for free GitHub Actions minutes).
7. **Uncheck** the box that says **"Add a README file"** (we already have one).
8. **Uncheck** the box that says **"Add .gitignore"** (we already have one).
9. **Uncheck** the box that says **"Choose a license"**.
10. Click the green **"Create repository"** button at the bottom.

✅ **You now have an empty repository ready to receive files.**

---

## Step 3: Upload the VoiceCraft Files

There are **two ways** to do this. Use **Method A** if you have the files on your computer. Use **Method B** if you are using this workspace directly.

### Method A: Upload from Your Computer (Easiest)

1. On your new repository page, click the gray button that says **"uploading an existing file"** (in the Quick Setup section).
   - *Alternative:* Click the **"<> Code"** tab near the top, then click the **"Add file"** dropdown → **"Upload files"**.
2. Open your computer's file explorer and find the `tts_app` folder containing all the project files.
3. **Drag and drop** the entire contents of the `tts_app` folder into the GitHub upload box.  
   - You must upload the files **individually or as a ZIP** because GitHub's web upload doesn't support folders directly.
   - **Best approach:** Compress the `tts_app` folder into a ZIP file, drag it into the upload box, then click **"Commit changes"**. Wait a moment, then click the **"<> Code"** tab again. You will see a `tts_app.zip` file. Click it, then click **"Extract"** (if GitHub shows that option) or just leave it as a ZIP — the workflow can handle it either way.
   - **Even better approach:** See Method B below using GitHub Desktop or command line. But if you want purely web-based, upload the ZIP.

4. If you uploaded a ZIP, click the **"Commit changes"** button.

### Method B: Use GitHub Desktop (Recommended for Folders)

If dragging folders doesn't work well, use GitHub's free Desktop app:

1. Download and install **GitHub Desktop** from **[desktop.github.com](https://desktop.github.com)**.
2. Open GitHub Desktop and sign in with your GitHub account.
3. Click **"File" → "Clone repository"**.
4. Select your `VoiceCraft-TTS` repository and click **"Clone"**.
5. This will create a `VoiceCraft-TTS` folder on your computer (usually in `Documents/GitHub`).
6. Open that folder. Copy **all** the files from the `tts_app` project into it.
7. Return to GitHub Desktop. You will see all the files listed in the left panel.
8. At the bottom, type a summary: `Initial project upload`
9. Click the **"Commit to main"** button.
10. Click the **"Push origin"** button at the top.

✅ **All your project files are now on GitHub.**

---

## Step 4: Verify the Workflow File is in Place

The magic that builds your `.exe` is a file called `build-release.yml`. Let's make sure it's there.

1. On your GitHub repository page, click the **"<> Code"** tab.
2. Look for a folder named `.github`. If you don't see it immediately, check if your files are inside a `tts_app` subfolder — this is OK.
3. Navigate to: `.github/workflows/build-release.yml`.
4. Click the file name to open it. You should see code about `Build VoiceCraft Installer`.

If the `.github` folder is missing, you need to add it manually:

1. Click **"Add file" → "Create new file"**.
2. In the **"Name your file..."** box, type exactly: `.github/workflows/build-release.yml`
3. Copy the entire contents of the file from your project (`tts_app/.github/workflows/build-release.yml`) and paste it into the GitHub text editor.
4. Click **"Commit changes..."** at the top, then click **"Commit changes"** again.

✅ **GitHub Actions is now configured.**

---

## Step 5: Trigger the Automated Build

There are two ways to start the build. Use **Method A** for instant building. Use **Method B** for versioned releases.

### Method A: Manual Trigger (Fastest — Recommended First Time)

1. On your repository page, click the **"Actions"** tab at the top (between "Pull requests" and "Projects").
2. On the left side, you will see a workflow called **"Build VoiceCraft Installer"**. Click it.
3. On the right side, click the gray button that says **"Run workflow"**.
4. A dropdown will appear. In the **"Version tag"** box, type: `v1.0.0`
5. Click the green **"Run workflow"** button inside the dropdown.
6. GitHub will queue the job. Click the new row that appears below to watch it run.

### Method B: Create a Release Tag (Best for Distribution)

1. On your repository page, click the **"<> Code"** tab.
2. On the right side, look for **"Releases"** and click it.
3. Click the green **"Create a new release"** button.
4. Click the **"Choose a tag"** dropdown, type `v1.0.0`, and click **"Create new tag: v1.0.0 on publish"**.
5. In the **"Release title"** box, type: `VoiceCraft TTS v1.0.0`
6. In the large text box, paste this description:
   ```
   🎙 VoiceCraft TTS — First Release
   - 30+ offline Piper voices bundled
   - Deepgram, Fish Audio, TopMedia AI cloud support
   - Mood controls: speed, pitch, emotion
   - Modern dark UI
   ```
7. Scroll down and click the green **"Publish release"** button.
8. This will automatically trigger the build workflow.

✅ **The build is now running in the cloud.**

---

## Step 6: Wait for the Build (10–15 Minutes)

1. Click the **"Actions"** tab at the top of your repository.
2. You will see a yellow dot next to your running workflow. Click it to open the details.
3. You will see a list of steps running in real-time:
   - `Checkout repository` (downloads your code)
   - `Set up Python` (installs Python 3.11)
   - `Install dependencies` (downloads libraries)
   - `Download offline voice pack` (downloads 30 voice models — **this takes the longest**, ~5–8 minutes)
   - `Build with PyInstaller` (compiles the .exe)
   - `Bundle voices into dist` (packages voices)
   - `Install Inno Setup` (installs the installer tool)
   - `Build Installer` (creates the final setup.exe)
   - `Upload Installer Artifact` (saves it for you to download)
   - `Create Release` (attaches it to your release page)
4. Wait for the green checkmark ✅ to appear at the top.

**If the build fails:**
- Click the failed step to read the error.
- Common fixes:
  - If it fails at "Build Installer" because Inno Setup is missing, the workflow will still upload the portable `.exe` as an artifact — you can still download it!
  - If voices fail to download, the build will still complete with the voices that succeeded.

✅ **Build complete.**

---

## Step 7: Download Your Installer

### From Artifacts (Always Works)

1. Go to the completed workflow run (Actions tab → click the finished run).
2. Scroll down to the **"Artifacts"** section at the bottom.
3. You will see an artifact named `VoiceCraft_Setup_v1.0.0` (or similar).
4. Click it. It will download a ZIP file to your computer.
5. Extract the ZIP. Inside is your `VoiceCraft_Setup.exe`.

### From Releases (If You Used Method B)

1. Click the **"Releases"** section on the right side of your repo.
2. Click on the release title (e.g., `VoiceCraft TTS v1.0.0`).
3. Under **"Assets"**, you will see `VoiceCraft_Setup.exe`.
4. Click it to download directly.

✅ **You now have the installer file.**

---

## Step 8: Install and Test on Windows

1. Move `VoiceCraft_Setup.exe` to your Windows PC.
2. Double-click it. Windows may show a "Windows protected your PC" warning (because it's an unsigned app).  
   - Click **"More info"**, then **"Run anyway"**.
3. The installer wizard will open. Click **"Next"** through the steps.
4. Choose whether to create a Desktop shortcut.
5. Click **"Install"**, then **"Finish"**.
6. Launch **VoiceCraft TTS** from your Desktop or Start Menu.
7. The first-run welcome screen will say: **"✅ 30 offline voices are bundled and ready!"**
8. Select a voice with the ✅ icon, type some text, and click **Generate Speech**.

🎉 **It works completely offline.**

---

## 🔁 How to Rebuild (After Updates)

If you change the code later and want a new version:

1. Update your files on GitHub (upload new versions or edit in the browser).
2. Go to **Actions → Build VoiceCraft Installer → Run workflow**.
3. Type a new version tag, e.g., `v1.1.0`.
4. Wait 10 minutes.
5. Download the new installer.

---

## 🛠 Troubleshooting

| Problem | What to Do |
|---------|------------|
| **"Windows protected your PC"** warning | This is normal for unsigned apps. Click **More info → Run anyway**. |
| **Build failed at "Download offline voice pack"** | Some voices might be temporarily unavailable. The workflow will continue with what succeeded. You can still download the portable `.exe` from Artifacts. |
| **Build failed at "Build Installer"** | Inno Setup might have failed to install. The portable `.exe` is still in the Artifacts. Download that instead — it works without an installer. |
| **I can't find the Actions tab** | Make sure your repository is **Public** (free). Private repositories get limited free minutes. |
| **"Workflow not found"** | Make sure the file is at exactly `.github/workflows/build-release.yml` (with the dot in front of `.github`). |

---

## 📊 What Happens Behind the Scenes (For Your Understanding)

When you click **"Run workflow"**, GitHub spins up a **free Windows server** in the cloud and does this automatically:

```
1. GitHub Server (Windows 10 VM)
   ├─ 2. Installs Python 3.11
   ├─ 3. pip installs all libraries (customtkinter, pygame, etc.)
   ├─ 4. Downloads 30 Piper voice models from HuggingFace (~150MB)
   ├─ 5. PyInstaller compiles everything into one .exe
   ├─ 6. Inno Setup wraps it into a Setup.exe installer
   └─ 7. Uploads the result to your GitHub Releases / Artifacts
```

You don't do any of this manually. You just click the button.

---

## 🎁 What's Included in the Final Installer

- `VoiceCraft_Setup.exe` (~150–400 MB depending on voice count)
- Installs to `C:\Program Files\VoiceCraft TTS`
- Desktop & Start Menu shortcuts
- 30+ pre-bundled voices (English, Spanish, French, German, Japanese, Chinese, Arabic, Hindi, and more)
- Uninstall entry in Windows Settings / Control Panel
- Works completely offline for bundled voices
- Cloud voice support (Deepgram, Fish Audio, TopMedia AI) via optional API keys

---

## ✅ Checklist

- [ ] Created GitHub account
- [ ] Created `VoiceCraft-TTS` repository (Public)
- [ ] Uploaded all project files
- [ ] Verified `.github/workflows/build-release.yml` exists
- [ ] Clicked **Actions → Run workflow**
- [ ] Waited for green checkmark ✅
- [ ] Downloaded `VoiceCraft_Setup.exe` from Artifacts or Releases
- [ ] Installed on Windows and tested offline voice generation

**Done!** 🎉 You now have a professional, distributable, offline-ready TTS application.
