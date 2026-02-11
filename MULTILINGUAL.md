# Multilingual Support Guide

Your Flask application now supports English and Catalan languages! Here's how the multilingual system works:

## Features Implemented

✅ **Flask-Babel Integration** - Automatic language detection and translation management
✅ **English & Catalan Support** - Full UI translation for both languages
✅ **Language Switcher** - Globe icon (🌐) in the top navigation bar to switch languages
✅ **Session Persistence** - Language preference is saved in the user's session
✅ **Automatic Locale Selection** - Falls back to browser language preference if no language is selected

## How to Use

### For End Users

1. Look for the globe icon (🌐) in the top-right corner of the navigation bar
2. Click it to reveal language options:
   - **English** - Switch to English
   - **Català** - Switch to Catalan
3. The selected language persists for your session

The application will show all UI elements in your selected language:
- Form labels
- Buttons and links
- Flash messages
- Page titles
- Navigation menu

### For Developers

#### Adding New Translatable Strings

**In Python files:**
```python
from flask_babel import gettext as _

# For immediate translation
flash(_("Your message here"), "success")
```

**In Templates (Jinja2):**
```html
<h1>{{ _("Page Title") }}</h1>
<a href="#">{{ _("Link text") }}</a>
<p>{{ _("Descriptive text with %(var)s", var=value) }}</p>
```

**In Form Definitions:**
```python
from flask_babel import lazy_gettext as _l

class MyForm(FlaskForm):
    field = StringField(_l("Field Label"))
```

#### Updating Translations

1. **Extract new strings:**
   ```bash
   pybabel extract -F babel.cfg -o app/translations/messages.pot .
   ```

2. **Update translation catalogs:**
   ```bash
   pybabel update -i app/translations/messages.pot -d app/translations -l en
   pybabel update -i app/translations/messages.pot -d app/translations -l ca
   ```

3. **Edit translation files:**
   - English: `app/translations/en/LC_MESSAGES/messages.po`
   - Catalan: `app/translations/ca/LC_MESSAGES/messages.po`

   Find the `msgid "your string"` and add the translation to `msgstr "your translation"`

4. **Compile translations:**
   ```bash
   pybabel compile -d app/translations
   ```

## Project Structure

```
app/
├── translations/
│   ├── messages.pot           # Translation template
│   ├── en/LC_MESSAGES/
│   │   ├── messages.po        # English translations (empty - uses source strings)
│   │   └── messages.mo        # Compiled English translations
│   └── ca/LC_MESSAGES/
│       ├── messages.po        # Catalan translations
│       └── messages.mo        # Compiled Catalan translations
├── __init__.py                # Babel initialization
├── routes.py                  # Language switcher route + translated flash messages
├── forms.py                   # Translated form labels
└── templates/
    └── base.html              # Locale selector in navbar
```

## Configuration

The multilingual setup is configured in `app/__init__.py`:

- **Default Locale:** English (en)
- **Supported Locales:** English (en), Catalan (ca)
- **Translation Directories:** `app/translations/`
- **Locale Selection Logic:** Session → Browser preference → Default (en)

## Current Translations

The following items have been translated to Catalan:

- All page titles and headings
- Navigation menu items
- Button labels
- Form field labels
- Flash messages (success, error, info)
- Dashboard status indicators

### Translation Statistics

- **Total Strings:** 60+
- **Languages:** 2 (English + Catalan)
- **Translation Coverage:** 100% for UI elements

## Language Switcher Route

The language can be changed via the `/set-locale/<locale>` route:

```
GET /set-locale/en   # Switch to English
GET /set-locale/ca   # Switch to Catalan
```

The user is redirected back to their previous page after changing language.

## Notes

- Language preferences are stored in **session** (not database)
- Session data persists while the browser is open
- When the session expires, browser locale preferences are used
- English translations use source strings (no translation file needed)
- To add a new language, repeat the extraction/initialization/translation/compilation process

## Troubleshooting

**Translation not working?**
- Ensure `.mo` files are compiled: `pybabel compile -d app/translations`
- Check that `BABEL_TRANSLATION_DIRECTORIES` is set in config
- Verify locale code matches (en, ca)

**Form labels not translating?**
- Make sure to use `lazy_gettext` (_l) for form field labels
- Don't forget the function call parentheses: `_l("text")` not `_l"text"`

**Missing translations in navbar?**
- Ensure `get_locale()` is available in templates via `app.jinja_env.globals.update()`
- Check that the language switcher button passes the correct locale codes

## Future Enhancements

Possible improvements:
- Add more languages (Spanish, French, German, etc.)
- Store language preference in user database (for persistent preference)
- Add language selection in account settings
- Implement RTL (right-to-left) language support if needed
- Add language name localization (show "English" in English, "Anglès" in Catalan)
