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
- Measuring response times
- CLI output formatting
- Writing structured scan reports

It is **not** intended to replace professional security scanners.

---

## 🧪 How the Project Works

NX-TRACE is composed of two parts:

1. **A Flask test server**
   - Simulates common API behaviors
   - Runs locally on `http://localhost:8000`
   - Provides predictable endpoints for analysis

2. **The NX-TRACE scanner**
   - Sends requests to the test server
   - Analyzes responses
   - Displays results in the terminal
   - Generates a text report

This approach ensures the scans are:
- Safe
- Reproducible
- Fully authorized

---

## 🖥️ Test Server (Flask)

The test server simulates different real-world API scenarios.

### Available Endpoints

| Endpoint     | Behavior                          |
|--------------|-----------------------------------|
| `/`          | Server status message              |
| `/reservas` | 200 OK with JSON data              |
| `/usuarios` | 401 Unauthorized                   |
| `/admin`    | 403 Forbidden                      |
| `/slow`     | Slow response (2 seconds delay)    |
| `/notfound` | 404 Not Found                      |

The server exists **only for testing the scanner**.

---

## 🚀 Running the Project

### Requirements
- Python 3.6+
- pip

### 1️⃣ Install dependencies
```bash
pip install flask requests

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

The scanner reads endpoints from `endpoints.txt` and automatically scans the local server.

---

## 📄 Endpoints File

The scanner uses a simple text file:

```txt
/reservas
/usuarios
/admin
/slow
/notfound
```

Each line represents an endpoint to be tested.

---

## 🔍 What NX-TRACE Analyzes

For each endpoint, the scanner collects:

* HTTP status code
* Response time
* Response size
* Possible authentication requirement

Authentication is detected by:

* Status codes `401` and `403`
* `WWW-Authenticate` headers
* Common authentication keywords in the response body

---

## 📊 Output

### Terminal Output

* Colored status indicators
* Response times
* Authentication flags
* Summary statistics

### Report File

After the scan, a file named `report.txt` is generated containing:

* Scan date and target
* Per-endpoint results
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

It focuses on **understanding behavior**, not attacking systems.

---

## 🛡️ Ethical Use

NX-TRACE is meant to be used **only** on:

* The included test server
* Systems you own
* Systems you have explicit permission to test

Never scan public or private systems without authorization.

---

## 📚 What I Learned

Through this project, I practiced:

* Python scripting
* REST API behavior analysis
* CLI UX design
* Security-focused thinking
* Writing readable scan output
* Structuring a small security tool

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

Developed by **João**
Cybersecurity & Development enthusiast

Developed as a personal study project focused on cybersecurity fundamentals and defensive analysis.

---

> *“Security starts with visibility. Even simple tools can teach powerful lessons.”*

