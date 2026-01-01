"""
Database Verification Utility

A utility script to inspect the SQLite database used by the video learning platform.
Displays video progress records, user settings, and database structure information
in a formatted, human-readable way.

This tool is helpful for:
- Debugging database connectivity issues
- Verifying that progress data is being saved correctly
- Inspecting user settings and their values
- Understanding the database schema and content

Usage: python check_database.py
"""

import sqlite3
from datetime import datetime

def check_database():
    """
    Comprehensive database verification and content inspection.
    
    Connects to the course_progress.db database and displays:
    1. Table structure verification
    2. Video progress records with formatting
    3. User settings and their current values
    4. Database statistics and status
    
    Provides a formatted table view of all saved progress data
    including video paths, watch percentages, timestamps, and completion status.
    """
    print("\n===== DATABASE VERIFICATION =====\n")
    
    try:
        # Establish database connection
        conn = sqlite3.connect('course_progress.db')
        c = conn.cursor()
        
        # Verify video_progress table exists and get schema
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='video_progress'")
        table_exists = c.fetchone()
        
        if table_exists:
            print("Table 'video_progress' exists")
            
            # Retrieve all video progress records ordered by most recent
            c.execute("SELECT * FROM video_progress ORDER BY last_watched DESC")
            records = c.fetchall()
            
            print(f"\nFound {len(records)} saved video progress record(s)\n")
            
            if records:
                # Display records in formatted table
                print("-" * 100)
                print(f"{'Video Path':<40} | {'Progress':<10} | {'Time':<12} | {'Speed':<8} | {'Last Watched':<20}")
                print("-" * 100)
                
                for record in records:
                    # Extract record fields
                    video_path = record[0]
                    chapter = record[1]
                    video_name = record[2]
                    current_time = record[3]
                    duration = record[4]
                    playback_speed = record[5]
                    watch_percentage = record[6]
                    last_watched = record[7]
                    completed = record[8]
                    
                    # Format display values
                    path_display = video_path[:37] + "..." if len(video_path) > 40 else video_path
                    time_display = f"{int(current_time)}s / {int(duration)}s"
                    progress_display = f"{watch_percentage:.1f}%"
                    
                    # Add completion indicator
                    if completed:
                        progress_display += " (Completed)"
                    
                    # Display formatted row
                    print(f"{path_display:<40} | {progress_display:<10} | {time_display:<12} | {playback_speed}x{' ':<6} | {last_watched}")
                
                print("-" * 100)
                print("\nDatabase is working correctly. Data will persist across sessions.\n")
            else:
                print("No records found yet. Start watching videos to save progress.\n")
                
        # Check user_settings table
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_settings'")
        settings_table_exists = c.fetchone()
        
        if settings_table_exists:
            print("Table 'user_settings' exists")
            
            # Retrieve all user settings
            c.execute("SELECT setting_key, setting_value FROM user_settings")
            settings = c.fetchall()
            
            if settings:
                print(f"\nUser Settings ({len(settings)} entries):")
                print("-" * 40)
                for key, value in settings:
                    print(f"{key:<25} | {value}")
                print("-" * 40)
            else:
                print("No user settings found.")
        else:
            print("Table 'user_settings' does not exist")
            print("The settings table will be created when you first run the app.\n")
            
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {e}\n")
        print("Make sure course_progress.db exists and is accessible.")
        print("Run the Flask app first to initialize the database.\n")

if __name__ == "__main__":
    """
    Entry point for the database verification utility.
    
    Run this script directly to inspect the current state of the database:
    $ python check_database.py
    """
    check_database()
