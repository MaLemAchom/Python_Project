# Python_Project
🕸️ Web Scraping with Python – Flipkart Mobile Data
📌 Overview

This project demonstrates web scraping using Python to collect structured product data from Flipkart. Using Requests and BeautifulSoup, the scraper extracts product details such as name, price, description, and reviews across multiple pages. The data is cleaned, processed with pandas, and exported into CSV format for analysis.

🚀 Features

Scrapes Flipkart product listings (mobiles under ₹50,000).

Extracts product Name, Price, Description, and Reviews.

Cleans and structures raw HTML into tabular data.

Processes and analyzes 2,000+ product records.

Exports results into CSV for easy use in analytics pipelines.

🛠 Tech Stack

Python

Requests – for sending HTTP requests

BeautifulSoup – for parsing HTML

pandas – for cleaning and exporting data

📂 Output

flipkart_mobiles_under_50000.csv → contains all extracted records with clean fields

👨‍💻 Face Recognition Attendance System
📌 Overview

A real-time face recognition-based attendance system built with Python and OpenCV. The system detects and recognizes faces using the face_recognition (dlib) library, and automatically logs attendance by storing recognized names with timestamps in a CSV file.

🚀 Features

Real-time face detection & recognition using OpenCV and dlib.

Supports multiple faces simultaneously.

Logs name + timestamp when a face is recognized.

Stores attendance in a CSV file for record-keeping.

Can be adapted for classrooms, offices, and events.

🛠 Tech Stack

Python

OpenCV – for real-time face detection

dlib / face_recognition – for face encoding & recognition

NumPy – for data handling

CSV – for attendance storage

📂 Output

attendance.csv → contains names of recognized individuals with corresponding timestamps
