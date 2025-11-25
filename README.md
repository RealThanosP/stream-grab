# **StreamGrab 📺🎵**

**StreamGrab** is a modern, lightweight graphical interface (GUI) for the powerful command-line tool yt-dlp. It allows you to easily download videos and extract audio from YouTube and other platforms without touching the terminal.

Built with Python and Tkinter, it features a threaded architecture to keep the interface responsive during large downloads.

## **✨ Features**

### **🎧 Audio Downloader**

* **Format Selection:** Convert to MP3, M4A, WAV, or FLAC.  
* **Quality Control:** Select bitrate/quality (0 is best).  
* **Smart Metadata:** Automatically embeds cover art (thumbnail) and ID3 tags (Artist, Title).

### **🎬 Video Downloader**

* **High Resolution:** Supports downloads up to 4K (2160p).  
* **Smart Container Merging:** Automatically merges the best video and audio streams into MP4 or MKV.  
* **Subtitles:** Option to download and embed English subtitles.  
* **Resolution Limiter:** "Best", "1080p", "720p" etc. — prevents accidental 8K downloads.

### **⚙️ General**

* **Live Log:** View real-time output from the downloader.  
* **Responsive UI:** Download process runs in a background thread so the app doesn't freeze.  
* **Cross-Platform:** Works on Windows, Linux, and macOS.

## **🛠️ Prerequisites**

Before running StreamGrab, ensure you have the following installed:

1. **Python 3.10+**  
2. **FFmpeg** (Crucial for MP3 conversion and merging high-res video)  
3. **Tkinter** (Usually included with Python, but requires manual install on some Linux distros)

### **How to install FFmpeg:**

* **Windows:** [Download here](https://ffmpeg.org/download.html), extract it, and add the bin folder to your System PATH.  
* **Ubuntu/Debian:** sudo apt install ffmpeg  
* **macOS:** brew install ffmpeg

## **🚀 Installation**

1. **Clone the repository:**  
   git clone \[https://github.com/YOUR\_USERNAME/StreamGrab.git\](https://github.com/YOUR\_USERNAME/StreamGrab.git)  
   cd StreamGrab

2. Install Python dependencies:  
   StreamGrab relies on yt-dlp.  
   pip install yt-dlp

3. **Run the application:**  
   python ytdlp\_gui.py

## **🐛 Troubleshooting**

### **Error: ModuleNotFoundError: No module named '\_tkinter'**

This is common on Linux (Ubuntu/Debian) if you installed Python manually or via minimal install.

* **Fix:** Run sudo apt-get install python3-tk

### **Error: "FFmpeg not found"**

If you see this warning, audio conversion will fail, and videos may download without sound.

* **Fix:** Ensure FFmpeg is installed and accessible via your terminal (type ffmpeg \-version to check). If on Windows, restart your computer after adding it to PATH.

## **🤝 Contributing**

Pull requests are welcome\! For major changes, please open an issue first to discuss what you would like to change.

## **📄 License**

This project is open source. Please ensure you comply with the yt-dlp license and the Terms of Service of the websites you download from.

**Disclaimer:** This tool is for educational purposes and personal archiving only. The creators are not responsible for copyright misuse.