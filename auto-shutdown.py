import os
import re
import datetime
import subprocess
import argparse

# === CONFIGURATION ===
DEFAULT_LOG_FILE = "/path/to/your/server/logs/latest.log"
LOGIN_PATTERN = re.compile(r"\[.*\]: (.+) joined the game")
MIN_UPTIME_DAYS = 2
MAX_LOGIN_AGE_DAYS = 7

# === FUNCTIONS ===

def get_uptime_days():
    """Return the system uptime in days."""
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds / 86400  # seconds in a day

def last_login_time(log_file):
    """Parse the log and return the datetime of the last login."""
    last_login = None
    if not os.path.exists(log_file):
        print(f"Log file not found: {log_file}")
        return None

    with open(log_file, 'r') as file:
        for line in file:
            match = LOGIN_PATTERN.search(line)
            if match:
                time_match = re.match(r"\[(\d{2}):(\d{2}):(\d{2})\]", line)
                if time_match:
                    hours, minutes, seconds = map(int, time_match.groups())
                    log_datetime = datetime.datetime.combine(
                        datetime.date.today(), datetime.time(hours, minutes, seconds)
                    )
                    last_login = log_datetime
    return last_login

def shutdown_system(dry_run=False):
    """Shutdown the system, or simulate shutdown if dry_run is True."""
    if dry_run:
        print("Dry run enabled. Would shut down the system now.")
    else:
        print("Shutting down the system.")
        subprocess.run(["sudo", "shutdown", "-h", "now"])

def main():
    parser = argparse.ArgumentParser(description="Shutdown server if no Minecraft logins in 7 days and uptime exceeds threshold.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the shutdown without taking action")
    parser.add_argument("--log-file", default=DEFAULT_LOG_FILE, help="Path to the Minecraft latest.log file")

    args = parser.parse_args()

    uptime_days = get_uptime_days()
    if uptime_days < MIN_UPTIME_DAYS:
        print(f"Uptime is only {uptime_days:.2f} days. Minimum required is {MIN_UPTIME_DAYS} days. Skipping shutdown.")
        return

    login_time = last_login_time(args.log_file)
    now = datetime.datetime.now()

    if not login_time:
        print("No login entries found.")
        should_shutdown = True
    else:
        delta_days = (now - login_time).days
        print(f"Last login was {delta_days} day(s) ago.")
        should_shutdown = delta_days >= MAX_LOGIN_AGE_DAYS

    if should_shutdown:
        shutdown_system(dry_run=args.dry_run)
    else:
        print("Login detected within the past 7 days. No shutdown.")

if __name__ == "__main__":
    main()
