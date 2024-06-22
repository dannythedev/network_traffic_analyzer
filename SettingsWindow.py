import tkinter as tk
from tkinter import messagebox
import json


class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.settings_window = tk.Toplevel(parent)
        self.settings_window.title("Settings")
        self.settings_window.configure(bg="#D9E3F1")

        self.keys_to_display = ['AbuseIPDB']  # Hardcoded list of keys to display
        self.api_keys = self.load_api_keys()
        self.create_widgets()

    def load_api_keys(self):
        try:
            with open('api_key.json', 'r') as f:
                api_keys = json.load(f)
        except FileNotFoundError:
            api_keys = {}
        return api_keys

    def create_widgets(self):
        self.api_key_entries = {}

        # Create table headers
        headers = ["Key Name", "API Key Value"]
        for col, header in enumerate(headers):
            label = tk.Label(self.settings_window, text=header, font=("Segoe UI", 10, "bold"), bg="#D9E3F1")
            label.grid(row=0, column=col, padx=10, pady=5)

        # Populate table with existing API keys that match keys_to_display
        row = 1
        for key_name in self.keys_to_display:
            key_name_label = tk.Label(self.settings_window, text=key_name, bg="#D9E3F1", relief=tk.FLAT, borderwidth=1)
            key_name_label.grid(row=row, column=0, padx=10, pady=5, sticky="nsew")

            if key_name in self.api_keys:
                key_value = self.api_keys[key_name]
            else:
                key_value = ""

            key_value_entry = tk.Entry(self.settings_window, bg="white", relief=tk.SOLID, borderwidth=1)
            key_value_entry.insert(tk.END, key_value)
            key_value_entry.grid(row=row, column=1, padx=10, pady=5, sticky="nsew")

            self.api_key_entries[key_name] = key_value_entry

            row += 1

        # Save Button
        save_button = tk.Button(self.settings_window, text="Save Settings", command=self.save_settings, bg="#43CC29",
                                fg="white", relief=tk.FLAT)
        save_button.grid(row=row, columnspan=2, padx=10, pady=10, sticky="nsew")

        PURPOSE_STRING = 'This program utilizes the AbuseIPDB API to retrieve data for external IPs selected from the process list. In cases where no API key is available, it falls back to using IPApi.com to gather the data. Please ensure you have an AbuseIPDB key specifically for abuse-related data.'
        # Label explaining the purpose of the program
        purpose_label = tk.Label(self.settings_window, text=PURPOSE_STRING, font=("Segoe UI", 8), bg="#D9E3F1",
                                 wraplength=400)
        purpose_label.grid(row=row + 1, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configure grid weights for layout responsiveness
        self.settings_window.grid_rowconfigure(row + 1, weight=1)
        self.settings_window.grid_columnconfigure(1, weight=1)

    def save_settings(self):
        updated_keys = {}
        for key_name, entry in self.api_key_entries.items():
            updated_keys[key_name] = entry.get()

        with open('api_key.json', 'w') as f:
            json.dump(updated_keys, f, indent=4)

        messagebox.showinfo("Settings", "Settings saved successfully.")
        self.settings_window.destroy()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsWindow(root)
    root.mainloop()
