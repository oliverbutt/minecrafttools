# 🛡️ Minecraft Server Auto-Shutdown Script

This project provides a Python script that automatically shuts down an Ubuntu-based Minecraft server if:

- No players have logged in within the last **7 days**
- The server's uptime is greater than **2 days**
- (Optional) It can be run in **dry-run** mode for safe testing

This is useful for saving energy and resources on self-hosted or cloud-based servers that aren't used frequently.

---

## 📁 Contents

- `check_server_activity.py` – the main Python script
- `README.md` – project documentation

---

## 🚀 Features

- Parses `latest.log` to find the most recent player login
- Uses `/proc/uptime` to determine how long the system has been running
- Shuts down the *entire server* if conditions are met
- Supports `--dry-run` mode for safe testing
- Configurable Minecraft log file path

---

## ⚙️ Requirements

- Python 3.x
- Ubuntu or other Linux system with:
  - access to `/proc/uptime`
  - `sudo` permissions for shutdown

---

## 🛠️ Installation

1. Clone or download this repository
2. Edit the script:
   - Set the default path to your `latest.log`
   - (Optional) Change the minimum uptime or max login age constants
3. Make the script executable:

```bash
chmod +x check_server_activity.py
```

---

## 🔧 Usage

### Basic command

```bash
sudo ./check_server_activity.py --log-file /path/to/latest.log
```

### With dry run (no actual shutdown)

```bash
./check_server_activity.py --log-file /path/to/latest.log --dry-run
```

---

## 🕒 Automate with Cron

To check daily at 3:00 AM:

```bash
sudo crontab -e
```

Add the following line:

```cron
0 3 * * * /path/to/check_server_activity.py --log-file /path/to/latest.log >> /var/log/mc_shutdown.log 2>&1
```

---

## ✅ Safe Testing

Before enabling auto-shutdown, run in dry-run mode for a few days:

```cron
0 3 * * * /path/to/check_server_activity.py --log-file /path/to/latest.log --dry-run >> /var/log/mc_shutdown.log 2>&1
```

Then monitor `/var/log/mc_shutdown.log` for output.

---

## 📌 Customization

You can change constants in the script:

```python
MIN_UPTIME_DAYS = 2
MAX_LOGIN_AGE_DAYS = 7
```

---

## 📝 License

This project is open source and free to use under the MIT License.
