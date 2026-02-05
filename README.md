# 🎯 User Activity Logger - Multi-Employee Monitoring System

## 📋 Project Overview

Production-ready employee activity monitoring system with modern React dashboard. Tracks keyboard, mouse, apps, idle time, and login/logout events in real-time.

**Built by:** Rajat Singh Rawat  
**Status:** Production Ready ✅

---

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install pynput psutil pygetwindow pywin32 schedule fastapi uvicorn matplotlib pillow
cd web && npm install
```

### Step 2: Configure Employee Name
Edit `reports/confiq.py`:
```python
EMPLOYEE_NAME = "Rajat"  # Change for each employee: Rajat, Rikshit, Priyanshu, Sneha
START_TIME = time(9, 0, 0)        # 9:00 AM
END_TIME = time(18, 0, 0)         # 6:00 PM (use 24-hour format)
SCREENSHOT_INTERVAL = 300         # Take screenshot every 5 minutes
ENABLE_SCREENSHOTS = True         # Enable/disable screenshot capture
```

### Step 3: Run Project
**Right-click** `START_LOGGER.bat` → **Run as Administrator**

Or manually:
```bash
python main.py
cd api && python main.py
cd web && npm run dev
```

### Step 4: Access Dashboard
- **On PC:** http://localhost:5173
- **On Phone:** http://YOUR_PC_IP:5173 (same WiFi required)
- **Login:** andrewtatecoder@gmail.com
- **Screenshots:** Click "Screenshots" button in header

---

## 📐 Calculation Formulas

### 1. Total Logged Time
```
Total Logged Time = End Time - Start Time
```
Baseline duration between login and logout (in seconds/minutes)

### 2. Total Idle Time
```
Total Idle Time = SUM(all idle periods)
```
Sum of all periods with no keyboard/mouse activity (threshold: 3 minutes)

### 3. Total Active Time
```
Total Active Time = Total Logged Time - Total Idle Time
```
Time when employee was actively working

### 4. Distraction Time
```
Distraction Time = SUM(time spent on non-productive apps/sites)
```
Tracks time spent on YouTube, Instagram, Facebook, Netflix, Shopping sites, etc.

### 5. True Active Time
```
True Active Time = Active Time - Distraction Time
```
Actual productive time excluding distractions

### 6. Productivity Score (Enhanced)
```
Productivity Score = (True Active Time / Total Logged Time) × 100
```
- **True Active Time** = Active Time - Distraction Time
- Everything EXCEPT distractions is considered productive
- Includes: Work apps, Google Meet, Zoom, Email, Coding, Browsing work sites
- Excludes: YouTube, Instagram, Facebook, Shopping, Gaming, Entertainment
- Capped at 95% (realistic maximum)
- **Distraction apps:** YouTube, Instagram, Facebook, WhatsApp, Netflix, Spotify, Amazon, Flipkart, Gaming, Social Media, Entertainment sites

### 7. Effectivity Percentage
```
Effectivity % = 100 - (Idle Time / Total Logged Time) × 100
```
Inverse of idle ratio - shows how effective the work session was

### 8. Idle Per Section
```
Section Duration = Total Logged Time / 10
Idle Time (section i) = SUM(idle intervals within section i)
```
Divides session into 10 equal sections for hourly idle analysis

---

## 📊 Generated Graphs

Three professional graphs auto-generated at session end:

### 1. Effectivity Pie Chart
- **File:** `reports/graphs/effectivity_pie.png`
- **Shows:** Effective Time % vs Idle Time %
- **Colors:** Green (effective), Red (idle)

### 2. Productivity Bar Graph
- **File:** `reports/graphs/productivity_bar.png`
- **Shows:** Overall Productivity Score (0-100)
- **Colors:** 
  - Orange: <40% (Needs improvement)
  - Yellow: 40-70% (Average)
  - Green: >70% (Excellent)

### 3. Idle Distribution Line Chart
- **File:** `reports/graphs/idle_distribution.png`
- **Shows:** Idle time across 10 equal time sections
- **X-axis:** Time sections (S1-S10)
- **Y-axis:** Idle time in minutes

---

## 🆕 Key Features

### Multi-Employee Support
- Each employee runs logger with unique name
- Boss selects employee on dashboard
- Supports: Rajat, Rikshit, Priyanshu, Sneha

### Last 7 Days Tracking
- Stores daily productivity in database
- Shows 7-day performance trend
- Helps identify patterns

### Color-Coded Charts
- 🟠 Orange: <40% (Needs improvement)
- 🟡 Yellow: 40-70% (Average)
- 🟢 Green: >70% (Excellent)

### Mobile Responsive
- Optimized for phone screens
- Smaller fonts and compact layout
- All features accessible on mobile

### Screenshot Capture
- Automatic screenshots every 5 minutes (configurable)
- Stored in database with timestamps
- View screenshots in dashboard gallery
- Lightbox modal for full-screen viewing
- Auto-refresh every 60 seconds
- Old screenshots deleted on new session

### Distraction Time Detection
- Tracks non-productive apps/websites
- YouTube, Instagram, Facebook, WhatsApp, LinkedIn
- Netflix, Spotify, Amazon, Flipkart, Gaming sites
- Displays distraction breakdown on dashboard
- Reduces productivity score based on distraction time

### Professional UI
- Baby pink color scheme
- Inter font family
- Clean, modern design
- 3D hover effects on KPI cards
- Distraction summary with visual alerts
- Mobile-responsive design

---

## 🔧 Configuration

**Employee Name:** `reports/confiq.py` → `EMPLOYEE_NAME`  
**Work Hours:** `reports/confiq.py` → `START_TIME`, `END_TIME` (24-hour format)  
**Screenshot Interval:** `reports/confiq.py` → `SCREENSHOT_INTERVAL` (seconds)  
**Enable Screenshots:** `reports/confiq.py` → `ENABLE_SCREENSHOTS` (True/False)  
**Idle Threshold:** `modules/idle_time_detecter.py` → `threshold=180` (3 minutes)  
**Distraction Apps:** `reports/confiq.py` → `DISTRACTION_KEYWORDS` (60+ keywords)

---

## 📡 API Endpoints

- `GET /api/employees` - List all employees
- `GET /api/dashboard` - Dashboard data with real-time metrics
- `GET /api/reports/today?employee=Rajat` - Employee report
- `GET /api/productivity/last7days?employee=Rajat` - 7-day trend
- `GET /api/screenshots` - List of today's screenshots
- `GET /api/screenshots/{filename}` - Serve screenshot image
- `DELETE /api/screenshots` - Clear all screenshots
- `GET /health` - API health check

---

## 📱 Phone Access

### Automatic Setup
START_LOGGER.bat automatically:
- Requests admin rights
- Adds firewall rules for ports 5173 and 8000
- Enables network access

### Access from Phone
1. Connect phone to same WiFi as PC
2. Find PC IP: Run `ipconfig` in CMD, look for IPv4 Address
3. Open: http://YOUR_PC_IP:5173
4. Login with boss email

---

## 📁 Project Structure

```
UserActivityLogger/
├── api/                          # FastAPI backend server
│   ├── main.py                   # API endpoints and calculations
│   └── requirements.txt          # API dependencies
├── logs/                         # Data storage
│   ├── archive/                  # Previous session databases
│   ├── screenshots/              # Screenshot images
│   └── user_logs.db             # Current session database
├── modules/                      # Tracking modules
│   ├── app_usage_tracker.py     # Application usage tracking
│   ├── idle_time_detecter.py    # Idle time detection (3 min threshold)
│   ├── keyboard_logger.py       # Keyboard event logging
│   ├── login_logout_tracker.py  # Session start/end tracking
│   ├── mouse_tracker.py         # Mouse event logging
│   └── screenshot_capture.py    # Automatic screenshot capture
├── reports/                      # Configuration and reports
│   ├── graphs/                   # Generated graphs (pie, bar, line)
│   └── confiq.py                # Main configuration file
├── web/                          # React frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── AppsDoughnut.tsx # App usage pie chart
│   │   │   ├── HourlyChart.tsx  # Hourly productivity bar chart
│   │   │   ├── ScreenshotsGallery.tsx # Screenshot viewer
│   │   │   └── WeeklyTrend.tsx  # 7-day trend chart
│   │   ├── pages/
│   │   │   ├── NewDashboard.tsx # Main dashboard
│   │   │   └── NewLogin.tsx     # Login page
│   │   └── App.tsx              # Main app component
│   ├── package.json             # Frontend dependencies
│   └── vite.config.js           # Vite configuration
├── main.py                       # Main orchestrator
├── requirements.txt              # Python dependencies
└── START_LOGGER.bat             # One-click startup script
```

---

## ✅ Verification

All calculations have been verified and tested:

**Formula Accuracy:**
- ✅ Total Hours = Logout Time - Login Time
- ✅ Active Time = Total Hours - Idle Time
- ✅ True Active = Active Time - Distraction Time
- ✅ Productivity = (True Active / Total Hours) × 100
- ✅ Effectivity = 100 - (Idle / Total Hours) × 100

**Features Tested:**
- ✅ Keyboard and mouse tracking
- ✅ Idle detection (3-minute threshold)
- ✅ App usage monitoring
- ✅ Distraction time calculation
- ✅ Screenshot capture and gallery
- ✅ Real-time dashboard updates
- ✅ Mobile responsive design
- ✅ Phone access via WiFi
- ✅ 7-day productivity trend
- ✅ Hourly activity breakdown

---

## 🎯 Project Status: Production Ready ✅

**Built with ❤️ by Rajat Singh Rawat**
