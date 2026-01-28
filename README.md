# Offline Course Player - Modern Video Learning Platform

## Advanced Learning Management System with Analytics Dashboard

A comprehensive, modern video learning platform built with Flask featuring analytics dashboard, progress tracking, settings management, and customizable UI themes. Perfect for organizing and tracking progress through course content.

## Key Features

### Analytics Dashboard
- **Comprehensive Analytics**: Total progress percentage, videos watched, and total watch time
- **Chapter-wise Statistics**: Per-chapter completion rates and progress tracking
- **Real-time Updates**: Analytics update dynamically as you progress through content
- **Visual Progress Indicators**: Beautiful progress bars and completion status indicators

### Advanced Settings Management
- **Theme Switching**: Toggle between modern dark and light themes with smooth transitions
- **Auto-Resume Control**: Enable/disable automatic video resumption from last position
- **Playback Speed Limits**: Configure maximum allowed playback speed (1x to 3x)
- **Last Chapter Memory**: Remember and highlight your last accessed chapter
- **Persistent Settings**: All preferences saved to database and restored on startup

### Enhanced Video Player
- **YouTube-Style Interface**: Professional video controls with modern UI
- **Smart Resume**: Automatically resumes videos from where you left off
- **Progress Tracking**: Saves viewing progress every 3 seconds
- **Speed Memory**: Remembers preferred playback speed per video
- **Completion Detection**: Auto-marks videos as watched at 90% completion
- **Theater Mode**: Distraction-free viewing experience

### Modern UI & Theming
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Material Design Icons**: Beautiful SVG icons throughout the interface
- **Glass Morphism Effects**: Modern backdrop blur and transparency effects
- **Animated Backgrounds**: Subtle gradient animations for visual appeal
- **CSS Custom Properties**: Fully customizable color schemes and sizing
- **Smooth Transitions**: Professional animations and hover effects

### Smart Content Organization
- **Chapter Navigation**: Easy switching between course chapters/folders
- **Grid Layout**: Modern card-based chapter display with preview information
- **Progress Visualization**: Visual progress bars on each chapter card
- **Resource Management**: PDF and document display alongside videos
- **Search-Friendly Structure**: Organized file system for easy content management

## 🚀 Quick Start (Desktop App)

### One-Click Launch

1. **Double-click `OfflineCoursePlayer.pyw`** to start the application
   - First launch installs required dependencies automatically (Flask, PyQt6)
   - No command line required!

2. **Select your course folder** when prompted
   - Click "📁 Select Folder" to choose where your video content is stored
   - The folder is remembered for future launches

3. **Start learning!**
   - Server starts automatically
   - Browser opens to the learning platform
   - Track your progress across sessions

### Creating a Desktop Shortcut

**Windows:**
- Right-click `OfflineCoursePlayer.pyw` → Send to → Desktop (create shortcut)
- Or right-click `start.bat` → Send to → Desktop

**macOS/Linux:**
- Create a shortcut/alias to `start.sh`
- Make executable first: `chmod +x start.sh`

---

## 📋 Prerequisites

