#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

# Definiere alle Dokumente mit Literaturabschnitten
docs_to_process = [
    'docs/aussprache.md',
    'docs/wandel.md',
    'docs/herkunftssprachen.md',
    'docs/variation/variation_anrede.md',
    'docs/kreativitaet.md',
    'docs/fehlerlinguistik.md',
    'docs/orthographie.md',
    'docs/variation/variation_aussprache.md',
    'docs/variation/variation_plurizentrik.md'
]

changes_log = []

def normalize_bibliography(text):
    """Wendet alle Normalisierungsregeln an"""
    original = text
    
    # 1. (Hrsg.) -> (Hg.)
    text = re.sub(r'\(Hrsg\.\)', '(Hg.)', text)
    
    # 2. "&" -> " / " in Autorenlisten
    # Pattern 1: "Name1 & Name2 (Jahr):"
    text = re.sub(r'([a-zäöüß])\s+&\s+([A-Z])', r'\1 / \2', text)
    # Pattern 2: "Name1 & Name2 (Hg.)"
    text = re.sub(r'([a-zäöüß])\s+&\s+(\w+)\s+\(Hg', r'\1 / \2 (Hg', text)
    
    # 3. "in:" -> "In:" (nach Anführungszeichen)
    text = re.sub(r'"\s*,?\s+in:', '". In:', text)
    text = re.sub(r'"\s*,?\s+in:', '". In:', text)
    
    # 4. Seitenzahlen normalisieren: "S. XXX" -> "XXX"
    text = re.sub(r',\s+S\.\s+', ', ', text)
    
    # 5. Bindestrich zu Halbgeviertstrich in Seitenzahlen
    text = re.sub(r',\s+(\d+)-(\d+)\.', r', \1–\2.', text)
    
    # 6. Auflagen normalisieren
    text = re.sub(r'2\.\s+[Üü]berarbeitete\s+[Aa]uflage', '2., überarb. Aufl.', text)
    text = re.sub(r'2\.\s+[Aa]uflage\.', '2. Aufl.', text)
    
    # 7. Hochstellungen in Jahresangaben markieren für (TO CHECK)
    # ²2002 -> (2002): [Edition 2 - TO CHECK]
    text = re.sub(r'\(²(\d{4})\):', r'(\1): (TO CHECK - Edition 2)', text)
    text = re.sub(r'\(³(\d{4})\):', r'(\1): (TO CHECK - Edition 3)', text)
    
    if original != text:
        changes_log.append(f"Modified bibliography section")
    
    return text

# Verarbeite alle Dateien
processed_count = 0
for doc_path in docs_to_process:
    filepath = Path(doc_path)
    if filepath.exists():
        print(f"Verarbeite {doc_path}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Nur den Literaturbereich normalisieren
        if '## Literatur' in content:
            # Extrahiere Literaturabschnitt
            lit_start = content.find('## Literatur')
            next_section = content.find('\n!!! ', lit_start)
            if next_section == -1:
                next_section = len(content)
            
            lit_section = content[lit_start:next_section]
            lit_normalized = normalize_bibliography(lit_section)
            
            # Ersetze in Originaltext
            content_new = content[:lit_start] + lit_normalized + content[next_section:]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content_new)
            
            print(f"  ✓ {doc_path} erfolgreich normalisiert")
            processed_count += 1
        else:
            print(f"  ! Keine Literatursektion in {doc_path}")
    else:
        print(f"  ! Datei nicht gefunden: {doc_path}")

print(f"\n✅ Normalisierung abgeschlossen! {processed_count} Dateien verarbeitet.")
