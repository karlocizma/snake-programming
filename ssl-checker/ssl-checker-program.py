import ssl
import socket
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def ssl_pruefung(domain):
    try:
        # Verbindung zum Server auf Port 443 herstellen und SSL-Zertifikat abrufen
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        # Ablaufdatum und Aussteller extrahieren
        ablaufdatum_str = cert['notAfter']
        aussteller = cert['issuer']
        ablaufdatum = datetime.strptime(ablaufdatum_str, '%b %d %H:%M:%S %Y %Z')
        
        # SSL-Zertifikat-Informationen zusammensetzen
        zertifikat_info = f"SSL-Zertifikat für {domain}\n"
        zertifikat_info += f"Ablaufdatum: {ablaufdatum.strftime('%d.%m.%Y')}\n"
        zertifikat_info += "Ausgestellt von:\n"
        for teil in aussteller:
            zertifikat_info += f"  - {teil[0][0]}: {teil[0][1]}\n"
        
        # Kostenlos oder kostenpflichtig prüfen
        kostenlose_anbieter = ["Let's Encrypt", "ZeroSSL"]
        kostenlos = any(any(ka in teil[0][1] for ka in kostenlose_anbieter) for teil in aussteller)
        if kostenlos:
            zertifikat_info += "\nDieses SSL-Zertifikat ist kostenlos (ausgestellt von einem kostenlosen Anbieter)."
        else:
            zertifikat_info += "\nDieses SSL-Zertifikat ist kostenpflichtig (ausgestellt von einem kommerziellen Anbieter)."
        
        # Ergebnis anzeigen
        messagebox.showinfo("Zertifikat-Informationen", zertifikat_info)

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Abrufen des Zertifikats: {e}")

# GUI-Funktion
def start_gui():
    # Hauptfenster
    root = tk.Tk()
    root.title("SSL-Zertifikatsprüfung")

    # Eingabefeld und Label
    label = tk.Label(root, text="Bitte geben Sie eine Domain ein (ohne https://):")
    label.pack(pady=10)

    domain_entry = tk.Entry(root, width=40)
    domain_entry.pack(pady=5)

    # Funktion zum Aufrufen der Zertifikatsprüfung
    def on_check():
        domain = domain_entry.get().strip()
        if domain:
            ssl_pruefung(domain)
        else:
            messagebox.showwarning("Eingabefehler", "Bitte eine gültige Domain eingeben.")

    # Prüfen-Button
    check_button = tk.Button(root, text="Zertifikat prüfen", command=on_check)
    check_button.pack(pady=20)

    # GUI starten
    root.mainloop()

# GUI aufrufen
start_gui()
