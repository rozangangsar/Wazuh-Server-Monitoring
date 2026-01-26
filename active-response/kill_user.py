#!/usr/bin/env python3
import sys
import json
import time
import subprocess

LOG_FILE = "/var/ossec/logs/active-responses.log"
WHITELIST = ['root', 'wazuh', 'daemon']

# ABSOLUTE PATHS
SUDO = "/usr/bin/sudo"
LOGINCTL = "/usr/bin/loginctl"
PKILL = "/usr/bin/pkill"

def write_log(msg):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")
            f.flush()
    except:
        pass

def kick_user(username):
    """Kick user via loginctl"""
    try:
        cmd = [SUDO, LOGINCTL, "terminate-user", username]
        write_log(f"→ CMD: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )

        write_log(f"RETURN: {result.returncode}")

        if result.stdout:
            write_log(f"STDOUT: {result.stdout.strip()}")
        if result.stderr:
            write_log(f"STDERR: {result.stderr.strip()}")

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        write_log(f"✗ TIMEOUT")
        return False
    except Exception as e:
        write_log(f"✗ Exception: {e}")
        return False

def kill_ssh_backup(username):
    """Backup: kill SSH"""
    try:
        cmd = [SUDO, PKILL, "-9", "-f", f"sshd: {username}"]
        write_log(f"→ PKILL CMD: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )

        write_log(f"PKILL return: {result.returncode}")
        return True

    except Exception as e:
        write_log(f"✗ PKILL error: {e}")
        return False

def main():
    try:
        write_log("=" * 60)
        write_log("🔥 SCRIPT START")

        input_data = sys.stdin.read()

        if not input_data:
            write_log("✗ No input")
            sys.exit(1)

        data = json.loads(input_data)

        # Extract user
        user_target = None
        try:
            alert = data.get('parameters', {}).get('alert', {})
            audit = alert.get('syscheck', {}).get('audit', {})
            user_target = audit.get('login_user', {}).get('name')

            if not user_target:
                user_target = audit.get('effective_user', {}).get('name')
            if not user_target:
                user_target = audit.get('user', {}).get('name')
        except Exception as e:
            write_log(f"✗ Parse: {e}")

        if not user_target:
            write_log("✗ No target")
            sys.exit(0)

        write_log(f"🎯 TARGET: {user_target}")

        if user_target in WHITELIST:
            write_log(f"SKIP: whitelisted")
            sys.exit(0)

        # KICK
        write_log(f"⚡ KICKING {user_target}...")

        success = kick_user(user_target)

        if success:
            write_log(f"✅ KICK SUCCESS!")
        else:
            write_log("→ Trying backup...")
            kill_ssh_backup(user_target)

        write_log("=" * 60)

    except Exception as e:
        write_log(f"💥 ERROR: {e}")
        import traceback
        write_log(traceback.format_exc())

if __name__ == "__main__":
    main()
