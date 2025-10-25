# Arachnida

A Python toolkit for web scraping and image metadata analysis, consisting of two main tools: **Spider** (web image scraper) and **Scorpion** (EXIF metadata extractor).

## 📋 Table of Contents

- [Overview](#overview)
- [Tools](#tools)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Examples](#examples)
- [Project Structure](#project-structure)

## 🕷️ Overview

Arachnida is a cybersecurity-focused project that provides tools for:
- Web scraping and downloading images from websites
- Extracting and analyzing EXIF metadata from images
- Anonymizing images by removing metadata

This project is part of the 42 Cyber Pool curriculum and demonstrates skills in web scraping, image processing, and metadata analysis.

## 🛠️ Tools

### Spider
A web scraper that downloads images from websites with support for recursive crawling.

### Scorpion
An EXIF metadata extractor that analyzes image files and optionally anonymizes them.

## 📦 Installation

### Prerequisites
- Python 3.x
- `exiftool` (for anonymization feature)

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd 42-CyberPool-Arachnida
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv arachnide
source arachnide/bin/activate
```

3. **Install dependencies:**
```bash
# Spider dependencies
pip install requests beautifulsoup4

# Scorpion dependencies
pip install Pillow exif
```

4. **Install exiftool (for anonymization):**
```bash
sudo apt install libimage-exiftool-perl
```

5. **Create data directory:**
```bash
mkdir data
```

## 🚀 Usage

### Spider - Web Image Scraper

Download images from a website:

```bash
python3 spider.py [URL]
```

#### Options:
- `-r, --recursive`: Enable recursive download
- `-l, --length [DEPTH]`: Maximum depth level for recursive download (default: 5)
- `-p, --path [PATH]`: Download directory path (default: data/)
- `-d, --domain`: Stay on the same domain during recursive crawling

#### Examples:
```bash
# Basic image download
python3 spider.py https://example.com

# Recursive download with custom depth and path
python3 spider.py -r -l 3 -p ./images/ https://example.com

# Recursive download staying on same domain
python3 spider.py -r -d https://example.com
```

### Scorpion - EXIF Metadata Extractor

Analyze images in a directory:

```bash
python3 scorpion.py
```

#### Options:
- `-p, --path [PATH]`: Directory containing images (default: ./data/)
- `-a, --anonimize`: Remove EXIF data from images (creates anonymized copies)

#### Examples:
```bash
# Analyze images in default directory
python3 scorpion.py

# Analyze images in custom directory
python3 scorpion.py -p ./my_images/

# Analyze and anonymize images
python3 scorpion.py -a
```

## ✨ Features

### Spider Features:
- ✅ Downloads images in supported formats (JPG, JPEG, PNG, GIF, BMP)
- 🔄 Recursive website crawling
- 🌐 Domain restriction option
- 📁 Custom save directory
- 🛡️ Error handling for network issues
- 📊 Progress indicators with emojis

### Scorpion Features:
- 📸 Comprehensive EXIF data extraction
- 🗂️ Categorized metadata display:
  - 📱 Device information
  - ⏰ DateTime metadata
  - 📸 Camera settings
  - 🌍 GPS geolocation data
  - ⚙️ Technical specifications
- 🌍 GPS coordinate formatting (DMS and decimal)
- 🗺️ Google Maps links for GPS data
- 🎨 Colorized terminal output
- 🔒 Image anonymization (EXIF removal)

### Supported Image Formats:
- JPEG/JPG
- PNG
- GIF
- BMP

## 📊 Metadata Categories

Scorpion organizes EXIF data into the following categories:

1. **Device Information**: Camera make, model, lens specifications
2. **DateTime Information**: Creation dates, timestamps, timezone data
3. **Camera Settings**: Aperture, exposure, ISO, flash settings
4. **Image Specifications**: Dimensions, resolution, color space
5. **GPS Information**: Location coordinates, altitude, timestamps
6. **Technical Metadata**: EXIF version, compression, etc.

## 📁 Project Structure

```
42-CyberPool-Arachnida/
├── spider.py              # Web image scraper
├── scorpion.py            # EXIF metadata extractor
├── README.md              # Project documentation
├── .gitignore            # Git ignore rules
├── en.subject.pdf        # Project subject (42 School)
├── data/                 # Downloaded images directory
└── arachnide/           # Python virtual environment
```

## 🔧 Environment Management

**Activate virtual environment:**
```bash
source arachnide/bin/activate
```

**Deactivate virtual environment:**
```bash
deactivate
```

## ⚠️ Important Notes

- Always respect website terms of service when scraping
- Be mindful of rate limiting and server load
- GPS data in images can reveal sensitive location information
- Anonymized images are created as separate files with `_anonymized` suffix
- The tool requires `exiftool` for the anonymization feature

## 🎯 Educational Purpose

This project is designed for educational purposes as part of cybersecurity training. It demonstrates:
- Web scraping techniques and best practices
- Image metadata analysis for digital forensics
- Privacy implications of image metadata
- Python programming for security tools

## 📜 License

This project is part of the 42 School curriculum and follows their academic guidelines.