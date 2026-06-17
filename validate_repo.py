#!/usr/bin/env python3
"""
Run this BEFORE uploading to GitHub to make sure everything is in place
for the automated build to succeed.
"""
import sys
from pathlib import Path

REQUIRED_FILES = [
    "main.py",
    "requirements.txt",
    "bundle/prepare_offline_voices.py",
    "bundle/pyinstaller_offline.spec",
    "bundle/installer.iss",
    ".github/workflows/build-release.yml",
]

REQUIRED_FOLDERS = [
    "ui",
    "tts",
    "config",
    "bundle",
    ".github/workflows",
]

def main():
    root = Path(__file__).parent
    issues = []
    
    print("🔍 VoiceCraft Repository Validator")
    print("=" * 50)
    
    for f in REQUIRED_FILES:
        path = root / f
        if path.exists():
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f}  MISSING")
            issues.append(f)
    
    for d in REQUIRED_FOLDERS:
        path = root / d
        if path.exists() and path.is_dir():
            print(f"  ✅ {d}/")
        else:
            print(f"  ❌ {d}/  MISSING")
            issues.append(d)
    
    print("=" * 50)
    if not issues:
        print("✅ All required files are present. Ready to upload to GitHub!")
        print()
        print("Next steps:")
        print("  1. Create a new public repo on GitHub.")
        print("  2. Upload ALL files in this folder (not the parent folder).")
        print("  3. Go to Actions → Build VoiceCraft Installer → Run workflow.")
        return 0
    else:
        print(f"❌ {len(issues)} issue(s) found. Please fix before uploading.")
        print()
        print("Missing items:")
        for i in issues:
            print(f"   - {i}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
