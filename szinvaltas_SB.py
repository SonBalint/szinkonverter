import tkinter as tk
from tkinter import colorchooser


class SzinKezelo_SB:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

    def rgb_to_hex_konverter_SB(self, r, g, b):
        try:
            r = int(r)
            g = int(g)
            b = int(b)
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                hex_kod = f'#{r:02x}{g:02x}{b:02x}'
                self.r, self.g, self.b = r, g, b
                return hex_kod.upper()
            else:
                return "ÉRVÉNYTELEN"
        except ValueError:
            return "ÉRVÉNYTELEN"

    def hex_to_rgb_konverter(self, hex_kod):
        hex_kod = hex_kod.lstrip('#')
        if len(hex_kod) == 6:
            try:
                r = int(hex_kod[0:2], 16)
                g = int(hex_kod[2:4], 16)
                b = int(hex_kod[4:6], 16)
                self.r, self.g, self.b = r, g, b
                return r, g, b
            except ValueError:
                return None
        return None


class Ablak(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Színkód Konverter ZXS6MW")
        self.szin_kezelo = SzinKezelo_SB()
        self.geometry("500x350")

        self.setup_ui()

    def setup_ui(self):
        self.rgb_entry = {}
        szin_nevek = ["R", "G", "B"]

        for i, nev in enumerate(szin_nevek):
            tk.Label(self, text=f"{nev}:").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entry.insert(0, "0")
            entry.bind("<KeyRelease>", self.frissites_esemeny)
            self.rgb_entry[nev] = entry

        tk.Label(self, text="HEX:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.hex_entry = tk.Entry(self)
        self.hex_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.hex_entry.insert(0, "#000000")
        self.hex_entry.bind("<KeyRelease>", self.hex_frissites_esemeny)

        self.szin_panel = tk.Label(self, bg="#000000", width=15, height=5, relief="groove")
        self.szin_panel.grid(row=0, column=2, rowspan=4, padx=10, pady=10)

        tk.Button(self, text="Színválasztó", command=self.szinvalaszto_esemeny).grid(row=4, column=0, columnspan=2,
                                                                                     pady=10)

        self.grid_columnconfigure(1, weight=1)

    def frissites_esemeny(self, event):
        r_val = self.rgb_entry["R"].get()
        g_val = self.rgb_entry["G"].get()
        b_val = self.rgb_entry["B"].get()

        hex_kod = self.szin_kezelo.rgb_to_hex_konverter_SB(r_val, g_val, b_val)

        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(0, hex_kod)

        if hex_kod != "ÉRVÉNYTELEN":
            self.szin_panel.config(bg=hex_kod)
        else:
            self.szin_panel.config(bg="gray")

    def hex_frissites_esemeny(self, event):
        hex_val = self.hex_entry.get()
        rgb_tuple = self.szin_kezelo.hex_to_rgb_konverter(hex_val)

        if rgb_tuple:
            r, g, b = rgb_tuple

            for nev, val in zip(["R", "G", "B"], [r, g, b]):
                self.rgb_entry[nev].delete(0, tk.END)
                self.rgb_entry[nev].insert(0, str(val))

            self.szin_panel.config(bg=hex_val)
        else:
            self.szin_panel.config(bg="gray")

    def szinvalaszto_esemeny(self):
        szin_kod = colorchooser.askcolor(title="Szín kiválasztása")
        if szin_kod:
            rgb_tuple = szin_kod[0]
            hex_val = szin_kod[1]

            if rgb_tuple:
                r, g, b = [int(x) for x in rgb_tuple]

                for nev, val in zip(["R", "G", "B"], [r, g, b]):
                    self.rgb_entry[nev].delete(0, tk.END)
                    self.rgb_entry[nev].insert(0, str(val))

            self.hex_entry.delete(0, tk.END)
            self.hex_entry.insert(0, hex_val.upper())

            self.szin_panel.config(bg=hex_val)