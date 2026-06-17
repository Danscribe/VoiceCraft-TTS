#!/usr/bin/env python3
"""
Pre-downloads the most popular Piper voices so they can be bundled
into the installer for 100% offline use.
Run this BEFORE building the .exe.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from tts.piper_engine import download_voice, PIPER_DIR

# Essential voices to bundle for offline use (covers major languages + quality)
ESSENTIAL_VOICES = [
    # English (US) - high quality
    "en_US-amy-medium",
    "en_US-ryan-high",
    "en_US-lessac-high",
    "en_US-libritts-high",
    "en_US-joe-medium",
    # English (UK)
    "en_GB-cori-high",
    "en_GB-alan-medium",
    "en_GB-southern_english_female-medium",
    # English variants
    "en_AU-natasha-medium",
    "en_CA-claire-medium",
    # Spanish
    "es_ES-carlfm-x_low",
    "es_MX-ald-medium",
    # French
    "fr_FR-siwis-medium",
    "fr_FR-tom-medium",
    # German
    "de_DE-thorsten-high",
    "de_DE-eva_k-medium",
    # Italian
    "it_IT-paola-medium",
    # Portuguese
    "pt_BR-faber-medium",
    "pt_PT-tugão-medium",
    # Russian
    "ru_RU-irina-medium",
    # Chinese
    "zh_CN-huayan-medium",
    # Japanese
    "ja_JP-0amazon-medium",
    # Korean
    "ko_KO-0gihun-medium",
    # Arabic
    "ar_JO-kareem-medium",
    # Hindi
    "hi_IN-cmu_indic_medium",
    # Dutch
    "nl_NL-thijs-medium",
    # Polish
    "pl_PL-gosia-medium",
    # Turkish
    "tr_TR-fahrettin-medium",
    # Swedish
    "sv_SE-nst-medium",
    # Others
    "en_US-hfc_female",
    "en_US-hfc_male",
    "en_GB-northern_english_male-medium",
    "de_DE-thorsten_emotional-medium",
]

def main():
    print("=" * 60)
    print("VoiceCraft Offline Voice Pack Builder")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for i, voice_id in enumerate(ESSENTIAL_VOICES, 1):
        print(f"\n[{i}/{len(ESSENTIAL_VOICES)}] Downloading {voice_id}...")
        try:
            def progress(p, msg):
                print(f"  {msg} ({p*100:.0f}%)")
            
            result = download_voice(voice_id, progress_callback=progress)
            if result:
                print(f"  ✓ Success -> {result}")
                success += 1
            else:
                print(f"  ✗ Failed")
                failed += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Done! {success} voices ready, {failed} failed.")
    print(f"Voice cache location: {PIPER_DIR}")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
