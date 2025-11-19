# 🚀 Deploy to Your VPS (AlmaLinux)

This guide will help you deploy your textbook generator to your VPS so it can run 24/7.

## 1. Connect to Your VPS

Open your terminal and run:

```bash
ssh root@69.57.163.159
```

When asked for a password, copy and paste this (it won't show when you type):
`ceG6i8VmP5o6QMT1k4`

> **Note:** If it asks "Are you sure you want to continue connecting?", type `yes` and press Enter.

---

## 2. One-Step Setup

Once you are logged in, copy and paste this **entire block** of code and press Enter:

```bash
# Install Git
dnf install -y git

# Clone your repository
git clone https://github.com/Researchwriting/book.git
cd book

# Run the setup script
chmod +x setup_vps.sh
./setup_vps.sh
```

This script will automatically:
- Update your system
- Install Python 3.9+ and tools
- Install `tmux` (to keep app running)
- Set up the virtual environment
- Install all dependencies

---

## 3. Add Your Keys

Since we didn't upload your keys to GitHub (for security), you need to add them now.

1. **Edit the config file:**
   ```bash
   nano src/config.py
   ```

2. **Find the line:** `API_KEY: str = "YOUR_API_KEY_HERE"`
3. **Replace** `YOUR_API_KEY_HERE` with your actual DeepSeek API key.
4. **Save and Exit:** Press `Ctrl+O`, `Enter`, then `Ctrl+X`.

---

## 4. Run the App (24/7 Mode)

To keep the app running even after you close your computer, we use `tmux`.

1. **Start a new session:**
   ```bash
   tmux new -s generator
   ```

2. **Run the app:**
   ```bash
   python3 -m src.interactive_main
   ```

3. **Detach (Leave it running):**
   - Press `Ctrl+B`, then release both and press `D`.
   - You will return to the main shell, but the app is still running in the background!

---

## 5. Check on Your App Later

To see how it's doing:

```bash
tmux attach -t generator
```

To detach again: `Ctrl+B`, then `D`.

---

## 📄 Download Your Files

When the book is done, you can download the files to your computer:

**On your LOCAL computer (not the VPS):**
```bash
scp -r root@69.57.163.159:/root/book/output ./vps_output
```
This will copy the `output` folder from the VPS to a `vps_output` folder on your desktop.
