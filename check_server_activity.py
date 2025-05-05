import os
import re
import datetime
import subprocess
import argparse
from pathlib import Path

# === CONFIGURATION ===
DEFAULT_LOG_DIR = "/path/to/your/server/logs"
LOGIN_PATTERN = re.compile(r"\[.*\]: (.+) joined the game")
MIN_UPTIME_DAYS = 2
MAX_LOGIN_AGE_DAYS = 7

def get_uptime_days():
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds / 86400

def get_log_files(log_dir):
    cutoff = datetime.datetime.now() - datetime.timedelta(days=MAX_LOGIN_AGE_DAYS)
    log_files = []

    for path in Path(log_dir).glob("*.log"):
        mod_time = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        if mod_time >= cutoff:
            log_files.append((path, mod_time.date()))

    return log_files

def parse_last_login(log_files):
    latest_login = None

    for path, file_date in log_files:
        with open(path, 'r', errors='ignore') as file:
            for line in file:
                match = LOGIN_PATTERN.search(line)
                if match:
                    time_match = re.match(r"\[(\d{2}):(\d{2}):(\d{2})\]", line)
                    if time_match:
                        hours, minutes, seconds = map(int, time_match.groups())
                        login_time = datetime.datetime.combine(
                            file_date, datetime.time(hours, minutes, seconds)
                        )
                        if latest_login is None or login_time > latest_login:
                            latest_login = login_time

    return latest_login

def shutdown_system(dry_run=False):
    uptime_days = get_uptime_days()
    if uptime_days < MIN_UPTIME_DAYS:
        print(f"Uptime is only {uptime_days:.2f} days. Required: {MIN_UPTIME_DAYS} days. Skipping shutdown.")
    elif dry_run:
        print("Dry run enabled. Would shut down the system now.")
    else:
        print("Shutting down the system.")
        subprocess.run(["sudo", "shutdown", "-h", "now"])

def main():
    parser = argparse.ArgumentParser(description="Shut down the server if no Minecraft logins in 7 days and uptime > 2 days.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the shutdown without actually doing it")
    parser.add_argument("--log-dir", default=DEFAULT_LOG_DIR, help="Path to the directory containing Minecraft logs")
    args = parser.parse_args()



    log_files = get_log_files(args.log_dir)
    if not log_files:
        raise RuntimeError("No log files found in the last 7 days. Cannot determine player activity.")

    last_login = parse_last_login(log_files)
    now = datetime.datetime.now()

    if not last_login:
        print("No logins found in the last 7 days.")
        shutdown_system(dry_run=args.dry_run)
        return

    delta = now - last_login
    print(f"Most recent login: {last_login.strftime('%Y-%m-%d %H:%M:%S')} ({delta.days} days ago)")

    if delta.days >= MAX_LOGIN_AGE_DAYS:
        shutdown_system(dry_run=args.dry_run)
    else:
        print("Login detected within the past 7 days. No shutdown.")

if __name__ == "__main__":
    main()
