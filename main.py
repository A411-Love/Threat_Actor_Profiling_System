import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import webbrowser
from osint.platform_check import check_platforms
from osint.footprint_analysis import analyze_footprint

# Function to open URLs in browser
def open_link(event):
    try:
        url = event.widget.get("current linestart", "current lineend").split(": ", 1)[1].strip()
        webbrowser.open(url)
    except IndexError:
        pass

# Function to clear input and output
def clear_all():
    entry_username.delete(0, tk.END)
    text_output.delete("1.0", tk.END)

# Main analysis function
def analyze_username():
    username = entry_username.get().strip()
    if not username:
        messagebox.showerror("Error", "Please enter a username")
        return

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "Checking platforms...\n")
    root.update()  # Update GUI to show status

    platforms_found = check_platforms(username)
    profile = analyze_footprint(platforms_found)

    # Format platforms with URLs
    platforms_text = ""
    for name, url in profile['platforms'].items():
        platforms_text += f"{name}: {url}\n"

    # Insert final result
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, f"Username: {username}\n\n")
    text_output.insert(tk.END, f"Platforms Found ({profile['platform_count']}):\n{platforms_text}\n")
    text_output.insert(tk.END, f"Risk Level: {profile['risk']}\n")
    text_output.insert(tk.END, f"Skill Level: {profile['skill_level']}\n")

    # Make URLs clickable
    text_output.tag_configure("link", foreground="blue", underline=True)
    start_index = text_output.search("https://", "1.0", tk.END)
    while start_index:
        end_index = text_output.search("\n", start_index, tk.END)
        if not end_index:
            end_index = tk.END
        text_output.tag_add("link", start_index, end_index)
        start_index = text_output.search("https://", end_index, tk.END)
    text_output.tag_bind("link", "<Button-1>", open_link)

    # Save report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("output/profile_report.txt", "w") as f:
        f.write(f"Threat Actor Profiling Report\nScan Time: {timestamp}\n")
        f.write("-----------------------------\n")
        f.write(f"Username: {username}\n")
        f.write(f"Platforms Found ({profile['platform_count']}):\n{platforms_text}\n")
        f.write(f"Risk Level: {profile['risk']}\n")
        f.write(f"Skill Level: {profile['skill_level']}\n")

    text_output.insert(tk.END, f"\nReport saved to output/profile_report.txt\n")

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Threat Actor Profiling System (OSINT)")
root.geometry("600x500")
root.resizable(False, False)

# Title
tk.Label(root, text="Threat Actor Profiling System", font=("Arial", 18, "bold")).pack(pady=10)

# Input frame
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Enter Username:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
entry_username = tk.Entry(frame_input, width=35, font=("Arial", 12))
entry_username.pack(side=tk.LEFT)

# Buttons frame
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

tk.Button(frame_buttons, text="Analyze", width=20, command=analyze_username).pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons, text="Clear", width=20, command=clear_all).pack(side=tk.LEFT, padx=10)

# Output Text Box
text_output = tk.Text(root, height=18, width=70, font=("Arial", 11))
text_output.pack(pady=10)

# Run GUI
root.mainloop()
