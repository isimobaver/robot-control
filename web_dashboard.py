#!/usr/bin/env python3
"""
🌐 Robot Control Web Dashboard - لوحة التحكم الويب
Web-based control interface for robot management
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

try:
    from flask import Flask, render_template_string, jsonify, request, send_file
    from flask_socketio import SocketIO, emit, join_room, leave_room
    import cv2
    import numpy as np
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("Run: pip install flask flask-socketio opencv-python numpy")
    exit(1)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'robot_control_secret_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

class RobotDashboard:
    """لوحة التحكم الرئيسية"""
    
    def __init__(self):
        self.camera_enabled = False
        self.recording = False
        self.motor_status = {'state': 'idle', 'speed': 0}
        self.sensor_data = {
            'imu': {'ax': 0, 'ay': 0, 'az': 0},
            'lidar': {'distance': 0, 'obstacles': 0},
            'camera': {'fps': 0, 'resolution': '0x0'}
        }
        self.logs = []
    
    def log_event(self, event_type, message):
        """تسجيل الأحداث"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            'time': timestamp,
            'type': event_type,
            'message': message
        }
        self.logs.append(log_entry)
        if len(self.logs) > 100:
            self.logs.pop(0)
        
        return log_entry

# إنشاء instance
dashboard = RobotDashboard()

