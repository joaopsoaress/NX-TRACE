# 👁️ NX-TRACE

> **NX-TRACE** is a simple network endpoint scanner written in Python.
> It was developed as a **learning project** focused on understanding how REST APIs respond to unauthenticated requests and how basic security indicators can be identified.

> This tool scans local endpoints and reports response status, response time, payload size and basic signs of authentication requirements.

> ⚠️ This project is intended for **educational and defensive purposes only**.

---

## ✨ Features

What NX-TRACE currently does:

* Reads a list of endpoints from a text file
* Sends HTTP GET requests to each endpoint
* Measures response time
* Displays HTTP status codes with visual indicators
* Detects **possible authentication requirements** using:

  * Status codes (401 / 403)
  * `WWW-Authenticate` headers
  * Common authentication-related keywords in responses
* Prints colored terminal output
* Generates a simple scan report (`report.txt`)

This is a **basic scanner**, not a full vulnerability assessment tool.

---

## 📂 Project Structure

```
nx-trace/
├── scanner.py
├── endpoints.txt
├── report.txt
└── README.md
```

---

## 🛠️ Requirements

* Python 3.8+
* `requests` library

Install dependency:

```bash
pip install requests
```

---

## 🚀 Usage

### 1. Start a local API server

(default target is `http://localhost:8000`)

### 2. Add endpoints to `endpoints.txt`, one per line

```
/users
/login
/admin
/api/data
```

### 3. Run the scanner

```bash
python scanner.py
```

The tool will:

* Clear the terminal
* Display the NX-TRACE banner
* Scan each endpoint
* Print results and summary
* Generate a `report.txt` file

---

## 📊 Output Example

* ✅ `200` responses shown in green
* 🔒 `401 / 403` responses highlighted as protected
* ⚠️ Other status codes flagged
* Authentication hints displayed when detected

A summary and a detailed table are printed at the end of the scan.

---

## 📄 Report File

After the scan, NX-TRACE generates `report.txt` containing:

* Scan date and target URL
* Number of endpoints scanned
* Success and failure count
* Average response time
* Per-endpoint details:

  * Status code
  * Response time
  * Content size
  * Authentication detection

This report is meant for **manual review and learning**, not automated compliance.

---

## ⚠️ Limitations

This project **does not** currently include:

* Authentication bypass attempts
* POST, PUT or DELETE requests
* Token handling
* Async or concurrent scanning
* Vulnerability exploitation
* Deep payload analysis

Authentication detection is **heuristic-based** and may produce false positives.

---

## 🎓 Learning Goals

This project was created to practice:

* HTTP request handling
* Basic API security concepts
* Terminal UI formatting
* Error handling
* Writing readable security-related code
* Producing clear scan reports

---

## 🛡️ Ethical Use

* Scan **only systems you own or have permission to test**
* Do not use this tool for unauthorized access
* This project is educational and defensive in nature

---

## 📜 License

MIT License

---

## 👤 Author

Developed by **João**
Cybersecurity & Development enthusiast
