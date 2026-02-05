import os
import schedule
import time
import threading
import sqlite3
from datetime import datetime

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Initialize database
db_path = os.path.join("logs", "user_logs.db")

def init_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS keyboard_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS app_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT,
            window_title TEXT,
            start_time TEXT,
            end_time TEXT,
            duration REAL
        );
        CREATE TABLE IF NOT EXISTS idle_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idle_time REAL NOT NULL,
            timestamp TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS mouse_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            button TEXT NOT NULL,
            pressed BOOLEAN NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS login_logout (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS employee_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            session_date TEXT NOT NULL,
            login_time TEXT,
            logout_time TEXT
        );
        CREATE TABLE IF NOT EXISTS daily_productivity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            date TEXT NOT NULL,
            productivity_score REAL NOT NULL,
            active_time REAL,
            total_time REAL,
            timestamp TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS screenshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

if not os.path.exists(db_path):
    print("[INFO] Initializing database...")
    init_database()
    print("[INFO] Database tables created successfully.")

# Import monitoring modules
from modules.keyboard_logger import start_keyboard_logger
from modules.mouse_tracker import start_mouse_tracker
from modules.app_usage_tracker import start_app_usage_tracker
from modules.idle_time_detecter import start_idle_monitor
from modules.login_logout_tracker import log_event
# If you have advanced session tracking, you could also:
# from modules.login_logout_tracker import start_login_logout_tracker

from reports.confiq import START_TIME, END_TIME, EMPLOYEE_NAME, SCREENSHOT_INTERVAL, ENABLE_SCREENSHOTS

# Global thread references (optional)
threads = []

# Event used to signal trackers to stop
stop_event = threading.Event()

def run_all_modules(stop_event):
    """
    Starts all monitoring modules in background daemon threads.
    Logs login event once at start. Trackers accept a stop_event to exit cleanly.
    """
    log_event('login')
    
    # Store employee session
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO employee_sessions (employee_name, session_date, login_time) VALUES (?, ?, ?)',
            (EMPLOYEE_NAME, datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[WARN] Failed to store employee session: {e}")
    global threads
    threads = []
    
    # Start modules and pass stop_event to each starter
    kb = start_keyboard_logger(stop_event=stop_event)
    ms = start_mouse_tracker(stop_event=stop_event)
    app = start_app_usage_tracker(stop_event=stop_event)
    idle = start_idle_monitor(stop_event=stop_event)
    
    # Start screenshot capture if enabled
    if ENABLE_SCREENSHOTS:
        from modules.screenshot_capture import start_screenshot_capture
        screenshot = start_screenshot_capture(interval=SCREENSHOT_INTERVAL, stop_event=stop_event)
        threads.append(screenshot)

    # Filter out None values (failed starts) and store valid threads/listeners
    active_trackers = [t for t in [kb, ms, app, idle] if t is not None]
    threads.extend(active_trackers)
    
    if not threads:
        print("[WARN] No trackers could be started!")
        return False
        
    print("[INFO] Started {} trackers successfully.".format(len(threads)))
    return True



def wait_until_end_time_or_interrupt(stop_event):
    """
    Runs scheduler, waits until END_TIME or until user interrupts with Ctrl+C.
    When END_TIME is reached, stop trackers and exit.
    """
    print(f"[INFO] Monitoring will stop at {END_TIME.strftime('%H:%M:%S')} or on Ctrl+C.")
    try:
        while True:
            now = datetime.now().time()
            if now >= END_TIME:
                print(f"\n[INFO] End time {END_TIME.strftime('%H:%M:%S')} reached.")
                break
            schedule.run_pending()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped by user (Ctrl+C).")
    finally:
        print("[INFO] Stopping all trackers...")
        stop_event.set()
        
        # Log logout event and update session
        print("[INFO] Logging logout event...")
        log_event('logout')
        
        try:
            conn = sqlite3.connect(db_path, timeout=10)
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE employee_sessions SET logout_time = ? WHERE session_date = ? AND employee_name = ?',
                (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d'), EMPLOYEE_NAME)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[WARN] Failed to update logout time: {e}")
        
        # Give threads time to stop gracefully
        time.sleep(2)
        
        # Force stop any remaining threads
        for thread in threads:
            try:
                if hasattr(thread, 'is_alive') and thread.is_alive():
                    print(f"[INFO] Waiting for thread to stop: {thread}")
                    thread.join(timeout=2.0)
            except Exception as e:
                print(f"[WARN] Error stopping thread: {e}")
                
    print("[INFO] All monitoring processes stopped.")

if __name__ == "__main__":
    print("[INFO] Starting User Activity Logger...")
    
    # Delete old screenshots
    if ENABLE_SCREENSHOTS:
        from modules.screenshot_capture import delete_old_screenshots
        delete_old_screenshots()

    # Archive previous logs and clear database for fresh session
    try:
        archive_dir = os.path.join('logs', 'archive')
        os.makedirs(archive_dir, exist_ok=True)
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_name = f"user_logs_{timestamp}.db"
            archive_path = os.path.join(archive_dir, archive_name)
            try:
                if not os.path.exists(archive_path):
                    import shutil
                    shutil.copy2(db_path, archive_path)
                    print(f"[INFO] Archived previous DB to {archive_path}")
            except Exception as e:
                print(f"[WARN] Failed to archive DB: {e}")
            
            # Recreate database with all tables
            try:
                os.remove(db_path)
                init_database()
                print(f"[INFO] Database recreated for new session")
            except Exception as e:
                print(f"[WARN] Failed to recreate DB: {e}")

    except Exception as e:
        print(f"[WARN] Error while preparing logs archive: {e}")

    # Wait until START_TIME before starting trackers
    print(f"[INFO] Waiting for START_TIME {START_TIME.strftime('%H:%M:%S')}...")
    while True:
        if datetime.now().time() >= START_TIME:
            break
        time.sleep(5)

    # Start trackers
    run_all_modules(stop_event)

    print("[INFO] Monitoring started. Press Ctrl+C to stop.")
    wait_until_end_time_or_interrupt(stop_event)

    print("[INFO] Monitoring finished. Data saved to database.")
    print("[INFO] View dashboard at: http://localhost:5173")
