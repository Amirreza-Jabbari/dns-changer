import tkinter as tk
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk
import webbrowser

class DNSChanger:
    def __init__(self, root):
        self.root = root
        self.root.title("DNS Changer")
        self.root.geometry("300x300")
        self.dns_list = {
            "DNS 1": ["178.22.122.100", "185.51.200.2"],
            "DNS 2": ["10.202.10.202", "10.202.10.102"],
            "DNS 3": ["185.55.226.26", "185.55.225.25"],
            "DNS 4": ["172.29.0.100", "172.29.2.100"],
            "DNS 5": ["91.92.251.221", "91.92.251.222"]
        }
        self.selected_dns = tk.StringVar()
        self.selected_dns.set("DNS 1")
        self.is_connected = False

        self.create_widgets()

    def create_widgets(self):
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.on_button = tk.Button(self.button_frame, text="ON", command=self.connect_dns, width=10, height=5)
        self.on_button.pack(side=tk.LEFT, padx=10)

        self.off_button = tk.Button(self.button_frame, text="OFF", command=self.disconnect_dns, width=10, height=5, state=tk.DISABLED)
        self.off_button.pack(side=tk.LEFT, padx=10)

        self.dns_frame = tk.Frame(self.root)
        self.dns_frame.pack(pady=10)

        self.dns_label = tk.Label(self.dns_frame, text="Select DNS:")
        self.dns_label.pack(side=tk.LEFT)

        self.dns_option = ttk.OptionMenu(self.dns_frame, self.selected_dns, *self.dns_list.keys())
        self.dns_option.pack(side=tk.LEFT)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

        self.github_button_frame = tk.Frame(self.root)
        self.github_button_frame.pack(pady=10)

        self.github_image = ImageTk.PhotoImage(Image.open("github.png"))
        self.github_button = tk.Button(self.github_button_frame, image=self.github_image, command=self.open_github)
        self.github_button.pack(side=tk.LEFT, padx=10)

        self.github_label = tk.Label(self.github_button_frame, text="GitHub")
        self.github_label.pack(side=tk.LEFT, padx=10)

        self.coded_by_label = tk.Label(self.root, text="Coded by Amirreza Jabbari")
        self.coded_by_label.pack(side=tk.BOTTOM)

    def connect_dns(self):
        dns = self.dns_list[self.selected_dns.get()]
        self.change_dns(dns)
        self.on_button.config(state=tk.DISABLED)
        self.off_button.config(state=tk.NORMAL)
        self.on_button.config(bg="green")
        self.status_label.config(text="Connected to " + self.selected_dns.get())

    def disconnect_dns(self):
        self.change_dns(["8.8.8.8", "8.8.4.4"])  # default dns
        self.on_button.config(state=tk.NORMAL)
        self.off_button.config(state=tk.DISABLED)
        self.on_button.config(bg="SystemButtonFace")
        self.status_label.config(text="Disconnected")

    def change_dns(self, dns):
        # Get all network connections
        connections = subprocess.check_output(["netsh", "interface", "ip", "show", "config"]).decode("utf-8").splitlines()

        # Get the names of all network connections
        connection_names = []
        for connection in connections:
            if "Ethernet" in connection or "Wi-Fi" in connection:
                connection_name = connection.split(":")[0].strip()
                if connection_name.startswith("Ethernet") or connection_name.startswith("Wi-Fi"):
                    connection_names.append(connection_name)

        # Change DNS for each connection
        for connection_name in connection_names:
            subprocess.run(["netsh", "interface", "ip", "set", "dns", "name=\"" + connection_name + "\"", "static", dns[0], "primary"])
            subprocess.run(["netsh", "interface", "ip", "add", "dns", "name=\"" + connection_name + "\"", "addr=" + dns[1] + " index=2"])

    def open_github(self):
        webbrowser.open("https://github.com/Amirreza-Jabbari")

if __name__ == "__main__":
    root = tk.Tk()
    app = DNSChanger(root)
    root.mainloop()