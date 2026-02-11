# Quick Start Guide - Multilingual Features

## How to Test the Multilingual Features

### 1. Start the Application

```bash
cd /Users/ramonmariagallartescola/Documents/Projects/pindola_demo_flask
python run.py
```

Then open: http://127.0.0.1:5000

### 2. Change Language

1. Look for the **globe icon (🌐)** in the top-right corner of the navigation bar
2. Click it to reveal language options:
   - **English** - English interface
   - **Català** - Catalan (Balear) interface
3. Click your preferred language
4. The entire interface will update to show your selected language

### 3. Language-Specific Pages to Test

All pages are translated. Try visiting:

- **Login page** (`/login`)
  - Labels: "Username", "Password", "Remember me"
  - Buttons: "Log in", "Create account", "Forgot password?"

- **Registration page** (`/register`)
  - Labels: "Username", "Email", "Password", "Confirm password"
  - Button: "Create account"

- **Forgot Password page** (`/forgot`)
  - Title: "Forgot password"
  - Instructions: "Enter your email..."
  - Button: "Send reset link"

- **Dashboard** (`/dashboard`) - After login
  - Title: "Dashboard"
  - MFA status: "enabled" / "disabled"
  - User greeting: "Hi, [username]"

- **Settings Pages**
  - Change password
  - Activate MFA

### 4. Flash Messages in Both Languages

Try these actions to see translated flash messages:

1. **Registration Error (English)**
   - Register with same username twice
   - Message: "Username or email already exists."

2. **Registration Error (Catalan)**
   - Switch to Catalan
   - Register with same username again
   - Message: "El nom d'usuari o correu electrònic ja existeix."

3. **Login Error**
   - Try invalid credentials
   - Error appears in your selected language

4. **Success Messages**
   - Successful registration: "Account created. Please log in." (EN) or "Compte creat. Si us plau, inicia sessió." (CA)

## Translation Files Location

```
app/translations/
├── messages.pot                    # Translation template
├── en/LC_MESSAGES/
│   ├── messages.po                 # English translation source
│   └── messages.mo                 # Compiled English translations
└── ca/LC_MESSAGES/
    ├── messages.po                 # Catalan translation source
    └── messages.mo                 # Compiled Catalan translations
```

## Switching Language Programmatically

If you want to switch languages via URL, use the `/set-locale/<locale>` endpoint:

```
# Switch to English
http://127.0.0.1:5000/set-locale/en

# Switch to Catalan
http://127.0.0.1:5000/set-locale/ca
```

The app will redirect back to your previous page in the new language.

## Catalan Translations Included

✅ Page titles and headings
✅ Form labels
✅ Button labels
✅ Flash messages (success, error, info)
✅ Navigation menu items
✅ Field descriptions
✅ Error messages
✅ Dashboard status indicators

## Browser Language Detection

If no language is set:
1. The app checks your browser's language preference
2. If browser language is Catalan (ca), the app shows Catalan
3. If browser language is English or something else, the app shows English
4. Once you click the language switcher, your choice is saved for the session

## Configuration

The app is configured in `app/__init__.py`:

```python
app.config['BABEL_DEFAULT_LOCALE'] = 'en'  # Default language
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'app/translations'
```

Supported locales are defined by available translation files:
- `en` (English)
- `ca` (Catalan)

## Troubleshooting

**Language selector not appearing?**
- Clear your browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
- Make sure JavaScript is enabled for the dropdown menu

**Translations not showing?**
- Verify `.mo` files exist in `app/translations/en/LC_MESSAGES/` and `app/translations/ca/LC_MESSAGES/`
- Restart the Flask server

**Language reverts to English?**
- The session expires when you close the browser or restart server
- Click the language selector again to switch

## Adding More Languages

See [MULTILINGUAL.md](MULTILINGUAL.md) for detailed instructions on adding Spanish, French, or other languages.

## Files Modified for Multilingual Support

**Backend:**
- `app/__init__.py` - Babel initialization
- `app/routes.py` - Language switcher endpoint + translated messages
- `app/forms.py` - Translated form labels

**Frontend:**
- `app/templates/base.html` - Language selector button + get_locale()

**Configuration:**
- `requirements.txt` - Added Flask-Babel==4.0.0
- `babel.cfg` - Translation extraction configuration

**Translations:**
- `app/translations/messages.pot` - Translation template
- `app/translations/en/LC_MESSAGES/messages.po` - English catalog
- `app/translations/ca/LC_MESSAGES/messages.po` - Catalan catalog (70+ translations)
