# 🕵️‍♂️ HTTP(s) Proxy Interceptor

A Python-based HTTP proxy tool that allows manual interception, inspection, and forwarding of HTTP requests and responses through a simple GUI.

---

## 🔧 Features

- Intercepts incoming HTTP requests from clients
- Displays request/response in a user-friendly interface
- Allows manual forwarding to target servers or dropping traffic
- Supports multiple connections using multithreading
- Simple and responsive GUI built with Tkinter

---

## 🧱 Tech Stack

- **Language:** Python 3
- **Networking:** `socket`, `threading`
- **GUI:** `Tkinter`
- **Architecture:** Client-Proxy-Server (manual forward/drop control)

---

## 📥 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kushagra888/Http-s-Proxy-Interceptor.git
   cd Http-s-Proxy-Interceptor
   ```

2. No additional dependencies required! The project uses only Python standard libraries.

## 🚀 Usage

1. Start the proxy server:
   ```bash
   cd PythonProxyServer
   python main.py
   ```

2. The GUI will appear and the proxy will start listening on `127.0.0.1:8080`

3. Configure your browser to use the proxy:

   **Chrome/Edge:**
   - Settings → Search for "proxy" → Open system proxy settings
   - Manual proxy setup:
     - Address: `127.0.0.1`
     - Port: `8080`

   **Firefox:**
   - Settings → Network Settings
   - Manual proxy configuration:
     - HTTP Proxy: `127.0.0.1`
     - Port: `8080`
     - Check "Also use this proxy for HTTPS"

4. Test the proxy:
   - Visit http://example.com or http://neverssl.com
   - Watch the requests appear in the GUI
   - Use the buttons to:
     - "Forward to Server": Send request to target server
     - "Forward to Client": Send response back to browser
     - "Drop": Discard the request

## ⚠️ Notes

- Best suited for HTTP traffic inspection
- For HTTPS, you may see certificate warnings (normal for proxy interceptors)
- Remember to disable proxy settings in your browser after testing
- Default proxy address: `127.0.0.1:8080`

## 📝 License

This project is licensed under the terms of the LICENSE file included in the repository.
