import socket
import requests
import ssl
import tkinter as tk
from tkinter import ttk, scrolledtext

def get_ip_address(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def reverse_dns_lookup(ip):
    try:
        return socket.gethostbyaddr(ip)[0]  # Returns the hostname for the given IP address
    except socket.herror:
        return "No reverse DNS record found."

def get_server_info(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        headers = response.headers
        server = headers.get('Server', 'Unknown')
        date = headers.get('Date', 'Unknown')
        return {
            "status_code": response.status_code,
            "server": server,
            "date": date
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Error: {e}"}

def get_ssl_info(domain):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
    
    try:
        conn.connect((domain, 443))  # Connect to the HTTPS port
        cert = conn.getpeercert()
        ssl_info = {
            "issuer": dict(x[0] for x in cert['issuer']),
            "valid_from": cert['notBefore'],
            "valid_until": cert['notAfter'],
            "subject": dict(x[0] for x in cert['subject']),
        }
        return ssl_info
    except Exception as e:
        return {"error": f"SSL Error: {e}"}
    finally:
        conn.close()

def check_server(domain, option, output_box):
    output_box.delete(1.0, tk.END)  # Clear the output box
    
    if not domain:
        output_box.insert(tk.END, "Please enter a domain name.\n")
        return
    
    # Step 1: Get the IP address of the domain
    ip_address = get_ip_address(domain)
    if ip_address:
        output_box.insert(tk.END, f"IP Address: {ip_address}\n")
        
        # Step 2: Perform reverse DNS lookup on the IP address
        reverse_dns = reverse_dns_lookup(ip_address)
        output_box.insert(tk.END, f"Reverse DNS Lookup: {reverse_dns}\n")
    else:
        output_box.insert(tk.END, f"Failed to resolve IP for {domain}.\n")
        return
    
    # Step 3: Get the server info if option includes "Homepage Info"
    if option != "SSL Info":
        server_info = get_server_info(domain)
        if "error" in server_info:
            output_box.insert(tk.END, f"{server_info['error']}\n")
        else:
            output_box.insert(tk.END, f"HTTP Status Code: {server_info['status_code']}\n")
            output_box.insert(tk.END, f"Server: {server_info['server']}\n")
            output_box.insert(tk.END, f"Date: {server_info['date']}\n")
    
    # Step 4: Get SSL certificate information if option includes "SSL Info"
    if option != "Homepage Info":
        ssl_info = get_ssl_info(domain)
        if "error" in ssl_info:
            output_box.insert(tk.END, f"{ssl_info['error']}\n")
        else:
            output_box.insert(tk.END, "SSL Certificate Info:\n")
            output_box.insert(tk.END, f" - Issuer: {ssl_info['issuer']}\n")
            output_box.insert(tk.END, f" - Valid From: {ssl_info['valid_from']}\n")
            output_box.insert(tk.END, f" - Valid Until: {ssl_info['valid_until']}\n")
            output_box.insert(tk.END, f" - Subject: {ssl_info['subject']}\n")

def create_gui():
    # Create the main window
    window = tk.Tk()
    window.title("Domain Server & SSL Info with Reverse Lookup")
    window.geometry("700x450")
    
    # Create input label and entry field
    label = ttk.Label(window, text="Enter Domain (without http/https):", font=("Arial", 12))
    label.pack(pady=10)
    
    domain_entry = ttk.Entry(window, width=50, font=("Arial", 12))
    domain_entry.pack(pady=5)
    
    # Create a dropdown to select Homepage or SSL Info
    option_var = tk.StringVar(value="Both")
    options = ["Both", "Homepage Info", "SSL Info"]
    
    option_menu = ttk.Combobox(window, textvariable=option_var, values=options, state="readonly", width=20)
    option_menu.pack(pady=10)
    
    # Create an output box to display results
    output_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=15, font=("Arial", 10))
    output_box.pack(pady=10)
    
    # Create a button to trigger the check
    check_button = ttk.Button(window, text="Check Server Info", command=lambda: check_server(domain_entry.get(), option_var.get(), output_box))
    check_button.pack(pady=10)
    
    # Apply a modern style
    style = ttk.Style(window)
    style.theme_use('clam')  # Use 'clam' or 'alt' for a modern look
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TEntry", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12), padding=5)
    
    # Run the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    create_gui()
