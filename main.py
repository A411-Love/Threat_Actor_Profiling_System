import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import webbrowser
from osint.platform_check import check_platforms
from osint.footprint_analysis import analyze_footprint
#FAKE

def open_link(event):
    try:
        url = event.widget.get("current linestart", "current lineend").split(": ", 1)[1].strip()
        webbrowser.open(url)
    except:
        pass

def clear_all():
    entry_username.delete(0, tk.END)
    text_output.delete("1.0", tk.END)

def analyze_username():
    username = entry_username.get().strip()
        # Save search history
    with open("output/search_history.txt", "a") as history_file:
        history_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {username}\n")

    if not username:
        messagebox.showerror("Error", "Please enter a username")
        return

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, "🔎 Scanning platforms...\n")
    root.update()

    # Get platform data
    platforms_found, github_repos = check_platforms(username)

    # Analyze footprint
    profile = analyze_footprint(platforms_found, github_repos, username)

    text_output.delete("1.0", tk.END)

    # 🚨 Known Threat Actor Warning (RED)
    if profile.get("known_actor"):
        text_output.insert(tk.END, "⚠ KNOWN THREAT ACTOR DETECTED ⚠\n\n", "alert")

    # Build platform list
    platforms_text = ""
    for name, url in profile['platforms'].items():
        platforms_text += f"{name}: {url}\n"

    text_output.insert(tk.END, f"Username: {username}\n\n", "header")
    text_output.insert(tk.END, f"Platforms Found ({profile['platform_count']}):\n", "subheader")
    text_output.insert(tk.END, platforms_text + "\n")

    # Risk coloring
    if profile['risk'] == "LOW RISK":
        risk_color = "#00ff99"
    elif profile['risk'] == "MEDIUM RISK":
        risk_color = "#ffcc00"
    else:
        risk_color = "#ff4d4d"

    text_output.insert(tk.END, "Risk Level: ", "subheader")
    text_output.insert(tk.END, f"{profile['risk']}\n", ("risk",))
    text_output.insert(tk.END, f"Skill Level: {profile['skill_level']}\n")

    # Tag styling
    text_output.tag_config("alert", foreground="#ff0000", font=("Consolas", 14, "bold"))
    text_output.tag_config("subheader", foreground="#00ccff", font=("Consolas", 12, "bold"))
    text_output.tag_config("risk", foreground=risk_color, font=("Consolas", 12, "bold"))

    text_output.tag_configure("link", foreground="#3399ff", underline=True)
    start = text_output.search("https://", "1.0", tk.END)
    while start:
        end = text_output.search("\n", start, tk.END)
        if not end:
            end = tk.END
        text_output.tag_add("link", start, end)
        start = text_output.search("https://", end, tk.END)
    text_output.tag_bind("link", "<Button-1>", open_link)

    # Save report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("output/profile_report.txt", "w") as f:
        f.write(f"Threat Actor Profiling Report\nScan Time: {timestamp}\n")
        f.write("----------------------------------\n")
        f.write(f"Username: {username}\n")
        f.write(f"Platforms Found ({profile['platform_count']}):\n{platforms_text}\n")
        f.write(f"Risk Level: {profile['risk']}\n")
        f.write(f"Skill Level: {profile['skill_level']}\n")


def show_history():
    try:
        with open("output/search_history.txt", "r") as history_file:
            history_data = history_file.read()
    except FileNotFoundError:
        history_data = "No search history found."

    history_window = tk.Toplevel(root)
    history_window.title("Search History")
    history_window.geometry("600x400")
    history_window.configure(bg="#1e1e1e")

    tk.Label(history_window,
             text="Search History",
             bg="#1e1e1e",
             fg="#00ffff",
             font=("Consolas", 16, "bold")).pack(pady=10)

    text_history = tk.Text(history_window,
                           height=18,
                           width=70,
                           font=("Consolas", 11),
                           bg="#121212",
                           fg="white")
    text_history.pack(pady=10)

    text_history.insert(tk.END, history_data)
    text_history.config(state="disabled")


root = tk.Tk()
root.title("Threat Actor Profiling System (OSINT)")
root.geometry("750x550")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

tk.Label(root, text="Threat Actor Profiling System",
         bg="#1e1e1e", fg="#00ffff",
         font=("Consolas", 20, "bold")).pack(pady=15)

frame_input = tk.Frame(root, bg="#1e1e1e")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Enter Username:",
         bg="#1e1e1e", fg="white",
         font=("Consolas", 12)).pack(side=tk.LEFT, padx=10)

entry_username = tk.Entry(frame_input, width=30,
                          font=("Consolas", 12),
                          bg="#2d2d2d", fg="white",
                          insertbackground="white")
entry_username.pack(side=tk.LEFT)

frame_buttons = tk.Frame(root, bg="#1e1e1e")
frame_buttons.pack(pady=10)


tk.Button(frame_buttons, text="Analyze",
          command=analyze_username,
          bg="#00cc66", fg="black",
          font=("Consolas", 11, "bold"),
          width=15).pack(side=tk.LEFT, padx=15)

tk.Button(frame_buttons, text="History",
          command=show_history,
          bg="#3399ff", fg="black",
          font=("Consolas", 11, "bold"),
          width=15).pack(side=tk.LEFT, padx=15)

tk.Button(frame_buttons, text="Clear",
          command=clear_all,
          bg="#cc3333", fg="white",
          font=("Consolas", 11, "bold"),
          width=15).pack(side=tk.LEFT, padx=15)


frame_output = tk.Frame(root, bg="#1e1e1e")
frame_output.pack(pady=15)

scrollbar = tk.Scrollbar(frame_output)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(frame_output,
                      height=20, width=85,
                      font=("Consolas", 11),
                      bg="#121212", fg="white",
                      yscrollcommand=scrollbar.set)
text_output.pack()

scrollbar.config(command=text_output.yview)

root.mainloop()
