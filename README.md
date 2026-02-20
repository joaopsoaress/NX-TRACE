# 👁️ NX-TRACE — Network Endpoint Security Scanner

> A small Python tool created for learning and practicing basic REST API security analysis in a controlled environment.

NX-TRACE is a **student project** focused on understanding how REST endpoints behave under different conditions, such as authentication requirements, slow responses, and missing routes.

The scanner is designed to run **locally** against a **test server included in the project**, allowing safe and ethical experimentation.

---

## 📌 Project Goal

The main goal of NX-TRACE is educational.

This project helped me practice:
- HTTP requests and status codes
- Basic security analysis concepts
- Detecting authentication-protected endpoints
- **Automatic endpoint discovery using wordlists**
- Measuring response times
- CLI output formatting
- Writing structured scan reports
- **JSON response data extraction and analysis**

It is **not** intended to replace professional security scanners.

---

## 🧪 How the Project Works

NX-TRACE is composed of two parts:

1. **A Flask test server**
   - Simulates common API behaviors
   - Runs locally on `http://localhost:8000`
   - Provides predictable endpoints for analysis
   - **Includes a dedicated `/api/test` endpoint with structured JSON data**

2. **The NX-TRACE scanner**
   - Sends requests to the test server
   - Analyzes responses
   - **Automatically discovers endpoints using a built-in wordlist**
   - **Updates the endpoints file with newly discovered paths**
   - **Extracts and displays JSON response data**
   - Displays results in the terminal
   - Generates a detailed text report

This approach ensures the scans are:
- Safe
- Reproducible
- Fully authorized

---

## 🖥️ Test Server (Flask)

The test server simulates different real-world API scenarios.

### Available Endpoints

| Endpoint       | Behavior                           | Response Data                     |
|----------------|------------------------------------|-----------------------------------|
| `/`            | Server status message              | Simple message                    |
| `/api/test`    | 200 OK with programming info       | JSON with languages and versions  |
| `/reservations`| 200 OK with reservation data       | List of reservations              |
| `/users`       | 401 Unauthorized                   | Authentication error message      |
| `/admin`       | 403 Forbidden                      | Access denied message             |
| `/slow`        | Slow response (2 seconds delay)    | Simple message                    |
| `/notfound`    | 404 Not Found                      | Error page                        |

The server exists **only for testing the scanner**.

---

## 🚀 Running the Project

### Requirements
- Python 3.6+
- pip

### 1️⃣ Install dependencies
```bash
pip install flask requests
```

### 2️⃣ Start the test server
```bash
python test_server.py
```

The server will run at:
```
http://localhost:8000
```

### 3️⃣ Run the scanner
```bash
python scanner.py
```

The scanner will ask if you want to enable automatic endpoint discovery before starting the scan.

---

## 🔍 What NX-TRACE Analyzes

For each endpoint, the scanner collects:

* HTTP status code
* Response time
* Response size
* Possible authentication requirement
* **JSON response data (when available)**

Authentication is detected by:
* Status codes `401` and `403`
* `WWW-Authenticate` headers
* Common authentication keywords in the response body

---

## 🎯 New Features in v1.5

### 🔎 Automatic Endpoint Discovery
The scanner now includes a built-in wordlist to automatically discover endpoints:

- Tests common paths like `/admin`, `/api`, `/users`, `/login`
- Tries variations like `/api/test`, `/v1/users`, `/rest/api`
- Shows real-time results when endpoints are found
- **Automatically updates `endpoints.txt` with new discoveries**
- Creates backups of the original file before updating

### 📦 JSON Response Analysis
When an endpoint returns JSON data, the scanner now:

- Extracts and stores the structured data
- Includes the full response in the generated report
- Provides better insight into API responses

### 📊 Enhanced Reporting
The `report.txt` file now includes:

- Complete JSON response data for applicable endpoints
- Better formatting and organization
- Detailed endpoint information

---

## 📄 Endpoints File

The scanner uses a simple text file:

```txt
/reservations
/users
/admin
/slow
/notfound
/api/test
```

Each line represents an endpoint to be tested. **The file is automatically updated when new endpoints are discovered!**

---

## 📊 Output

### Terminal Output
* Colored status indicators
* Response times
* Authentication flags
* **Real-time endpoint discovery feedback**
* Summary statistics

### Report File
After the scan, a file named `report.txt` is generated containing:

* Scan date and target
* Per-endpoint results
* **Full JSON response data (when available)**
* Errors (if any)
* Basic statistics

---

## ⚠️ Limitations

This project intentionally keeps things simple:

* No concurrency
* No authentication bypass attempts
* No vulnerability exploitation
* No external targets
* No HTTPS or certificate analysis
* **Basic wordlist-based discovery (not exhaustive)**

It focuses on **understanding behavior**, not attacking systems.

---

## 🛡️ Ethical Use

NX-TRACE is meant to be used **only** on:

* The included test server
* Systems you own
* Systems you have explicit permission to test

Never scan public or private systems without authorization.

---

## 🔧 Configuration

The scanner can be easily configured by modifying:

- `BASE_URL` in `scanner.py` - Change the target URL
- `wordlist` in the `discover_endpoints()` function - Add/remove discovery paths
- `HEADERS` - Customize request headers

---

## 📁 File Structure

```
NX-TRACE/
├── scanner.py          # Main scanner with discovery features
├── test_server.py      # Flask test server
├── endpoints.txt       # List of endpoints to scan (auto-updated)
├── report.txt          # Generated scan report
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

---

## 🎓 Learning Outcomes

By using NX-TRACE, you'll learn about:

1. **HTTP fundamentals** - Status codes, headers, methods
2. **API structure** - Common endpoint patterns
3. **Authentication** - How servers indicate protected resources
4. **Response analysis** - Parsing and understanding JSON data
5. **Automation** - Building tools to discover and test endpoints
6. **File I/O** - Reading/writing files, creating backups
7. **Error handling** - Dealing with timeouts and connection issues

---

## 🤝 Contributing

This is a personal learning project, but feel free to fork and experiment! Some ideas for improvements:

- Add more sophisticated discovery techniques
- Implement concurrent scanning
- Add support for authentication tokens
- Create a web dashboard for results
- Export reports in JSON/HTML format

---

## 📝 Changelog

### v1.5
- Added automatic endpoint discovery with wordlist
- Implemented JSON response data extraction
- Enhanced report generation with full response data
- Added backup system for endpoints file
- Improved visual feedback during discovery

### v1.0
- Initial release
- Basic endpoint scanning
- Simple report generation
- Authentication detection