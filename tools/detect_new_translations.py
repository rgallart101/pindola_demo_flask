#!/usr/bin/env python3
"""Detect new/untranslated strings after extracting messages.pot.

This script extracts translatable strings into `app/translations/messages.pot`
then scans each locale's `messages.po` for untranslated entries and prints a
summary and examples.
"""
import os
import subprocess
import sys
from babel.messages.pofile import read_po

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TRANS_DIR = os.path.join(ROOT, 'app', 'translations')
POT_PATH = os.path.join(TRANS_DIR, 'messages.pot')

# Locales to skip when checking for untranslated strings (comma-separated)
# By default skip 'en' (source language) so detection only flags real missing
# translations. You can override with environment variable DETECT_SKIP_LOCALES.
SKIP_LOCALES = [l.strip() for l in os.getenv('DETECT_SKIP_LOCALES', 'en').split(',') if l.strip()]


def run_extract():
    cmd = [sys.executable, '-m', 'babel.messages.frontend', 'extract', '-F', 'babel.cfg', '-o', POT_PATH, '.']
    print('Running:', ' '.join(cmd))
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        print('Error: pybabel extract failed', file=sys.stderr)
        sys.exit(res.returncode)


def scan_locales():
    if not os.path.isdir(TRANS_DIR):
        print('No translations directory:', TRANS_DIR)
        return 1

    locales = [d for d in os.listdir(TRANS_DIR) if os.path.isdir(os.path.join(TRANS_DIR, d))]
    if not locales:
        print('No locale catalogs found in', TRANS_DIR)
        return 1

    any_untranslated = False
    for loc in sorted(locales):
        if loc in SKIP_LOCALES:
            print(f'{loc}: skipped (in SKIP_LOCALES)')
            continue
        po_path = os.path.join(TRANS_DIR, loc, 'LC_MESSAGES', 'messages.po')
        if not os.path.exists(po_path):
            print(f'  - {loc}: missing {po_path}')
            continue

        with open(po_path, 'rb') as fh:
            catalog = read_po(fh)

        untranslated = []
        for message in catalog:
            # message.id may be a tuple for plurals; handle simple case
            mid = message.id
            if not mid:
                continue
            # Skip header
            if mid == '':
                continue
            if not message.string:
                untranslated.append(str(mid))

        print(f'{loc}: {len(untranslated)} untranslated entries')
        if untranslated:
            any_untranslated = True
            print('  Examples:')
            for msg in untranslated[:20]:
                print('   -', msg)

    return 1 if any_untranslated else 0


def main():
    run_extract()
    rc = scan_locales()
    if rc == 0:
        print('\nNo new untranslated strings detected.')
    else:
        print('\nSome untranslated strings were detected. Run `make compile-language` or edit the .po files to translate.')
    sys.exit(rc)


if __name__ == '__main__':
    main()
