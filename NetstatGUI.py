import tkinter as tk
from tkinter import messagebox, ttk
from Functions import validate_and_expand_ip, extract_ip
from NetstatProcessor import NetstatProcessor
from SettingsWindow import SettingsWindow


class NetstatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Traffic Analyzer")
        self.processor = NetstatProcessor()
        self.connections = []  # Store connections to allow sorting
        self.program_ips_dict = dict() # Dictionary to store program names and associated external IPs
        self.create_style()
        self.create_widgets()

    def create_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Normal state configuration
        style.configure("Treeview.Heading", background="#5B62F4", foreground="white", relief=tk.FLAT)

        # Hover state configuration (change hover background color to black)
        style.map("Treeview.Heading",
                  background=[("active", "#4F55C9")],
                  foreground=[("active", "white")])

        style.configure('Flat.Treeview', relief=tk.FLAT, background="#F0F5FA", foreground="#8599C8")
        # Define scrollbar style
        style.configure("Custom.Vertical.TScrollbar",
                        background="#8599C8",
                        troughcolor="#D9E3F1",
                        gripcount=0,
                        bordercolor="#D9E3F1",
                        darkcolor="#D9E3F1",
                        lightcolor="#D9E3F1")

    def create_widgets(self):
        # Create button to trigger netstat command
        self.get_button = tk.Button(self.root, text="Get Processes", command=self.on_get_processes,
                                    bg="#43CC29", fg="white", relief=tk.FLAT, height=2)
        self.get_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        # Apply style to the scrollbar
        self.result_scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, style="Custom.Vertical.TScrollbar")
        self.result_scrollbar.grid(row=1, column=2, sticky="ns", padx=2)

        # Treeview to display results in a table
        columns = (
            "Protocol", "Local Address", "Foreign Address", "Connection", "PID", "Program Name", "ISP", "Country",
            "Abuse"
        )
        widths = (60, 140, 140, 100, 40, 100, 100, 95, 60)
        self.result_tree = ttk.Treeview(self.root, columns=columns, show="headings",
                                        yscrollcommand=self.result_scrollbar.set, height=12, style='Flat.Treeview')
        for col, width in zip(columns, widths):
            self.result_tree.heading(col, text=col, anchor=tk.CENTER,
                                     command=lambda _col=col: self.sort_by_column(_col, False))
            self.result_tree.column(col, width=width, anchor=tk.W)

        # Grid setup for result treeview
        self.result_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.result_scrollbar.config(command=self.result_tree.yview)

        # Listbox to display external IPs with checkboxes (initially hidden)
        self.external_ip_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, bg="#F0F5FA", fg="#8599C8",
                                              relief=tk.FLAT)
        self.external_ip_listbox.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.external_ip_listbox.bind("<Shift-Button-1>", self.shift_select_ips)
        self.external_ip_listbox.grid_remove()  # Hide initially

        # Listbox to display program names (initially hidden)
        self.program_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, bg="#F0F5FA", fg="#8599C8", relief=tk.FLAT)
        self.program_listbox.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.program_listbox.bind("<ButtonRelease-1>", self.on_program_selected)
        self.program_listbox.grid_remove()  # Hide initially

        self.copy_bind()

        # Button to send external IPs (initially hidden and disabled)
        self.send_button = tk.Button(self.root, text="Send External IPs", command=self.send_external_ips,
                                     state=tk.DISABLED, bg="#3D3E3F", fg="white", relief=tk.FLAT, height=2)
        self.send_button.grid(row=4, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)
        self.send_button.grid_remove()  # Hide initially

        # Checkbox and Label for agreement
        agreement_text = "I agree to send the selected external IPs to third-party APIs to retrieve ISP, country of origin, and abuse reputation."
        self.agreement_var = tk.IntVar()
        self.agreement_check = tk.Checkbutton(self.root, text=agreement_text, variable=self.agreement_var,
                                              onvalue=1, offvalue=0, command=self.toggle_send_button,
                                              bg="#D9E3F1", fg="#8599C8", selectcolor="#D9E3F1",
                                              activebackground="#D9E3F1", activeforeground="#7878BE",
                                              font=("Segoe UI", 10))
        self.agreement_check.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        self.agreement_check.grid_remove()

        # Configure tags for LAN and WAN coloring
        self.result_tree.tag_configure("LAN", foreground="#23A7BC")
        self.result_tree.tag_configure("WAN", foreground="#7D54D5")

        # Button to open Settings window
        self.settings_button = tk.Button(self.root, text="Settings", command=self.open_settings_window,
                                         bg="#FFA500", fg="white", relief=tk.FLAT)
        self.settings_button.grid(row=5, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configure grid weights for layout responsiveness
        self.root.grid_rowconfigure(1, weight=1)  # Result Treeview row
        self.root.grid_rowconfigure(2, weight=1)  # Result Treeview row
        self.root.grid_columnconfigure(0, weight=1)  # Left column
        self.root.grid_columnconfigure(1, weight=1)  # Right column

        # Set root background color
        self.root.configure(bg="#D9E3F1")

    def open_settings_window(self):
        settings_window = SettingsWindow(self.root)

    def copy_bind(self):
        # Bind right-click event to show context menu
        self.result_tree.bind("<Button-3>", self.show_context_menu)

        # Context menu for copying
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selected_rows)

        # Bind right-click event to show context menu for external_ip_listbox
        self.external_ip_listbox.bind("<Button-3>", self.show_external_ips_context_menu)

        # Context menu for external_ip_listbox
        self.external_ips_context_menu = tk.Menu(self.root, tearoff=0)
        self.external_ips_context_menu.add_command(label="Copy", command=self.copy_external_ips)

        # Bind right-click event to show context menu for program_listbox
        self.program_listbox.bind("<Button-3>", self.show_program_names_context_menu)

        # Context menu for program_listbox
        self.program_names_context_menu = tk.Menu(self.root, tearoff=0)
        self.program_names_context_menu.add_command(label="Copy", command=self.copy_program_names)

    def show_context_menu(self, event):
        # Select the item under the mouse pointer if not already selected
        item = self.result_tree.identify_row(event.y)
        if item:
            # Check if the item is already selected, if not, select it
            if item not in self.result_tree.selection():
                self.result_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_selected_rows(self):
        selected_items = self.result_tree.selection()
        if selected_items:
            values_to_copy = []

            # Prepare data to be copied to clipboard
            for item in selected_items:
                values = self.result_tree.item(item, "values")
                if values:
                    values_str = "\t".join(map(str, values))  # Adjust as per your requirement
                    values_to_copy.append(values_str)

            # Join all lines with newline characters
            copy_text = "\n".join(values_to_copy)

            # Clear the clipboard contents and append the new content
            self.root.clipboard_clear()
            self.root.clipboard_append(copy_text)

    def show_external_ips_context_menu(self, event):
        # Select the item under the mouse pointer if not already selected
        index = self.external_ip_listbox.nearest(event.y)
        self.external_ip_listbox.selection_set(index)  # Ensure the clicked item is selected

        # Post the context menu
        self.external_ips_context_menu.post(event.x_root, event.y_root)

    def show_program_names_context_menu(self, event):
        # Select the item under the mouse pointer if not already selected
        index = self.program_listbox.nearest(event.y)
        self.program_listbox.selection_clear(0, tk.END)
        self.program_listbox.selection_set(index)
        self.program_names_context_menu.post(event.x_root, event.y_root)

    def copy_external_ips(self):
        selected_indices = self.external_ip_listbox.curselection()
        if selected_indices:
            selected_items = [self.external_ip_listbox.get(index) for index in selected_indices]
            copy_text = "\n".join(selected_items)

            self.root.clipboard_clear()
            self.root.clipboard_append(copy_text)

    def copy_program_names(self):
        selected_index = self.program_listbox.curselection()
        if selected_index:
            selected_item = self.program_listbox.get(selected_index)
            copy_text = selected_item

            self.root.clipboard_clear()
            self.root.clipboard_append(copy_text)

    def on_get_processes(self):
        self.connections = self.processor.fetch_netstat_data()

        if self.connections:
            self.external_ip_listbox.grid()
            self.send_button.grid()
            self.program_listbox.grid()
            self.agreement_check.grid()

            self.result_tree.delete(*self.result_tree.get_children())
            self.external_ip_listbox.delete(0, tk.END)
            self.program_listbox.delete(0, tk.END)
            self.program_ips_dict = dict()

            self.connections.sort(key=lambda x: (self.processor.is_private_ip(x[2]), x[5]))

            for conn in self.connections:
                protocol, local_addr, foreign_addr, state, pid, program_name = conn
                tag = "LAN" if self.processor.is_private_ip(foreign_addr) else "WAN"
                self.result_tree.insert("", "end",
                                        values=(protocol, local_addr, foreign_addr, state, pid, program_name),
                                        tags=(tag,))

                # Store program names and associated IPs
                if program_name not in self.program_ips_dict:
                    self.program_ips_dict[program_name] = []
                if foreign_addr != '*:*':
                    self.program_ips_dict[program_name].append(foreign_addr)

            # Filter programs to show only those with external IPs
            self.program_listbox.insert(tk.END, "All")
            for name, ips in self.program_ips_dict.items():
                if any(not self.processor.is_private_ip(ip) for ip in ips):
                    self.program_listbox.insert(tk.END, name)

            # Select "All" by default
            self.program_listbox.selection_set(0)

            # Update external IPs listbox based on selected program
            self.update_external_ips_listbox()

        else:
            messagebox.showerror("Error", "Failed to fetch processes.\n"
                                          "Please ensure that administrative privileges are enabled.")

    def sort_by_column(self, col, descending):
        # Function to sort columns in the treeview
        data = [(self.result_tree.set(child, col), child) for child in self.result_tree.get_children('')]
        if col in ("Local Address", "Foreign Address"):
            data.sort(key=lambda t: (':' in t, t[0]), reverse=descending)
        elif col in ("Abuse", "PID"):
            data.sort(key=lambda t: int(t[0]) if t[0].isdigit() else float('inf'), reverse=descending)
        else:
            data.sort(reverse=descending)

        for index, (val, child) in enumerate(data):
            self.result_tree.move(child, '', index)

        self.result_tree.heading(col, command=lambda: self.sort_by_column(col, not descending))

    def on_program_selected(self, event):
        # Function to handle program selection in program_listbox
        selected_program_index = self.program_listbox.curselection()
        if selected_program_index:
            selected_program_name = self.program_listbox.get(selected_program_index)
            if selected_program_name == "All":
                self.update_external_ips_listbox()
            else:
                self.update_external_ips_listbox(selected_program_name)

    def update_external_ips_listbox(self, program_name=None):
        # Function to update external_ip_listbox based on selected program
        self.external_ip_listbox.delete(0, tk.END)

        if program_name is None or program_name == "All":
            if "All" in self.program_ips_dict:
                ips = self.program_ips_dict["All"]
            else:
                ips = []
                for ips_list in self.program_ips_dict.values():
                    ips.extend(ips_list)
        else:
            ips = self.program_ips_dict.get(program_name, [])

        # Deduplicate and sort IPs
        unique_ips = list(set(ips))
        unique_ips.sort(key=lambda x: (':' in x, x))

        for ip in unique_ips:
            if not self.processor.is_private_ip(ip):
                self.external_ip_listbox.insert(tk.END, ip)

    def shift_select_ips(self, event):
        # Function to handle shift-select in external_ip_listbox
        index = self.external_ip_listbox.nearest(event.y)

        if not self.external_ip_listbox.curselection():
            self.external_ip_listbox.selection_set(index)
            return

        anchor = self.external_ip_listbox.index(tk.ACTIVE)

        self.external_ip_listbox.select_clear(0, tk.END)
        if index > anchor:
            self.external_ip_listbox.selection_set(anchor, index)
        else:
            self.external_ip_listbox.selection_set(index, anchor)

    def toggle_send_button(self):
        # Function to toggle the state of send_button based on agreement checkbox
        if self.agreement_var.get() == 1:
            self.send_button.config(state=tk.NORMAL)
        else:
            self.send_button.config(state=tk.DISABLED)

    def send_external_ips(self):
        # Function to handle "Send External IPs" button click
        selected_indices = self.external_ip_listbox.curselection()
        if selected_indices:
            selected_ips = [self.external_ip_listbox.get(i) for i in selected_indices]
            self.processor.send_external_ips(selected_ips, self.result_tree)
        else:
            messagebox.showwarning("Warning", "No external IPs selected.")

    def main(self):
        # Main function to start the GUI main loop
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = NetstatGUI(root)
    app.main()

