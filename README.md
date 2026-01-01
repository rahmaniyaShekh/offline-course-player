# C++ DSA Course - Modern Video Learning Platform

## 🎥 Advanced Learning Management System with Analytics Dashboard

A comprehensive, modern video learning platform built with Flask featuring analytics dashboard, progress tracking, settings management, and customizable UI themes. Perfect for organizing and tracking progress through course content.

## ✨ Key Features

### 🎯 **Analytics Dashboard**
- **Comprehensive Analytics**: Total progress percentage, videos watched, and total watch time
- **Chapter-wise Statistics**: Per-chapter completion rates and progress tracking
- **Real-time Updates**: Analytics update dynamically as you progress through content
- **Visual Progress Indicators**: Beautiful progress bars and completion status indicators

### 📊 **Advanced Settings Management**
- **Theme Switching**: Toggle between modern dark and light themes with smooth transitions
- **Auto-Resume Control**: Enable/disable automatic video resumption from last position
- **Playback Speed Limits**: Configure maximum allowed playback speed (1x to 3x)
- **Last Chapter Memory**: Remember and highlight your last accessed chapter
- **Persistent Settings**: All preferences saved to database and restored on startup

### 🎬 **Enhanced Video Player**
- **YouTube-Style Interface**: Professional video controls with modern UI
- **Smart Resume**: Automatically resumes videos from where you left off
- **Progress Tracking**: Saves viewing progress every 3 seconds
- **Speed Memory**: Remembers preferred playback speed per video
- **Completion Detection**: Auto-marks videos as watched at 90% completion
- **Theater Mode**: Distraction-free viewing experience

### 🎨 **Modern UI & Theming**
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Material Design Icons**: Beautiful SVG icons throughout the interface
- **Glass Morphism Effects**: Modern backdrop blur and transparency effects
- **Animated Backgrounds**: Subtle gradient animations for visual appeal
- **CSS Custom Properties**: Fully customizable color schemes and sizing
- **Smooth Transitions**: Professional animations and hover effects

### 🗂️ **Smart Content Organization**
- **Chapter Navigation**: Easy switching between course chapters/folders
- **Grid Layout**: Modern card-based chapter display with preview information
- **Progress Visualization**: Visual progress bars on each chapter card
- **Resource Management**: PDF and document display alongside videos
- **Search-Friendly Structure**: Organized file system for easy content management

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Web browser (Chrome, Firefox, Edge, or Safari)

### Installation

1. **Clone or download** the project to your local machine

2. **Install required Python packages:**
```bash
pip install flask
```

3. **Organize your content** in the `static/` folder:
```
static/
├── Day - 01/
│   ├── video1.mp4
│   ├── video2.mp4
│   └── notes.pdf
├── Day - 02/
└── ...
```

4. **Run the application:**
```bash
python app.py
```

