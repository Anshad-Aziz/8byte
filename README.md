# 🧾 Receipt Manager

A Django-based web application for managing receipts. It includes features for uploading, parsing, editing, and visualizing receipt data. The app uses **Tesseract OCR** to extract information from images and PDFs, stores data in a **SQLite** database, and offers a modern, responsive UI built with **Tailwind CSS**.

---

## ✨ Features

- 📤 **Upload Receipts**: Upload `.jpg`, `.png`, `.pdf`, or `.txt` files.
- 🔍 **OCR Processing**: Automatically extract **vendor**, **date**, **amount**, and **category** using Tesseract OCR.
- 🔎 **Search & Sort**: Filter receipts by **vendor** or **category**, and sort by **date**, **amount**, or **vendor**.
- 📝 **Edit Receipts**: Modify details through an intuitive form.
- 📁 **Export CSV**: Download receipt data in CSV format.
- 📊 **Visualizations**: View **vendor distribution** and **monthly spend trends** using Chart.js.
- 🖥️ **Responsive UI**: Built with Tailwind CSS and animations for a modern experience.

---

## 📦 Prerequisites

- Python 3.8+
- Tesseract OCR (installed and added to PATH)
- Git
- Virtual environment (recommended)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/receipt-manager.git
cd receipt-manager