# HTML Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 لوحة التحكم بالروبوت</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #00d4ff;
        }
        .header h1 {
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        .card:hover {
            border-color: rgba(0,212,255,0.5);
            box-shadow: 0 8px 32px rgba(0,212,255,0.2);
        }
        .card h2 {
            font-size: 1.5em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #00d4ff;
        }
        .card-content {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: rgba(0,212,255,0.1);
            border-radius: 8px;
        }
        .stat-label {
            font-weight: bold;
        }
        .stat-value {
            color: #00d4ff;
            font-family: monospace;
            font-size: 1.1em;
        }
        .button-group {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .btn-danger {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .btn-success {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        .status-online { color: #00ff00; font-weight: bold; }
        .status-offline { color: #ff4444; font-weight: bold; }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online .status-indicator { background: #00ff00; }
        .status-offline .status-indicator { background: #ff4444; }
        .video-container {
            position: relative;
            width: 100%;
            padding-bottom: 75%;
            background: #000;
            border-radius: 10px;
            overflow: hidden;
        }
        .video-container img {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .logs-container {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            max-height: 300px;
            overflow-y: auto;
            border-left: 5px solid #00d4ff;
        }
        .log-entry {
            padding: 8px;
            margin: 5px 0;
            background: rgba(0,212,255,0.1);
            border-radius: 5px;
            font-size: 0.9em;
            border-left: 3px solid #00d4ff;
        }
        .slider {
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: rgba(255,255,255,0.2);
            outline: none;
            -webkit-appearance: none;
        }
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #00d4ff;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,212,255,0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🤖 لوحة التحكم بالروبوت الأمني</h1>
            <p>Robot Control Dashboard - نظام إدارة شامل للروبوت</p>
            <p id="connection-status" class="status-offline"><span class="status-indicator"></span>غير متصل</p>
        </div>
        
        <!-- Main Grid -->
        <div class="grid">
            <!-- Motor Control Card -->
            <div class="card">
                <h2>🔧 التحكم بالمحركات</h2>
                <div class="card-content">
                    <div class="stat">
                        <span class="stat-label">الحالة:</span>
                        <span class="stat-value" id="motor-state">متوقف</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">السرعة:</span>
                        <input type="range" class="slider" id="speed-slider" min="0" max="100" value="50">
                    </div>
                    <div class="button-group">
                        <button onclick="moveForward()">⬆️ أمام</button>
                        <button onclick="moveBackward()">⬇️ خلف</button>
                        <button onclick="turnLeft()">⬅️ يسار</button>
                        <button onclick="turnRight()">➡️ يمين</button>
                        <button class="btn-danger" onclick="stopMotor()" style="grid-column: 1/-1;">⛔ توقف</button>
                    </div>
                </div>
            </div>
            
            <!-- Sensor Data Card -->
            <div class="card">
                <h2>📊 بيانات الحساسات</h2>
                <div class="card-content">
                    <div class="stat">
                        <span class="stat-label">تسارع X:</span>
                        <span class="stat-value" id="imu-ax">0 m/s²</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">تسارع Y:</span>
                        <span class="stat-value" id="imu-ay">0 m/s²</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">تسارع Z:</span>
                        <span class="stat-value" id="imu-az">0 m/s²</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">المسافة (LiDAR):</span>
                        <span class="stat-value" id="lidar-distance">0 m</span>
                    </div>
                </div>
            </div>
            
            <!-- Status Card -->
            <div class="card">
                <h2>📡 حالة النظام</h2>
                <div class="card-content">
                    <div class="stat">
                        <span class="stat-label">الكاميرا:</span>
                        <span class="stat-value" id="camera-status">متوقفة</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">الليدار:</span>
                        <span class="stat-value" id="lidar-status">متوقف</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">IMU:</span>
                        <span class="stat-value" id="imu-status">متوقف</span>
                    </div>
                    <div class="button-group">
                        <button class="btn-success" onclick="startCamera()" style="grid-column: 1/-1;">📷 تشغيل الكاميرا</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Video Feed -->
        <div class="card">
            <h2>📹 بث الكاميرا المباشر</h2>
            <div class="video-container">
                <img id="video-feed" src="" alt="Camera Feed" style="display:none;">
                <p style="padding: 20px; text-align: center; color: #888;" id="video-placeholder">بث الكاميرا سيظهر هنا</p>
            </div>
        </div>
        
        <!-- Logs -->
        <div class="card" style="margin-top: 20px;">
            <h2>📋 السجلات</h2>
            <div class="logs-container" id="logs-container"></div>
        </div>
    </div>
    
    <script>
        const socket = io();
        const speedSlider = document.getElementById('speed-slider');
        
        // Connection events
        socket.on('connect', () => {
            updateStatus('online');
            addLog('success', '✅ متصل بالخادم');
        });
        
        socket.on('disconnect', () => {
            updateStatus('offline');
            addLog('error', '❌ قطع الاتصال');
        });
        
        // Control functions
        function moveForward() {
            socket.emit('motor_command', {direction: 'forward', speed: speedSlider.value});
            addLog('info', '⬆️ حركة للأمام');
        }
        
        function moveBackward() {
            socket.emit('motor_command', {direction: 'backward', speed: speedSlider.value});
            addLog('info', '⬇️ حركة للخلف');
        }
        
        function turnLeft() {
            socket.emit('motor_command', {direction: 'left'});
            addLog('info', '⬅️ دوران يسار');
        }
        
        function turnRight() {
            socket.emit('motor_command', {direction: 'right'});
            addLog('info', '➡️ دوران يمين');
        }
        
        function stopMotor() {
            socket.emit('motor_command', {direction: 'stop'});
            addLog('warning', '⛔ توقف');
        }
        
        function startCamera() {
            socket.emit('camera_command', {action: 'start'});
            addLog('info', '📷 تشغيل الكاميرا');
        }
        
        function updateStatus(state) {
            const statusEl = document.getElementById('connection-status');
            statusEl.className = `status-${state}`;
            statusEl.innerHTML = state === 'online' ? 
                '<span class="status-indicator"></span>متصل' : 
                '<span class="status-indicator"></span>غير متصل';
        }
        
        function addLog(type, message) {
            const logsContainer = document.getElementById('logs-container');
            const timestamp = new Date().toLocaleTimeString('ar-SA');
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            logEntry.innerHTML = `[${timestamp}] ${message}`;
            logsContainer.insertBefore(logEntry, logsContainer.firstChild);
            if (logsContainer.children.length > 20) {
                logsContainer.removeChild(logsContainer.lastChild);
            }
        }
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status')
def get_status():
    return jsonify({
        'motor': dashboard.motor_status,
        'sensors': dashboard.sensor_data,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/logs')
def get_logs():
    return jsonify(dashboard.logs)

# Socket Events
@socketio.on('motor_command')
def handle_motor_command(data):
    direction = data.get('direction')
    speed = data.get('speed', 50)
    
    dashboard.motor_status['state'] = direction
    dashboard.motor_status['speed'] = speed
    dashboard.log_event('motor', f'Motor command: {direction} (speed: {speed})')
    
    emit('response', {'status': 'ok', 'message': f'Motor {direction}'})

@socketio.on('camera_command')
def handle_camera_command(data):
    action = data.get('action')
    dashboard.camera_enabled = action == 'start'
    dashboard.log_event('camera', f'Camera {action}')
    
    emit('response', {'status': 'ok', 'message': f'Camera {action}'})

@socketio.on('connect')
def handle_connect():
    dashboard.log_event('system', 'Client connected')
    emit('response', {'message': 'مرحباً في لوحة التحكم'})

def main():
    print("\n" + "="*60)
    print("🌐 Robot Web Dashboard")
    print("="*60)
    print(f"\n🚀 Starting server...")
    print(f"📍 Open http://localhost:5000 in your browser")
    print(f"\n⌨️  Press Ctrl+C to stop\n")
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        print("✅ Dashboard stopped")

if __name__ == '__main__':
    main()
