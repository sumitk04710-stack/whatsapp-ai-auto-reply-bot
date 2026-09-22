# WhatsApp AI Auto Reply Chatbot 🤖

An AI-powered WhatsApp automation bot that detects incoming WhatsApp messages using OCR, generates intelligent replies using Google Gemini, and automatically sends the reply through WhatsApp Web.

## 🚀 Features

- 📱 WhatsApp Web automation
- 🔍 Automatic message detection using OCR
- 🧠 AI-generated replies using Google Gemini
- ⌨️ Automatic message typing
- 🛑 Bot pauses when WhatsApp is inactive
- 🔐 API key stored using environment variables
- 🐍 Built with Python

## 🛠️ Technologies Used

- Python
- PyAutoGUI
- Tesseract OCR
- Google Gemini API
- python-dotenv
- WhatsApp Web

## 🔄 How It Works

```text
WhatsApp Web
     ↓
Screenshot
     ↓
Tesseract OCR
     ↓
Detect Incoming Message
     ↓
Google Gemini
     ↓
AI-generated Reply
     ↓
PyAutoGUI
     ↓
WhatsApp Message Sent