# Running Thesis Generator: Local vs VPS

## Current Situation ⚠️

### If PC Shuts Down:
- ❌ **Process stops immediately**
- ❌ **Generation interrupted**
- ✅ **BUT**: Progress is saved to `thesis_state.json`
- ✅ **Can resume** from where it stopped

### Current State Saving:
The system already saves progress after each section:
- `thesis_state.json` - All completed sections
- `thesis/output/Thesis_*.md` - Generated content
- `thesis/reviews/` - Review reports
- `thesis/data/` - CSV datasets

**Resume capability**: ✅ YES (manually restart and it continues)

---

## Solution 1: Run on VPS with SSH (RECOMMENDED) ✅

### Setup:

1. **Upload code to VPS**:
   ```bash
   scp -r /home/gemtech/Desktop/map/thesis user@your-vps-ip:/home/user/
   ```

2. **SSH into VPS**:
   ```bash
   ssh user@your-vps-ip
   ```

3. **Run with `screen` or `tmux`** (keeps running after disconnect):

   **Using screen**:
   ```bash
   # Start screen session
   screen -S thesis
   
   # Run thesis generator
   cd /home/user/thesis
   python test_thesis.py
   
   # Detach: Press Ctrl+A then D
   # Now you can close SSH and shut down your PC!
   ```

   **To reconnect later**:
   ```bash
   ssh user@your-vps-ip
   screen -r thesis  # Reattach to session
   ```

   **Using tmux** (alternative):
   ```bash
   # Start tmux session
   tmux new -s thesis
   
   # Run thesis generator
   cd /home/user/thesis
   python test_thesis.py
   
   # Detach: Press Ctrl+B then D
   ```

   **To reconnect**:
   ```bash
   ssh user@your-vps-ip
   tmux attach -t thesis
   ```

### Benefits:
- ✅ **Runs continuously** even after SSH disconnect
- ✅ **Shut down your PC** - process continues on VPS
- ✅ **Reconnect anytime** to check progress
- ✅ **Email notifications** keep you updated

---

## Solution 2: Run as Background Service (ADVANCED)

### Create systemd service:

**File**: `/etc/systemd/system/thesis-generator.service`

```ini
[Unit]
Description=PhD Thesis Generator
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/user/thesis
ExecStart=/usr/bin/python3 /home/user/thesis/test_thesis.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Commands**:
```bash
# Enable and start service
sudo systemctl enable thesis-generator
sudo systemctl start thesis-generator

# Check status
sudo systemctl status thesis-generator

# View logs
sudo journalctl -u thesis-generator -f
```

### Benefits:
- ✅ **Auto-starts** on VPS reboot
- ✅ **Auto-restarts** if crashes
- ✅ **Runs in background**

---

## Solution 3: Add Resume Capability (IMPLEMENT THIS)

### Current Limitation:
If interrupted, you must manually restart from beginning (but it skips completed sections).

### Better Solution:
Add a `--resume` flag to continue from last checkpoint.

**I can implement this for you**:
```python
# In test_thesis.py
if __name__ == "__main__":
    import sys
    
    resume = "--resume" in sys.argv
    
    if resume:
        print("📂 Resuming from last checkpoint...")
        # Load state and continue
    else:
        print("🆕 Starting new thesis generation...")
```

---

## Recommended Workflow

### For VPS:

1. **Upload to VPS**:
   ```bash
   scp -r /home/gemtech/Desktop/map/thesis user@vps-ip:/home/user/
   ```

2. **SSH and start screen**:
   ```bash
   ssh user@vps-ip
   screen -S thesis
   cd /home/user/thesis
   python test_thesis.py
   ```

3. **Detach** (Ctrl+A, D) and close SSH

4. **Shut down your PC** - thesis continues generating!

5. **Check progress**:
   - Email notifications arrive as chapters complete
   - Or reconnect: `ssh user@vps-ip && screen -r thesis`

---

## What Happens If Interrupted?

### Current Behavior:
```
Chapter 1: ✅ Complete (saved to state)
Chapter 2: ✅ Complete (saved to state)
Chapter 3: ⏸️ Section 3.4 in progress...
[PC SHUTS DOWN]

On restart:
Chapter 1: ✅ Skipped (already in state)
Chapter 2: ✅ Skipped (already in state)
Chapter 3: 🔄 Continues from Section 3.4
```

### State File (`thesis_state.json`):
```json
{
  "CHAPTER ONE": {
    "1.1 Setting the scene": "content...",
    "1.2 Background": "content..."
  },
  "CHAPTER TWO": {
    "2.1 Introduction": "content...",
    "2.2 Framework": "content..."
  }
}
```

**Resume**: Just run `python test_thesis.py` again - it skips completed sections!

---

## Time Estimates

**Full thesis generation**: 4-6 hours (depending on API speed)

**With VPS + screen**:
- Start generation
- Detach and close laptop
- Go to sleep
- Wake up to completed thesis + email notifications! ✅

---

## Quick Setup Guide

### 1. Install screen on VPS:
```bash
sudo apt update
sudo apt install screen
```

### 2. Upload thesis code:
```bash
scp -r /home/gemtech/Desktop/map/thesis user@vps-ip:/home/user/
```

### 3. Run in screen:
```bash
ssh user@vps-ip
screen -S thesis
cd /home/user/thesis
python test_thesis.py
# Press Ctrl+A then D to detach
```

### 4. Close SSH and shut down PC ✅

### 5. Check later:
```bash
ssh user@vps-ip
screen -r thesis  # See live progress
```

---

## Do You Want Me To:

1. ✅ **Add `--resume` flag** for better restart handling?
2. ✅ **Create VPS setup script** for easy deployment?
3. ✅ **Add progress logging** to file (so you can check without SSH)?

Let me know!
