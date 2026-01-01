"""
Flask Video Learning Platform

A comprehensive video course management system that provides:
- Video progress tracking and analytics
- User settings management
- Chapter-based course organization
- Auto-resume functionality
- Responsive web interface

Author: Course Platform Team
Version: 2.0
"""

import os
import sqlite3
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime

app = Flask(__name__)

def init_db():
    """
    Initialize the SQLite database with required tables.
    
    Creates two main tables:
    1. video_progress: Stores individual video watching progress
    2. user_settings: Stores user preferences and configuration
    
    Also inserts default settings if they don't exist.
    """
    conn = sqlite3.connect('course_progress.db')
    c = conn.cursor()
    
    # Create video progress tracking table
    c.execute('''CREATE TABLE IF NOT EXISTS video_progress
                 (video_path TEXT PRIMARY KEY,
                  chapter TEXT,
                  video_name TEXT,
                  current_time REAL,
                  duration REAL,
                  playback_speed REAL DEFAULT 1.0,
                  watch_percentage REAL DEFAULT 0,
                  last_watched TIMESTAMP,
                  completed INTEGER DEFAULT 0)''')
    
    # Create user settings table
    c.execute('''CREATE TABLE IF NOT EXISTS user_settings
                 (setting_key TEXT PRIMARY KEY,
                  setting_value TEXT)''')
    
    # Insert default settings if they don't already exist
    default_settings = [
        ('max_playback_speed', '2.0'),
        ('auto_resume', 'true'),
        ('save_last_chapter', 'true'),
        ('last_chapter', ''),
        ('theme', 'dark'),
        ('current_playback_speed', '1')
    ]
    
    for key, value in default_settings:
        c.execute("INSERT OR IGNORE INTO user_settings (setting_key, setting_value) VALUES (?, ?)", (key, value))
    
    conn.commit()
    conn.close()

# Initialize database on application startup
init_db()

@app.route('/')
def index():
    """
    Main route that serves the chapters dashboard.
    
    Scans the static directory for course folders and organizes
    videos and PDF documents by chapter.
    
    Returns:
        Rendered chapters.html template with course structure
    """
    base_path = os.path.join('static')
    days = {}

    # Scan directory structure for course content
    for day_folder in sorted(os.listdir(base_path)):
        day_path = os.path.join(base_path, day_folder)
        if os.path.isdir(day_path):
            videos = []
            pdfs = []
            # Process each file in the chapter directory
            for file_name in sorted(os.listdir(day_path)):
                # Check for video files with supported formats
                if file_name.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                    videos.append(file_name)
                # Check for document files with supported formats
                elif file_name.endswith(('.pdf', '.docx', '.doc', '.txt')):
                    pdfs.append(file_name)
            
            # Store chapter data with videos and documents
            days[day_folder] = {'videos': videos, 'pdfs': pdfs}

    return render_template('chapters.html', days=days)

@app.route('/player/<path:chapter>')
def player(chapter):
    """
    Video player route for a specific chapter.
    
    Args:
        chapter (str): The chapter/folder name to display
        
    Returns:
        Rendered player.html template with chapter content
        or redirect to index if chapter doesn't exist
    """
    base_path = os.path.join('static')
    
    # Validate that the requested chapter exists
    chapter_path = os.path.join(base_path, chapter)
    if not os.path.isdir(chapter_path):
        return redirect(url_for('index'))
    
    videos = []
    pdfs = []
    
    # Scan chapter directory for media and document files
    for file_name in sorted(os.listdir(chapter_path)):
        if file_name.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
            videos.append(file_name)
        elif file_name.endswith(('.pdf', '.docx', '.doc', '.txt')):
            pdfs.append(file_name)
    
    # Prepare chapter data for template
    chapter_data = {chapter: {'videos': videos, 'pdfs': pdfs}}
    
    # Save last accessed chapter if the feature is enabled
    try:
        conn = sqlite3.connect('course_progress.db')
        c = conn.cursor()
        c.execute("UPDATE user_settings SET setting_value = ? WHERE setting_key = 'last_chapter'", (chapter,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Could not save last chapter: {e}")
    
    return render_template('player.html', days=chapter_data, current_chapter=chapter)

@app.route('/api/save-progress', methods=['POST'])
def save_progress():
    """
    API endpoint to save video watching progress.
    
    Accepts JSON data with video information and current progress,
    then updates the database with the latest viewing state.
    
    Expected JSON fields:
        - video_path: Unique path to the video file
        - chapter: Chapter name containing the video
        - video_name: Name of the video file
        - current_time: Current playback position in seconds
        - duration: Total video duration in seconds
        - playback_speed: Current playback speed multiplier
    
    Returns:
        JSON response with success status
    """
    data = request.json
    print(f"[SAVE PROGRESS] Received data: {data}")
    
    # Extract video progress data from request
    video_path = data.get('video_path')
    chapter = data.get('chapter')
    video_name = data.get('video_name')
    current_time = data.get('current_time', 0)
    duration = data.get('duration', 0)
    playback_speed = data.get('playback_speed', 1.0)
    
    # Calculate watch percentage and completion status
    watch_percentage = (current_time / duration * 100) if duration > 0 else 0
    completed = 1 if watch_percentage >= 90 else 0  # Mark as completed at 90% watched
    
    # Generate timestamp for the progress record
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[SAVE PROGRESS] Saving - Path: {video_path}, Time: {current_time:.2f}s, Duration: {duration:.2f}s, Progress: {watch_percentage:.2f}%, Speed: {playback_speed}x, Timestamp: {timestamp}")
    
    try:
        # Connect to database and save progress
        conn = sqlite3.connect('course_progress.db')
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO video_progress 
                     (video_path, chapter, video_name, current_time, duration, playback_speed, 
                      watch_percentage, last_watched, completed)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (video_path, chapter, video_name, current_time, duration, playback_speed,
                   watch_percentage, timestamp, completed))
        conn.commit()
        conn.close()
        print(f"[SAVE PROGRESS] Successfully saved to database")
    except Exception as e:
        print(f"[SAVE PROGRESS] Error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return jsonify({
        'status': 'success', 
        'watch_percentage': watch_percentage,
        'timestamp': timestamp,
        'completed': completed
    })

