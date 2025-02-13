# **Trackable Request Logger**

This Python program provides an **enhanced HTTP request logger** with **response tracking**, **error handling**, and an **exportable HTML report** featuring a **modern timeline layout**. The requests and headers are structured **consistently**, making it easy to **analyze API interactions**.

---

## **📌 Features**
- ✅ **Track HTTP Requests** (GET, POST, PUT, PATCH, DELETE)
- ✅ **Log Response Time & Request Timestamps**
- ✅ **Export API Logs to an HTML Report**
- ✅ **Modern Timeline UI for Requests**
- ✅ **Headers & Requests Displayed in a Unified Layout**

---

## **📥 Installation**
1. **Clone this repository** or download the script.
2. **Install required dependencies**:
   ```bash
   pip install requests
   ```
3. **Run the program**:
   ```bash
   python your_script.py
   ```

---

## **🚀 How to Use**
### **1️⃣ Initialize the Request Logger**
```python
from trackable_requests import trackable_request

request_logger = trackable_request()
request_logger.headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "User-Agent": "CustomLogger/1.0"
}
```

### **2️⃣ Make API Calls**
```python
response = request_logger.get("https://jsonplaceholder.typicode.com/posts/1")
print(response)
```

### **3️⃣ Export Requests to an HTML Report**
```python
request_logger.export_html("request_log.html")
```

---

## **🖥️ HTML Report Overview**
- **Headers** are displayed at the top in a structured card.
- **Requests appear in a timeline view** for easy tracking.
- **Timestamps and response times are logged** for performance analysis.
- **Errors are displayed only if they occur**.

---

## **📌 Example Report Screenshot**
![Report Example Screenshot](https://github.com/user-attachments/assets/1573b035-9080-447b-a7ae-48cf4009cdc0)

---

## **🛠️ Configuration**
- To redact the header `Authorization` in the report, set `redact_authorization_header=True`:
  ```python
  request_logger.export_html("request_log.html", redact_authorization_header=True)
  ```
---

## **📂 Project Structure**
```
/your_project
│── trackable_requests.py   # Main request logging class
│── example_script.py       # Example usage script
│── request_log.html        # Generated HTML report
│── README.md               # This file
```

---

### **🚀 Now you can easily track and visualize your API requests with an intuitive report!**
