import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from moviepy.editor import VideoFileClip
from tkinter import ttk

def browse_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    video_file_entry.delete(0, tk.END)
    video_file_entry.insert(0, file_path)

def browse_save_location():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Audio files", "*.mp3;*.wav")])
    save_location_entry.delete(0, tk.END)
    save_location_entry.insert(0, file_path)

def reset_fields():
    video_file_entry.delete(0, tk.END)
    save_location_entry.delete(0, tk.END)
    mp3_radio_button.select()

def convert_to_audio():
    video_file = video_file_entry.get()
    save_location = save_location_entry.get()
    output_format = output_format_var.get()

    if not os.path.isfile(video_file):
        messagebox.showerror("Error", "Please select a valid video file.")
        return

    if not save_location:
        messagebox.showerror("Error", "Please select a valid saving location.")
        return

    try:
        video_clip = VideoFileClip(video_file)

        if not video_clip.audio:
            raise ValueError("Error: No audio stream found in the video file.")

        audio_clip = video_clip.audio
        output_file = save_location if save_location.endswith(f".{output_format}") else f"{save_location}.{output_format}"
        audio_clip.write_audiofile(output_file)
        audio_clip.close()

        messagebox.showinfo("Success", "Conversion completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main GUI window
app = tk.Tk()
app.title("Video to Audio Converter")

# Set the window size and make it non-resizable
app.geometry("500x200")
app.resizable(False, False)

# Disable maximize button
app.attributes('-topmost', True)

# Apply a modern theme to the GUI
style = ttk.Style(app)
style.theme_use("clam")

# Create a frame to group elements
frame = ttk.Frame(app, padding="20")
frame.grid(row=0, column=0)

# GUI elements with improved styling
video_file_entry = ttk.Entry(frame, width=50)
video_file_entry.grid(row=0, column=0, padx=10, pady=5, columnspan=2, sticky="ew")
browse_video_button = ttk.Button(frame, text="Browse Video", command=browse_video_file)
browse_video_button.grid(row=0, column=2, padx=5, pady=5)

save_location_entry = ttk.Entry(frame, width=50)
save_location_entry.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky="ew")
browse_save_location_button = ttk.Button(frame, text="Browse Save Location", command=browse_save_location)
browse_save_location_button.grid(row=1, column=2, padx=5, pady=5)

output_format_var = tk.StringVar(app)
output_format_var.set("mp3")
mp3_radio_button = ttk.Radiobutton(frame, text="MP3", variable=output_format_var, value="mp3")
mp3_radio_button.grid(row=2, column=0, padx=10, pady=5)
wav_radio_button = ttk.Radiobutton(frame, text="WAV", variable=output_format_var, value="wav")
wav_radio_button.grid(row=2, column=1, padx=10, pady=5)

convert_button = ttk.Button(frame, text="Convert to Audio", command=convert_to_audio)
convert_button.grid(row=3, column=0, padx=5, pady=10, columnspan=3, sticky="ew")

reset_button = ttk.Button(frame, text="New", command=reset_fields)
reset_button.grid(row=4, column=0, padx=5, pady=10, columnspan=3, sticky="ew")

app.mainloop()