- **Python 3.7+** ([Download Python](https://www.python.org/downloads/))
- Web browser (Chrome, Firefox, Edge, or Safari)

Dependencies (Flask, PyQt6) install automatically on first launch.

---

## 🖥️ Desktop App Controls

| Button | Action |
|--------|--------|
| **▶ Start Server** | Starts the Flask server on port 5000 |
| **⏹ Stop Server** | Gracefully stops the server |
| **🌐 Open Browser** | Opens `http://localhost:5000` in your browser |
| **📁 Select Folder** | Choose a new content folder |

The app window shows server logs and current status.

---

## 📁 Content Folder Structure

Organize your course content like this:
```
Your Course Folder/
├── Day - 01/
│   ├── video1.mp4
│   ├── video2.mp4
│   └── notes.pdf
├── Day - 02/
│   └── lecture.mp4
└── Chapter 3/
    └── ...
```

**Supported formats:**
- **Video**: .mp4, .mov, .avi, .mkv, .webm
- **Documents**: .pdf, .docx, .doc, .txt

---

## 💾 Where Data is Stored

User settings and progress are stored separately from your course content:

| Platform | Location |
|----------|----------|
| **Windows** | `%APPDATA%\OfflineCoursePlayer\` |
| **macOS** | `~/Library/Application Support/OfflineCoursePlayer/` |
| **Linux** | `~/.config/OfflineCoursePlayer/` |

**Files stored:**
- `config.json` - Selected folder path, preferences
- `course_progress.db` - Video progress, watch history

---

## ⌨️ Alternative: Command Line Usage

If you prefer the command line:

```bash
# Install dependencies manually
pip install flask PyQt6

# Run the desktop app
python OfflineCoursePlayer.pyw

# Or run Flask directly (no GUI)
python app.py
```

## Project Structure

```
C++ DSA Course/
├── OfflineCoursePlayer.pyw     # 🚀 Double-click to launch (main entry)
├── start.bat                   # Windows alternative launcher
├── start.sh                    # macOS/Linux launcher
├── app.py                      # Flask backend with API endpoints
├── config.py                   # Configuration & persistence module
├── server.py                   # Server lifecycle management
├── desktop_app.py              # PyQt6 desktop GUI
├── check_database.py           # Database inspection utility
├── templates/
│   ├── chapters.html           # Analytics dashboard & chapter selection
│   └── player.html             # Modern video player interface
├── static/                     # Default content folder (or use any folder)
└── icons/                      # App icons
```

## Keyboard Shortcuts

### Video Player Controls
| Key | Action |
|-----|--------|
| `Space` / `K` | Play/Pause |
| `F` | Toggle Fullscreen |
| `T` | Toggle Theater Mode |
| `M` | Mute/Unmute |
| `J` / `←` | Rewind 5 seconds |
| `L` / `→` | Forward 5 seconds |
| `↑` | Increase volume |
| `↓` | Decrease volume |
| `>` | Cycle playback speed |

### General Navigation
| Key | Action |
|-----|--------|
| `Esc` | Close modals/settings |
| `Ctrl + ,` | Open settings (on chapters page) |

## Database Schema

The app uses SQLite with two main tables:

### **video_progress** Table
- **video_path**: Unique identifier for each video
- **chapter**: Chapter/folder name
- **video_name**: Video filename
- **current_time**: Last watched position (seconds)
- **duration**: Total video duration
- **playback_speed**: Preferred playback speed (0.25x - 3x)
- **watch_percentage**: How much of video watched (0-100%)
- **last_watched**: Timestamp of last view
- **completed**: Boolean flag (1 if >90% watched)

### **user_settings** Table
- **setting_key**: Setting identifier (theme, auto_resume, current_playback_speed, etc.)
- **setting_value**: Setting value
- **updated_at**: Last modification timestamp

## API Endpoints

### Analytics
```http
GET /api/analytics
Response: {
    "completed_videos": 15,
    "total_watch_time_seconds": 12650,
    "chapter_stats": {
        "Day - 01": {
            "total_videos": 5,
            "completed_videos": 3,
            "avg_progress": 75.5
        }
    }
}
```

### Settings Management
```http
GET /api/settings
Response: {
    "theme": "dark",
    "auto_resume": "true",
    "save_last_chapter": "true",
    "max_playback_speed": "2.0",
    "current_playback_speed": "1.25"
}

POST /api/settings
Body: {
    "theme": "light",
    "max_playback_speed": "2.5",
    "current_playback_speed": "1.5"
}
```

### Progress Tracking
```http
POST /api/save-progress
Body: {
    "video_path": "/static/Day - 01/video.mp4",
    "chapter": "Day - 01",
    "video_name": "video.mp4",
    "current_time": 120.5,
    "duration": 300.0,
    "playback_speed": 1.25
}

GET /api/get-progress/<video_path>
Response: {
    "current_time": 120.5,
    "playback_speed": 1.25,
    "watch_percentage": 40.17,
    "completed": 0
}

GET /api/get-all-progress
Response: {
    "/static/Day - 01/video.mp4": {
        "watch_percentage": 40.17,
        "completed": 0
    }
}
```

## UI Features & Customization

### Analytics Dashboard (`/`)
- **Statistics Cards**: Total progress, videos watched, and watch time
- **Chapter Grid**: Visual chapter cards with progress indicators
- **Status Badges**: "In Progress" and "Completed" indicators
- **Responsive Layout**: Adapts to all screen sizes

### Video Player Interface
- **Modern Controls**: YouTube-style control bar with custom styling
- **Chapter Sidebar**: Scrollable playlist with video thumbnails
- **Progress Indicators**: Real-time progress tracking and completion status
- **Settings Panel**: In-player settings for speed and quality options

### Customization System
- **CSS Variables**: Easily modify colors, sizes, and spacing
- **Icon System**: Centralized SVG icon management with Material Design
- **Text Localization**: All text labels stored in configurable objects
- **Theme Support**: Complete dark/light mode implementation

### Design Language
- **Glass Morphism**: Modern backdrop blur effects
- **Smooth Animations**: Professional transitions and micro-interactions
- **Material Icons**: Consistent iconography throughout the application
- **Typography**: Clean, readable font hierarchy

## Configuration & Customization

### Customizing Colors and Themes
All colors are defined as CSS custom properties in `/templates/chapters.html`:

```css
:root {
    /* Primary Colors */
    --primary-color: #667eea;
    --accent-color: #764ba2;
    
    /* Background Colors */
    --bg-primary: #0f0f0f;
    --bg-secondary: #1a1a1a;
    
    /* Text Colors */
    --text-primary: #ffffff;
    --text-secondary: #b0b0b0;
}
```

### Customizing Icons
Icons are centrally managed in the `ICONS` object:

```javascript
const ICONS = {
    settings: `<svg viewBox="0 0 24 24">...</svg>`,
    video: `<svg viewBox="0 0 24 24">...</svg>`,
    // Add your custom SVG icons here
};
```

### Customizing Text Labels
All text is stored in the `TEXT` object for easy localization:

```javascript
const TEXT = {
    logoTitle: 'DSA Course',
    settingsBtn: 'Settings',
    // Customize any text labels here
};
```

## Advanced Usage

### Content Organization Best Practices
1. **Naming Convention**: Use descriptive folder names (e.g., "Day - 01", "Chapter 1 - Introduction")
2. **File Structure**: Keep videos and related documents in the same chapter folder
3. **Video Formats**: Supports .mp4, .mov, .avi, .mkv, .webm
4. **Document Types**: Supports .pdf, .docx, .doc, .txt

### Performance Optimization
- **Progress Auto-Save**: Optimized to save every 3 seconds without UI blocking
- **Lazy Loading**: Chapter content loads on-demand
- **Efficient Queries**: Database queries optimized for large course libraries
- **Caching**: Static assets cached for faster load times

## Troubleshooting

### Common Issues

**Videos not playing:**
- Check video format is supported (mp4 recommended)
- Verify file paths are correct in browser console
- Ensure videos are placed in `static/` folder
- Check browser media codec support

**Progress not saving:**
- Check browser console for API errors
- Verify `course_progress.db` exists and is writable
- Ensure Flask app has proper file system permissions
- Check network connectivity to localhost:5000

**Settings not persisting:**
- Check database connectivity
- Verify user_settings table exists
- Check browser local storage permissions
- Look for JavaScript errors in console

**UI not responsive:**
- Clear browser cache and cookies
- Check for JavaScript errors in console
- Try different browser (Chrome/Firefox recommended)
- Verify CSS custom properties support

### Debug Mode
Enable debug mode by setting `debug=True` in `app.py` for detailed error messages.

### Database Inspection
Use `python check_database.py` to view database contents and verify data integrity.

## Contributing

We welcome contributions to improve this learning platform! Here's how you can help:

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch** from main: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test them thoroughly
4. **Commit your changes** with clear, descriptive messages
5. **Push to your branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request** with a detailed description of your changes

### Development Areas

#### Frontend Development
- **UI/UX Improvements**: Enhance user interface and experience
- **Accessibility**: Implement ARIA labels, keyboard navigation, screen reader support
- **Performance**: Optimize loading times and smooth animations
- **Mobile Experience**: Improve responsive design and touch interactions
- **Theme System**: Extend theming capabilities and color schemes

#### Backend Development
- **API Enhancements**: Add new endpoints and optimize existing ones
- **Database Optimization**: Improve query performance and schema design
- **Error Handling**: Better error messages and exception handling
- **Security**: Implement authentication and authorization features
- **Caching**: Add intelligent caching for improved performance

#### Testing
- **Unit Tests**: Write comprehensive tests for backend functions
- **Integration Tests**: Test API endpoints and database operations
- **Frontend Testing**: Implement JavaScript testing for UI components
- **Performance Testing**: Load testing and optimization validation
- **Cross-browser Testing**: Ensure compatibility across different browsers

#### Documentation
- **API Documentation**: Complete REST API reference with examples
- **Setup Guides**: Detailed installation and configuration instructions
- **User Tutorials**: Step-by-step guides for platform features
- **Developer Docs**: Contributing guidelines and code architecture
- **Video Tutorials**: Create instructional videos for setup and usage

### Code Standards

#### Python/Flask Backend
```python
# Follow PEP 8 style guidelines
# Use type hints where applicable
# Add docstrings to all functions
# Handle exceptions gracefully

def save_video_progress(video_path: str, current_time: float) -> bool:
    """
    Save video watching progress to database.
    
    Args:
        video_path: Unique path identifier for video
        current_time: Current playback position in seconds
        
    Returns:
        bool: True if save successful, False otherwise
    """
    try:
        # Implementation here
        return True
    except Exception as e:
        logger.error(f"Failed to save progress: {e}")
        return False
```

#### Frontend JavaScript
```javascript
// Use modern ES6+ syntax
// Add JSDoc comments for functions
// Follow consistent naming conventions
// Handle errors gracefully

/**
 * Load video progress from API
 * @param {string} videoPath - Unique video identifier
 * @returns {Promise<Object>} Progress data object
 */
async function loadVideoProgress(videoPath) {
    try {
        const response = await fetch(`/api/get-progress/${encodeURIComponent(videoPath)}`);
        return await response.json();
    } catch (error) {
        console.error('Failed to load progress:', error);
        return null;
    }
}
```

#### CSS/Styling
```css
/* Use meaningful class names */
/* Leverage CSS custom properties */
/* Ensure responsive design */
/* Add comments for complex selectors */

.video-player-controls {
    /* Player control bar styling */
    background: var(--player-controls-bg);
    border-radius: var(--radius-md);
    transition: opacity var(--transition-fast);
}

@media (max-width: 768px) {
    .video-player-controls {
        /* Mobile-specific adjustments */
        padding: var(--spacing-sm);
    }
}
```

### Reporting Issues

When reporting bugs or requesting features:

1. **Search existing issues** to avoid duplicates
2. **Use clear, descriptive titles**
3. **Provide detailed descriptions** with steps to reproduce
4. **Include system information** (OS, browser, Python version)
5. **Add screenshots or videos** if applicable
6. **Label appropriately** (bug, enhancement, documentation, etc.)

### Feature Requests

Before submitting feature requests:

1. **Check existing discussions** for similar ideas
2. **Explain the use case** and problem being solved
3. **Provide implementation suggestions** if you have ideas
4. **Consider backward compatibility** with existing features
5. **Think about user experience** and interface implications

### Community Guidelines

- **Be respectful** and constructive in all interactions
- **Help others** by answering questions and reviewing code
- **Share knowledge** through documentation and examples
- **Follow the code of conduct** and maintain a welcoming environment
- **Credit contributors** and acknowledge helpful feedback

## License

MIT License

Copyright (c) 2026 Mohammad Arif

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Support & Community

### Getting Help
- **Documentation**: Check this README for detailed information
- **Issues**: Report bugs and request features via GitHub issues
- **Discussions**: Join community discussions for help and ideas

### Acknowledgments
Built with modern web technologies:
- **Flask**: Lightweight Python web framework
- **SQLite**: Embedded database for data persistence
- **Material Design**: Icon system and design principles
- **Modern CSS**: CSS Grid, Flexbox, and Custom Properties

---

**Transform your course content into an engaging, trackable learning experience.**

---

## 📦 Packaging as Standalone Executable

To create a standalone `.exe` (Windows) or app bundle (macOS) that doesn't require Python:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable (Windows)
pyinstaller --onefile --windowed --name "OfflineCoursePlayer" OfflineCoursePlayer.pyw

# The executable will be in the 'dist' folder
```

**Note**: Copy `templates/` folder next to the executable for it to work.

---

## 🔒 Security Considerations

This application is designed for **local, single-user desktop use**:

| Aspect | Details |
|--------|---------|
| **Network** | Server runs on `127.0.0.1` only (not exposed to network) |
| **Authentication** | None - designed for personal use |
| **File Access** | Only reads from user-selected folder |
| **Path Security** | Paths are validated to prevent directory traversal |

**Not recommended for**: Shared/public servers, multi-user environments, or internet-facing deployments.
