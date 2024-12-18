#SPF and DMARC configurator

import tkinter as tk
from tkinter import messagebox

def show_spf_help():
    help_text = (
        "SPF Record Help:\n\n"
        "1. Domain: Enter your domain name (e.g., example.com).\n"
        "2. IP Addresses: List IP addresses (comma-separated) from which your mail server sends emails.\n"
        "3. Include Domains: List domains (comma-separated) whose SPF records you want to include.\n"
        "4. A record: If your domain has an A record, check this box.\n"
        "5. MX record: If your domain has MX records, check this box.\n"
        "6. All Policy:\n"
        "   - -all: Fail all emails that don't match (strict).\n"
        "   - ~all: Soft fail for emails that don't match (recommended).\n"
        "   - ?all: Neutral, no policy.\n"
        "   - +all: Pass all emails (not recommended)."
    )
    messagebox.showinfo("SPF Record Help", help_text)

def show_dmarc_help():
    help_text = (
        "DMARC Record Help:\n\n"
        "1. Domain: Enter your domain name (e.g., example.com).\n"
        "2. Policy:\n"
        "   - none: No action is taken (monitoring only).\n"
        "   - quarantine: Emails that fail DMARC are marked as spam or sent to the junk folder.\n"
        "   - reject: Emails that fail DMARC are rejected.\n"
        "3. RUA Email: Email address(es) to receive aggregate reports.\n"
        "4. RUF Email: Email address(es) to receive forensic reports.\n"
        "5. Percentage: The percentage of messages to which the DMARC policy is applied (0-100)."
    )
    messagebox.showinfo("DMARC Record Help", help_text)

def generate_spf():
    domain = spf_domain_entry.get()
    ip_addresses = spf_ip_entry.get()
    include_domains = spf_include_entry.get()
    a_record = spf_a_var.get()
    mx_record = spf_mx_var.get()
    all_record = spf_all_var.get()

    spf_record = f"v=spf1"
    
    if ip_addresses:
        for ip in ip_addresses.split(','):
            spf_record += f" ip4:{ip.strip()}"
    
    if include_domains:
        for domain in include_domains.split(','):
            spf_record += f" include:{domain.strip()}"
    
    if a_record:
        spf_record += " a"
    
    if mx_record:
        spf_record += " mx"
    
    spf_record += f" {all_record}"

    spf_result.set(spf_record)
    messagebox.showinfo("SPF Record Generated", f"Your SPF record is:\n{spf_record}")

def generate_dmarc():
    domain = dmarc_domain_entry.get()
    policy = dmarc_policy_var.get()
    rua = dmarc_rua_entry.get()
    ruf = dmarc_ruf_entry.get()
    pct = dmarc_pct_entry.get()

    dmarc_record = f"v=DMARC1; p={policy}"
    
    if rua:
        dmarc_record += f"; rua=mailto:{rua}"
    
    if ruf:
        dmarc_record += f"; ruf=mailto:{ruf}"
    
    if pct:
        dmarc_record += f"; pct={pct}"

    dmarc_result.set(dmarc_record)
    messagebox.showinfo("DMARC Record Generated", f"Your DMARC record is:\n{dmarc_record}")

# Create the main window
root = tk.Tk()
root.title("SPF and DMARC Record Generator")

# SPF Section
spf_frame = tk.LabelFrame(root, text="Generate SPF Record", padx=10, pady=10)
spf_frame.pack(padx=10, pady=5, fill="both", expand="yes")

tk.Label(spf_frame, text="Your Domain (e.g., example.com):").grid(row=0, column=0, sticky='e')
spf_domain_entry = tk.Entry(spf_frame, width=50)
spf_domain_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(spf_frame, text="IP Addresses (comma separated, e.g., 192.168.0.1, 10.0.0.1):").grid(row=1, column=0, sticky='e')
spf_ip_entry = tk.Entry(spf_frame, width=50)
spf_ip_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(spf_frame, text="Include Domains (comma separated, e.g., include:_spf.google.com):").grid(row=2, column=0, sticky='e')
spf_include_entry = tk.Entry(spf_frame, width=50)
spf_include_entry.grid(row=2, column=1, padx=5, pady=5)

spf_a_var = tk.BooleanVar()
tk.Checkbutton(spf_frame, text="Include A record (check if your domain has an A record)", variable=spf_a_var).grid(row=3, columnspan=2)

spf_mx_var = tk.BooleanVar()
tk.Checkbutton(spf_frame, text="Include MX record (check if your domain has MX records)", variable=spf_mx_var).grid(row=4, columnspan=2)

spf_all_var = tk.StringVar(value="~all")
tk.Label(spf_frame, text="All Policy (Choose one):").grid(row=5, column=0, sticky='e')
tk.OptionMenu(spf_frame, spf_all_var, "-all", "~all", "?all").grid(row=5, column=1, sticky='w', padx=5, pady=5)

tk.Button(spf_frame, text="Generate SPF Record", command=generate_spf).grid(row=6, columnspan=2, pady=10)
spf_result = tk.StringVar()
tk.Entry(spf_frame, textvariable=spf_result, width=80, state='readonly').grid(row=7, columnspan=2, padx=5, pady=5)

tk.Button(spf_frame, text="SPF Help", command=show_spf_help).grid(row=8, columnspan=2, pady=10)

# DMARC Section
dmarc_frame = tk.LabelFrame(root, text="Generate DMARC Record", padx=10, pady=10)
dmarc_frame.pack(padx=10, pady=5, fill="both", expand="yes")

tk.Label(dmarc_frame, text="Your Domain (e.g., example.com):").grid(row=0, column=0, sticky='e')
dmarc_domain_entry = tk.Entry(dmarc_frame, width=50)
dmarc_domain_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(dmarc_frame, text="Policy (Choose one):").grid(row=1, column=0, sticky='e')
dmarc_policy_var = tk.StringVar(value="none")
tk.OptionMenu(dmarc_frame, dmarc_policy_var, "none", "quarantine", "reject").grid(row=1, column=1, sticky='w', padx=5, pady=5)

tk.Label(dmarc_frame, text="RUA Email (e.g., rua@example.com):").grid(row=2, column=0, sticky='e')
dmarc_rua_entry = tk.Entry(dmarc_frame, width=50)
dmarc_rua_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(dmarc_frame, text="RUF Email (e.g., ruf@example.com):").grid(row=3, column=0, sticky='e')
dmarc_ruf_entry = tk.Entry(dmarc_frame, width=50)
dmarc_ruf_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(dmarc_frame, text="Percentage (0-100, e.g., 100):").grid(row=4, column=0, sticky='e')
dmarc_pct_entry = tk.Entry(dmarc_frame, width=50)
dmarc_pct_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Button(dmarc_frame, text="Generate DMARC Record", command=generate_dmarc).grid(row=5, columnspan=2, pady=10)
dmarc_result = tk.StringVar()
tk.Entry(dmarc_frame, textvariable=dmarc_result, width=80, state='readonly').grid(row=6, columnspan=2, padx=5, pady=5)

tk.Button(dmarc_frame, text="DMARC Help", command=show_dmarc_help).grid(row=7, columnspan=2, pady=10)

# Run the application
root.mainloop()
