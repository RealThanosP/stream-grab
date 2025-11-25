import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import shutil

APP_NAME = "StreamGrab"

class AudioTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        
        # --- Styles ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10), padding=5)
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))

        # --- Main Container ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        # --- Header ---
        header = ttk.Label(main_frame, text="Audio Downloader", style='Header.TLabel')
        header.pack(pady=(0, 20))

        # --- URL Section ---
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(url_frame, text="Video URL:").pack(anchor="w")
        self.url_entry = ttk.Entry(url_frame, font=('Helvetica', 11))
        self.url_entry.pack(fill="x", pady=5, ipady=3)

        # --- Audio Options ---
        options_frame = ttk.LabelFrame(main_frame, text="Audio Options", padding="10")
        options_frame.pack(fill="x", pady=(0, 20))

        # Row 1: Format & Quality
        ttk.Label(options_frame, text="Format:").grid(row=0, column=0, sticky="w", padx=5)
        self.format_var = tk.StringVar(value="mp3")
        self.format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, state="readonly", width=10)
        self.format_combo['values'] = ('mp3', 'm4a', 'wav', 'flac', 'best')
        self.format_combo.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(options_frame, text="Quality (0=Best):").grid(row=0, column=2, sticky="w", padx=5)
        self.quality_var = tk.StringVar(value="0")
        self.quality_spin = ttk.Spinbox(options_frame, from_=0, to=10, textvariable=self.quality_var, width=5)
        self.quality_spin.grid(row=0, column=3, sticky="w", padx=5)

        # Row 2: Extras
        self.meta_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Add Metadata", variable=self.meta_var).grid(row=1, column=0, sticky="w", padx=5, pady=10)

        self.thumb_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Embed Thumbnail", variable=self.thumb_var).grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=10)

        # --- Download Button ---
        self.download_btn = ttk.Button(main_frame, text="Start Download", command=self.start_download_thread)
        self.download_btn.pack(pady=(0, 10), fill="x")

        # --- Status Log ---
        self.status_text = tk.Text(main_frame, height=8, width=50, font=("Consolas", 9), state="disabled", bg="#f0f0f0")
        self.status_text.pack(fill="both", expand=True)

    def log(self, message):
        self.after(0, self._log_internal, message)

    def _log_internal(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
        self.status_text.config(state="disabled")

    def toggle_inputs(self, enable):
        state = "normal" if enable else "disabled"
        self.download_btn.config(state=state)
        self.url_entry.config(state=state)

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a valid URL.")
            return

        self.toggle_inputs(False)
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, "end")
        self.status_text.config(state="disabled")
        threading.Thread(target=self.run_download, args=(url,), daemon=True).start()

    def run_download(self, url):
        cmd = ["yt-dlp", "-x"] # Audio only
        cmd.extend(["--audio-format", self.format_var.get()])
        cmd.extend(["--audio-quality", self.quality_var.get()])
        
        if self.meta_var.get():
            cmd.append("--add-metadata")
        if self.thumb_var.get():
            cmd.append("--embed-thumbnail")
        
        cmd.append(url)
        self.execute_command(cmd)

    def execute_command(self, cmd):
        self.log(f"Running command:\n{' '.join(cmd)}\n")
        self.log("Downloading... please wait.")
        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            for line in process.stdout:
                self.log(line.strip())
            process.wait()
            if process.returncode == 0:
                self.log("\n✅ Download Complete!")
                messagebox.showinfo("Success", "Download finished successfully!")
            else:
                self.log(f"\n❌ Error: Exit code {process.returncode}")
                messagebox.showerror("Error", "Download failed.")
        except Exception as e:
            self.log(f"\n❌ Exception: {str(e)}")
        finally:
            self.after(0, self.toggle_inputs, True)


class VideoTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        header = ttk.Label(main_frame, text="Video Downloader", style='Header.TLabel')
        header.pack(pady=(0, 20))

        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(url_frame, text="Video URL:").pack(anchor="w")
        self.url_entry = ttk.Entry(url_frame, font=('Helvetica', 11))
        self.url_entry.pack(fill="x", pady=5, ipady=3)

        options_frame = ttk.LabelFrame(main_frame, text="Video Options", padding="10")
        options_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(options_frame, text="Max Resolution:").grid(row=0, column=0, sticky="w", padx=5)
        self.res_var = tk.StringVar(value="Best")
        self.res_combo = ttk.Combobox(options_frame, textvariable=self.res_var, state="readonly", width=12)
        self.res_combo['values'] = ('Best', '4K (2160p)', '1440p', '1080p', '720p', '480p')
        self.res_combo.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(options_frame, text="Container:").grid(row=0, column=2, sticky="w", padx=5)
        self.format_var = tk.StringVar(value="mp4")
        self.format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, state="readonly", width=10)
        self.format_combo['values'] = ('mp4', 'mkv', 'webm')
        self.format_combo.grid(row=0, column=3, sticky="w", padx=5)

        self.subs_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Download Subtitles", variable=self.subs_var).grid(row=1, column=0, sticky="w", padx=5, pady=10)

        self.thumb_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Embed Thumbnail", variable=self.thumb_var).grid(row=1, column=1, sticky="w", padx=5, pady=10)

        self.meta_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Add Metadata", variable=self.meta_var).grid(row=1, column=2, columnspan=2, sticky="w", padx=5, pady=10)

        self.download_btn = ttk.Button(main_frame, text="Start Download", command=self.start_download_thread)
        self.download_btn.pack(pady=(0, 10), fill="x")

        self.status_text = tk.Text(main_frame, height=8, width=50, font=("Consolas", 9), state="disabled", bg="#f0f0f0")
        self.status_text.pack(fill="both", expand=True)

    def log(self, message):
        self.after(0, self._log_internal, message)

    def _log_internal(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
        self.status_text.config(state="disabled")

    def toggle_inputs(self, enable):
        state = "normal" if enable else "disabled"
        self.download_btn.config(state=state)
        self.url_entry.config(state=state)

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a valid URL.")
            return

        self.toggle_inputs(False)
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, "end")
        self.status_text.config(state="disabled")
        threading.Thread(target=self.run_download, args=(url,), daemon=True).start()

    def run_download(self, url):
        cmd = ["yt-dlp"]
        
        # Resolution
        res_selection = self.res_var.get()
        if res_selection != "Best":
            height = res_selection.split()[0].replace('p', '')
            fmt_str = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
            cmd.extend(["-f", fmt_str])
        
        # Container
        cmd.extend(["--merge-output-format", self.format_var.get()])

        if self.subs_var.get():
            cmd.extend(["--write-auto-sub", "--sub-lang", "en", "--embed-subs"])
        if self.meta_var.get():
            cmd.append("--add-metadata")
        if self.thumb_var.get():
            cmd.append("--embed-thumbnail")

        cmd.append(url)
        self.execute_command(cmd)

    def execute_command(self, cmd):
        self.log(f"Running command:\n{' '.join(cmd)}\n")
        self.log("Downloading... please wait.")
        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            for line in process.stdout:
                self.log(line.strip())
            process.wait()
            if process.returncode == 0:
                self.log("\n✅ Download Complete!")
                messagebox.showinfo("Success", "Video downloaded successfully!")
            else:
                self.log(f"\n❌ Error: Exit code {process.returncode}")
                messagebox.showerror("Error", "Download failed.")
        except Exception as e:
            self.log(f"\n❌ Exception: {str(e)}")
        finally:
            self.after(0, self.toggle_inputs, True)


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("650x550")
        
        # Dependency Checks
        if not shutil.which("yt-dlp"):
            messagebox.showerror("Error", "yt-dlp is not installed.\nPlease run: pip install yt-dlp")
            root.destroy()
            return
        
        if not shutil.which("ffmpeg"):
            messagebox.showwarning("Warning", "FFmpeg not found!\n\n- Audio conversion (mp3) will fail.\n- High-res video (1080p+) will lack audio.\n\nPlease install FFmpeg and add it to PATH.")

        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.audio_tab = AudioTab(self.notebook)
        self.video_tab = VideoTab(self.notebook)

        self.notebook.add(self.audio_tab, text="  Audio Download  ")
        self.notebook.add(self.video_tab, text="  Video Download  ")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()