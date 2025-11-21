# Installation and Setup Instructions

## 1. Install python-docx for DOCX Conversion

Since your system is externally managed, you need to install python-docx using one of these methods:

### Option A: Using apt (Recommended for system-wide)
```bash
sudo apt install python3-docx
```

### Option B: Using pipx (For isolated installation)
```bash
pipx install python-docx
```

### Option C: Using virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install python-docx
```

## 2. Configure Email Notifications

Edit `/home/gemtech/Desktop/map/thesis/src/config.py` and set:

```python
EMAIL_ENABLED = True
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # See below
RECIPIENT_EMAIL = "recipient@email.com"
```

### How to Get Gmail App Password:
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification if not already enabled
3. Go to "App passwords"
4. Generate a new app password for "Mail"
5. Copy the 16-character password
6. Use this password in EMAIL_PASSWORD (not your regular Gmail password)

## 3. Features Implemented

✅ **DOCX Formatter** (`docx_formatter.py`)
- Times New Roman font
- 1.5 line spacing
- Justified text
- H1: Centered, UPPERCASE, Bold, 14pt
- H2: Bold, 13pt
- H3: Bold, Italic, 12pt
- Tables and figures properly formatted

✅ **Email Notifier** (`email_notifier.py`)
- Sends chapter completion emails with MD and DOCX attachments
- Sends peer review reports
- Gmail SMTP integration

✅ **Integration Ready**
- Code is ready to integrate into `thesis_main.py`
- Just need to install python-docx and configure email

## 4. Next Steps

After installing python-docx and configuring email:
1. Run thesis generation
2. Each chapter will be emailed as it completes
3. Review reports will be emailed
4. DOCX files will be generated with proper formatting