@app.route('/api/get-progress/<path:video_path>')
def get_progress(video_path):
    """
    API endpoint to retrieve video watching progress.
    
    Args:
        video_path (str): Unique path to the video file
        
    Returns:
        JSON response with video progress data or empty object if not found
        
        Response format:
        {
            'current_time': float,      # Last watched position in seconds
            'playback_speed': float,    # Last used playback speed
            'watch_percentage': float,  # Percentage of video watched
            'completed': int,           # 1 if completed (90%+), 0 otherwise
            'last_watched': str        # Timestamp of last view
        }
    """
    print(f"[GET PROGRESS] Fetching progress for: {video_path}")
    
    try:
        conn = sqlite3.connect('course_progress.db')
        c = conn.cursor()
        c.execute('SELECT current_time, playback_speed, watch_percentage, completed, last_watched FROM video_progress WHERE video_path = ?',
                  (video_path,))
        result = c.fetchone()
        conn.close()
        
        if result:
            print(f"[GET PROGRESS] Found - Time: {result[0]:.2f}s, Speed: {result[1]}x, Progress: {result[2]:.2f}%, Last Watched: {result[4]}")
            return jsonify({
                'current_time': result[0],
                'playback_speed': result[1],
                'watch_percentage': result[2],
                'completed': result[3],
                'last_watched': result[4]
            })
        else:
            print(f"[GET PROGRESS] No progress found for this video")
            return jsonify({
                'current_time': 0, 
                'playback_speed': 1.0, 
                'watch_percentage': 0, 
                'completed': 0,
                'last_watched': None
            })
    except Exception as e:
        print(f"[GET PROGRESS] Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-all-progress')
def get_all_progress():
    """
    API endpoint to retrieve all video progress data.
    
    Fetches progress information for all videos that have been watched,
    including current position, completion status, and metadata.
    
    Returns:
        JSON object where keys are video paths and values contain:
        {
            'current_time': float,      # Last watched position in seconds
            'playback_speed': float,    # Last used playback speed  
            'watch_percentage': float,  # Percentage of video watched
            'completed': int,           # 1 if completed, 0 otherwise
            'last_watched': str,        # Timestamp of last view
            'duration': float          # Total video duration in seconds
        }
    """
    print(f"[GET ALL PROGRESS] Fetching all progress data...")
    
    try:
        conn = sqlite3.connect('course_progress.db')
        c = conn.cursor()
        c.execute('SELECT video_path, current_time, playback_speed, watch_percentage, completed, last_watched, duration FROM video_progress')
        results = c.fetchall()
        conn.close()
        
        # Convert database results to dictionary format
        progress_dict = {
            row[0]: {
                'current_time': row[1],
                'playback_speed': row[2],
                'watch_percentage': row[3], 
                'completed': row[4],
                'last_watched': row[5],
                'duration': row[6]
            } for row in results
        }
        print(f"[GET ALL PROGRESS] Retrieved {len(progress_dict)} video progress records")
        return jsonify(progress_dict)
    except Exception as e:
        print(f"[GET ALL PROGRESS] Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """
    API endpoint for managing user settings.
    
    GET: Returns all current user settings as JSON
    POST: Updates user settings with provided key-value pairs
    
    Settings include:
        - theme: 'dark' or 'light'
        - auto_resume: 'true' or 'false' 
        - save_last_chapter: 'true' or 'false'
        - max_playback_speed: string representation of max speed (e.g. '2.0')
        - current_playback_speed: current default playback speed
        - last_chapter: name of last accessed chapter
        
    Returns:
        JSON response with settings data or success status
    """
    conn = sqlite3.connect('course_progress.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        # Update settings with provided data
        data = request.json
        print(f"[SETTINGS] Updating settings: {data}")
        
        # Insert or update each setting key-value pair
        for key, value in data.items():
            c.execute("INSERT OR REPLACE INTO user_settings (setting_key, setting_value) VALUES (?, ?)",
                     (key, str(value)))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    else:
        # Retrieve all current settings
        c.execute('SELECT setting_key, setting_value FROM user_settings')
        settings_data = {row[0]: row[1] for row in c.fetchall()}
        conn.close()
        return jsonify(settings_data)

@app.route('/api/analytics')
def analytics():
    """
    API endpoint that provides comprehensive learning analytics.
    
    Calculates and returns statistics including:
    - Total completed videos across all chapters
    - Total watch time in seconds
    - Per-chapter statistics with completion rates
    - Average progress percentages including unwatched videos
    
    The analytics account for the actual number of videos in each
    chapter folder, treating unwatched videos as 0% progress for
    accurate average calculations.
    
    Returns:
        JSON object containing:
        {
            'completed_videos': int,     # Total videos marked as completed
            'total_watch_time_seconds': float,  # Total seconds watched
            'chapter_stats': {           # Per-chapter breakdown
                'chapter_name': {
                    'total_videos': int,     # Actual video count in folder
                    'completed_videos': int,  # Number completed in chapter
                    'avg_progress': float,    # Average % including unwatched
                    'watch_time': float      # Chapter watch time in seconds
                }
            }
        }
    """
    print(f"[ANALYTICS] Computing analytics...")
    
    try:
        conn = sqlite3.connect('course_progress.db')
        c = conn.cursor()
        
        # Retrieve all video progress data from database
        c.execute('SELECT chapter, watch_percentage, completed, duration FROM video_progress')
        results = c.fetchall()
        conn.close()
        
        # Calculate overall analytics
        total_videos_watched = len(results)
        completed_videos = sum(1 for r in results if r[2] == 1)  # Count completed videos
        total_watch_time = sum(r[3] * (r[1] / 100) for r in results if r[3])  # Sum actual watch time
        
        # Get actual video counts from filesystem to handle unwatched videos
        base_path = os.path.join('static')
        actual_chapter_videos = {}
        for chapter_folder in os.listdir(base_path):
            chapter_path = os.path.join(base_path, chapter_folder)
            if os.path.isdir(chapter_path):
                # Count video files with supported extensions
                video_count = len([f for f in os.listdir(chapter_path) 
                                  if f.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))])
                actual_chapter_videos[chapter_folder] = video_count
        
        # Aggregate progress data by chapter
        chapter_progress = {}
        for row in results:
            chapter = row[0]
            if chapter not in chapter_progress:
                chapter_progress[chapter] = {
                    'completed_videos': 0,
                    'total_progress': 0,
                    'watched_count': 0,
                    'watch_time': 0
                }
            chapter_progress[chapter]['watched_count'] += 1
            if row[2] == 1:  # If video is completed
                chapter_progress[chapter]['completed_videos'] += 1
            chapter_progress[chapter]['total_progress'] += row[1]  # Add watch percentage
            if row[3]:  # If duration is available
                chapter_progress[chapter]['watch_time'] += row[3] * (row[1] / 100)
        
        # Calculate final statistics including unwatched videos as 0% progress
        chapter_stats = {}
        for chapter, actual_total in actual_chapter_videos.items():
            progress_data = chapter_progress.get(chapter, {
                'completed_videos': 0,
                'total_progress': 0,
                'watched_count': 0,
                'watch_time': 0
            })
            
            # Average progress considers all videos in chapter (unwatched = 0%)
            avg_progress = progress_data['total_progress'] / actual_total if actual_total > 0 else 0
            
            chapter_stats[chapter] = {
                'total_videos': actual_total,
                'completed_videos': progress_data['completed_videos'],
                'avg_progress': avg_progress,
                'watch_time': progress_data['watch_time']
            }
        
        # Prepare final analytics response
        analytics_data = {
            'total_videos_watched': total_videos_watched,
            'completed_videos': completed_videos,
            'total_watch_time_seconds': int(total_watch_time),
            'chapter_stats': chapter_stats
        }
        
        print(f"[ANALYTICS] Analytics computed: {total_videos_watched} videos, {completed_videos} completed")
        return jsonify(analytics_data)
        
    except Exception as e:
        print(f"[ANALYTICS] Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    """
    Application entry point.
    
    Starts the Flask development server with debug mode enabled
    for development purposes. In production, use a proper WSGI server.
    """
    app.run(debug=True)
