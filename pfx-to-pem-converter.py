import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12

def convert_pfx_to_pem(pfx_path, password):
    try:
        with open(pfx_path, 'rb') as pfx_file:
            pfx_data = pfx_file.read()
        
        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(pfx_data, password.encode())

        pem_cert = certificate.public_bytes(serialization.Encoding.PEM)
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        pem_path = pfx_path.replace('.pfx', '.pem')
        with open(pem_path, 'wb') as pem_file:
            pem_file.write(pem_cert)
            pem_file.write(pem_key)

            if additional_certificates:
                for cert in additional_certificates:
                    pem_file.write(cert.public_bytes(serialization.Encoding.PEM))
        
        messagebox.showinfo("Success", f"Converted to {pem_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_pfx_file():
    pfx_path = filedialog.askopenfilename(filetypes=[("PFX files", "*.pfx")])
    if pfx_path:
        password = password_entry.get()
        convert_pfx_to_pem(pfx_path, password)

# Set up the main window
root = tk.Tk()
root.title("PFX to PEM Converter")

# Create the GUI components
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

pfx_label = tk.Label(frame, text="Select PFX file:")
pfx_label.grid(row=0, column=0, sticky="w")

browse_button = tk.Button(frame, text="Browse", command=browse_pfx_file)
browse_button.grid(row=0, column=1)

password_label = tk.Label(frame, text="Password:")
password_label.grid(row=1, column=0, sticky="w")

password_entry = tk.Entry(frame, show="*")
password_entry.grid(row=1, column=1)

convert_button = tk.Button(frame, text="Convert", command=browse_pfx_file)
convert_button.grid(row=2, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()