5. **Open your browser** and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
C++ DSA Course/
├── app.py                      # Flask backend with API endpoints
├── check_database.py           # Database inspection utility
├── course_progress.db          # SQLite database (auto-created)
├── templates/
│   ├── chapters.html          # Analytics dashboard & chapter selection
│   ├── course.html            # Legacy interface (deprecated)
│   └── player.html            # Modern video player interface
├── static/                    # Your course content folders
│   ├── Day - 01/
│   ├── Day - 02/
│   └── ...
└── icons/                     # Custom icon assets (if any)
```

## 🎮 Keyboard Shortcuts

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

## 💾 Database Schema

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
- **setting_key**: Setting identifier (theme, auto_resume, etc.)
- **setting_value**: Setting value
- **updated_at**: Last modification timestamp

## 🔧 API Endpoints

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
    "max_playback_speed": "2.0"
}

POST /api/settings
Body: {
    "theme": "light",
    "max_playback_speed": "2.5"
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

## 🎨 UI Features & Customization

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

## 🔧 Configuration & Customization

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

## 🚀 Advanced Usage

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

### Multi-Course Support
To use this system for multiple courses:
1. Create separate folders for each course in `static/`
2. Modify the Flask routes to handle course selection
3. Update the database schema to include course identifiers
4. Customize the UI to show course selection

## 🐛 Troubleshooting

### Common Issues

**Videos not playing:**
- ✅ Check video format is supported (mp4 recommended)
- ✅ Verify file paths are correct in browser console
- ✅ Ensure videos are placed in `static/` folder
- ✅ Check browser media codec support

**Progress not saving:**
- ✅ Check browser console for API errors
- ✅ Verify `course_progress.db` exists and is writable
- ✅ Ensure Flask app has proper file system permissions
- ✅ Check network connectivity to localhost:5000

**Settings not persisting:**
- ✅ Check database connectivity
- ✅ Verify user_settings table exists
- ✅ Check browser local storage permissions
- ✅ Look for JavaScript errors in console

**UI not responsive:**
- ✅ Clear browser cache and cookies
- ✅ Check for JavaScript errors in console
- ✅ Try different browser (Chrome/Firefox recommended)
- ✅ Verify CSS custom properties support

### Debug Mode
Enable debug mode by setting `debug=True` in `app.py` for detailed error messages.

### Database Inspection
Use `python check_database.py` to view database contents and verify data integrity.

## 🔮 Future Enhancement Ideas

### Planned Features
- [ ] **Multi-user Authentication**: User accounts and personalized progress
- [ ] **Video Thumbnails**: Auto-generate thumbnails from video frames
- [ ] **Advanced Search**: Full-text search across video titles and descriptions
- [ ] **Bookmarks System**: Save favorite moments in videos
- [ ] **Note-taking**: Integrated note-taking with timestamps
- [ ] **Quiz Integration**: Chapter-end quizzes and assessments
- [ ] **Certificate System**: Completion certificates and badges
- [ ] **Mobile App**: Native mobile applications

### Technical Improvements
- [ ] **Progressive Web App (PWA)**: Offline support and app-like experience
- [ ] **Video Streaming**: HLS/DASH support for better video delivery
- [ ] **CDN Integration**: Content delivery network for global access
- [ ] **Analytics Export**: Export learning analytics to CSV/PDF
- [ ] **API Documentation**: Complete REST API documentation
- [ ] **Docker Support**: Containerized deployment options

### Community Features
- [ ] **Discussion Threads**: Chapter and video-specific discussions
- [ ] **Study Groups**: Collaborative learning features
- [ ] **Progress Sharing**: Social features for sharing achievements
- [ ] **Instructor Dashboard**: Content management for educators

## 🤝 Contributing

We welcome contributions! Areas where you can help:

### Development
- **Frontend**: Improve UI/UX, add new features
- **Backend**: Optimize API endpoints, add new functionality
- **Testing**: Write unit tests and integration tests
- **Documentation**: Improve docs and add tutorials

### Design
- **UI/UX**: Design improvements and accessibility features
- **Icons**: Create custom icon sets
- **Themes**: Develop new color schemes and themes

### Content
- **Templates**: Create course templates for different subjects
- **Translations**: Add multi-language support
- **Documentation**: Write guides and best practices

## 📄 License & Usage

This project is open-source and available for educational and commercial use. Feel free to:
- ✅ Use it for personal learning projects
- ✅ Adapt it for educational institutions
- ✅ Modify and distribute with attribution
- ✅ Use it as a base for commercial products

## 🆘 Support & Community

### Getting Help
- 📖 **Documentation**: Check this README for detailed information
- 🐛 **Issues**: Report bugs and request features via GitHub issues
- 💡 **Discussions**: Join community discussions for help and ideas

### Acknowledgments
Built with modern web technologies:
- **Flask**: Lightweight Python web framework
- **SQLite**: Embedded database for data persistence
- **Material Design**: Icon system and design principles
- **Modern CSS**: CSS Grid, Flexbox, and Custom Properties

---

**Happy Learning! 🚀📚**

*Transform your course content into an engaging, trackable learning experience.*
