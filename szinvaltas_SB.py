import tkinter as tk
from tkinter import colorchooser
import colorsys


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
                return hex_kod.upper()
            else:
                return "ÉRVÉNYTELEN"
        except ValueError:
            return "ÉRVÉNYTELEN"

    def rgb_to_cmyk(self, r, g, b):
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        k = 1 - max(r_norm, g_norm, b_norm)

        if k == 1:
            return 0, 0, 0, 100

        c = (1 - r_norm - k) / (1 - k) * 100
        m = (1 - g_norm - k) / (1 - k) * 100
        y = (1 - b_norm - k) / (1 - k) * 100
        k_perc = k * 100

        return round(c), round(m), round(y), round(k_perc)

    def cmyk_to_rgb(self, c, m, y, k):
        c_norm, m_norm, y_norm, k_norm = c / 100.0, m / 100.0, y / 100.0, k / 100.0
        r = 255 * (1 - c_norm) * (1 - k_norm)
        g = 255 * (1 - m_norm) * (1 - k_norm)
        b = 255 * (1 - y_norm) * (1 - k_norm)
        return round(r), round(g), round(b)

    def rgb_to_hsl(self, r, g, b):
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)
        return round(h * 360), round(s * 100), round(l * 100)

    def hsl_to_rgb(self, h, s, l):
        h_norm, s_norm, l_norm = h / 360.0, s / 100.0, l / 100.0
        r, g, b = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)
        return round(r * 255), round(g * 255), round(b * 255)

    def rgb_to_hsv(self, r, g, b):
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
        return round(h * 360), round(s * 100), round(v * 100)

    def hsv_to_rgb(self, h, s, v):
        h_norm, s_norm, v_norm = h / 360.0, s / 100.0, v / 100.0
        r, g, b = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)
        return round(r * 255), round(g * 255), round(b * 255)

    def update_rgb_from_source(self, source_type, values):
        r, g, b = 0, 0, 0
        valid = True

        try:
            val_f = []
            if source_type != "HEX":
                val_f = [float(v) for v in values]

            if source_type == "RGB":
                r, g, b = [round(v) for v in val_f]
            elif source_type == "HEX":
                hex_str = values[0].lstrip('#')
                if len(hex_str) == 6:
                    r = int(hex_str[0:2], 16)
                    g = int(hex_str[2:4], 16)
                    b = int(hex_str[4:6], 16)
                else:
                    valid = False
            elif source_type == "CMYK":
                r, g, b = self.cmyk_to_rgb(*val_f)
            elif source_type == "HSL":
                r, g, b = self.hsl_to_rgb(*val_f)
            elif source_type == "HSV":
                r, g, b = self.hsv_to_rgb(*val_f)

            if valid and 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                self.r, self.g, self.b = r, g, b
                return True
            else:
                raise ValueError
        except (ValueError, IndexError):
            return False


class Ablak(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Színkód Konverter ZXS6MW v1.4")
        self.szin_kezelo = SzinKezelo_SB()
        self.geometry("850x450")

        self.input_widgets = {}

        self.konv_forrasok = ["RGB", "HEX", "CMYK", "HSL", "HSV"]
        self.valasztott_forras = tk.StringVar(self)
        self.valasztott_forras.set(self.konv_forrasok[0])
        self.valasztott_forras.trace_add("write", self.reset_ui_fields_esemeny)

        self.setup_ui()
        self.update_ui_from_rgb()

    def setup_ui(self):
        for i in range(1, 5):
            tk.Grid.columnconfigure(self, i, weight=1)
        tk.Grid.columnconfigure(self, 5, weight=0)
        tk.Grid.columnconfigure(self, 6, weight=1)

        row_idx = 0

        tk.Label(self, text="RGB (0-255):").grid(row=row_idx, column=0, padx=5, pady=5, sticky="w")
        rgb_nevek = ["R", "G", "B"]
        self.rgb_entries = {}
        rgb_string_list = []
        for col, nev in enumerate(rgb_nevek):
            entry = tk.Entry(self, width=5)
            entry.grid(row=row_idx, column=col + 1, padx=5, pady=5, sticky="ew")
            self.rgb_entries[nev] = entry
            self.input_widgets[nev] = entry
            rgb_string_list.append(entry)

        tk.Button(self, text="📋", command=lambda: self.copy_rgb_to_clipboard(rgb_string_list)).grid(row=row_idx,
                                                                                                    column=5, padx=5,
                                                                                                    pady=5)
        row_idx += 1

        tk.Label(self, text="HEX:").grid(row=row_idx, column=0, padx=5, pady=5, sticky="w")
        self.hex_entry = tk.Entry(self, width=10)
        self.hex_entry.grid(row=row_idx, column=1, columnspan=4, padx=5, pady=5, sticky="ew")
        self.input_widgets["HEX"] = self.hex_entry
        tk.Button(self, text="📋", command=lambda: self.copy_to_clipboard_esemeny(self.hex_entry)).grid(row=row_idx,
                                                                                                       column=5, padx=5,
                                                                                                       pady=5)
        row_idx += 1

        tk.Label(self, text="CMYK (0-100%):").grid(row=row_idx, column=0, padx=5, pady=5, sticky="w")
        cmyk_nevek = ["C", "M", "Y", "K"]
        self.cmyk_entries = {}
        cmyk_string_list = []
        for col, nev in enumerate(cmyk_nevek):
            entry = tk.Entry(self, width=5)
            entry.grid(row=row_idx, column=col + 1, padx=5, pady=5, sticky="ew")
            self.cmyk_entries[nev] = entry
            self.input_widgets[nev] = entry
            cmyk_string_list.append(entry)
        tk.Button(self, text="📋", command=lambda: self.copy_multi_to_clipboard(cmyk_string_list, separator=", ")).grid(
            row=row_idx, column=5, padx=5, pady=5)
        row_idx += 1

        tk.Label(self, text="HSL (H/S/L):").grid(row=row_idx, column=0, padx=5, pady=5, sticky="w")
        hsl_nevek = ["H", "S", "L"]
        self.hsl_entries = {}
        hsl_string_list = []
        for col, nev in enumerate(hsl_nevek):
            entry = tk.Entry(self, width=5)
            entry.grid(row=row_idx, column=col + 1, padx=5, pady=5, sticky="ew")
            self.hsl_entries[nev] = entry
            self.input_widgets[f"HSL_{nev}"] = entry
            hsl_string_list.append(entry)
        tk.Button(self, text="📋", command=lambda: self.copy_hsl_hsv_to_clipboard(hsl_string_list, "HSL")).grid(
            row=row_idx, column=5, padx=5, pady=5)
        row_idx += 1

        tk.Label(self, text="HSV (H/S/V):").grid(row=row_idx, column=0, padx=5, pady=5, sticky="w")
        hsv_nevek = ["H", "S", "V"]
        self.hsv_entries = {}
        hsv_string_list = []
        for col, nev in enumerate(hsv_nevek):
            entry = tk.Entry(self, width=5)
            entry.grid(row=row_idx, column=col + 1, padx=5, pady=5, sticky="ew")
            self.hsv_entries[nev] = entry
            self.input_widgets[f"HSV_{nev}"] = entry
            hsv_string_list.append(entry)
        tk.Button(self, text="📋", command=lambda: self.copy_hsl_hsv_to_clipboard(hsv_string_list, "HSV")).grid(
            row=row_idx, column=5, padx=5, pady=5)
        row_idx += 1

        self.szin_panel = tk.Label(self, bg="#000000", width=15, height=5, relief="groove")
        self.szin_panel.grid(row=0, column=6, rowspan=6, padx=10, pady=10, sticky="nsew")

        tk.Label(self, text="Konvertálás forrása:").grid(row=row_idx, column=0, columnspan=2, pady=10, sticky="w")
        self.forras_menu = tk.OptionMenu(self, self.valasztott_forras, *self.konv_forrasok)
        self.forras_menu.grid(row=row_idx, column=2, columnspan=3, sticky="ew", padx=5)
        row_idx += 1

        tk.Button(self, text="Törlés", command=self.reset_ui_entry_fields).grid(row=row_idx, column=1, sticky="ew",
                                                                                padx=5, pady=5)

        tk.Button(self, text="Konvertálás", command=self.main_konvertalas_esemeny).grid(row=row_idx, column=2,
                                                                                        sticky="ew", padx=5, pady=5)

        tk.Button(self, text="Színválasztó", command=self.szinvalaszto_esemeny).grid(row=row_idx, column=3, sticky="ew",
                                                                                     padx=5, pady=5)

        row_idx += 1

    def copy_to_clipboard_esemeny(self, entry_widget):
        self.clipboard_clear()
        self.clipboard_append(entry_widget.get())

    def copy_multi_to_clipboard(self, entry_list, separator=", "):
        values = [entry.get() for entry in entry_list]
        formatted_string = separator.join(values)
        self.clipboard_clear()
        self.clipboard_append(formatted_string)

    def copy_rgb_to_clipboard(self, entry_list):
        values = [entry.get() for entry in entry_list]
        formatted_string = f"rgb({', '.join(values)})"
        self.clipboard_clear()
        self.clipboard_append(formatted_string)

    def copy_hsl_hsv_to_clipboard(self, entry_list, mode):
        values = [entry.get() for entry in entry_list]
        h, s, l_v = values[0], values[1], values[2]
        formatted_string = f"{mode.lower()}({h}deg, {s}%, {l_v}%)"
        self.clipboard_clear()
        self.clipboard_append(formatted_string)

    def reset_ui_entry_fields(self):
        self.szin_kezelo.r = 0
        self.szin_kezelo.g = 0
        self.szin_kezelo.b = 0

        for entry in self.rgb_entries.values():
            entry.delete(0, tk.END)
        self.hex_entry.delete(0, tk.END)
        for entry in self.cmyk_entries.values():
            entry.delete(0, tk.END)
        for entry in self.hsl_entries.values():
            entry.delete(0, tk.END)
        for entry in self.hsv_entries.values():
            entry.delete(0, tk.END)

        self.szin_panel.config(bg="#FFFFFF")

    def reset_ui_fields_esemeny(self, *args):
        self.reset_ui_entry_fields()

    def update_ui_from_rgb(self):
        r, g, b = self.szin_kezelo.r, self.szin_kezelo.g, self.szin_kezelo.b

        hex_kod = self.szin_kezelo.rgb_to_hex_konverter_SB(r, g, b)
        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(0, hex_kod)

        self.rgb_entries["R"].delete(0, tk.END)
        self.rgb_entries["G"].delete(0, tk.END)
        self.rgb_entries["B"].delete(0, tk.END)
        self.rgb_entries["R"].insert(0, str(r))
        self.rgb_entries["G"].insert(0, str(g))
        self.rgb_entries["B"].insert(0, str(b))

        c, m, y, k = self.szin_kezelo.rgb_to_cmyk(r, g, b)
        for nev, val in zip(["C", "M", "Y", "K"], [c, m, y, k]):
            self.cmyk_entries[nev].delete(0, tk.END)
            self.cmyk_entries[nev].insert(0, str(val))

        h_hsl, s_hsl, l_hsl = self.szin_kezelo.rgb_to_hsl(r, g, b)
        for nev, val in zip(["H", "S", "L"], [h_hsl, s_hsl, l_hsl]):
            self.hsl_entries[nev].delete(0, tk.END)
            self.hsl_entries[nev].insert(0, str(val))

        h_hsv, s_hsv, v_hsv = self.szin_kezelo.rgb_to_hsv(r, g, b)
        for nev, val in zip(["H", "S", "V"], [h_hsv, s_hsv, v_hsv]):
            self.hsv_entries[nev].delete(0, tk.END)
            self.hsv_entries[nev].insert(0, str(val))

        self.szin_panel.config(bg=hex_kod)

    def main_konvertalas_esemeny(self):
        source_type = self.valasztott_forras.get()
        values = []

        if source_type == "RGB":
            values = [self.rgb_entries["R"].get(), self.rgb_entries["G"].get(), self.rgb_entries["B"].get()]
        elif source_type == "HEX":
            values = [self.hex_entry.get()]
        elif source_type == "CMYK":
            values = [self.cmyk_entries["C"].get(), self.cmyk_entries["M"].get(), self.cmyk_entries["Y"].get(),
                      self.cmyk_entries["K"].get()]
        elif source_type == "HSL":
            values = [self.hsl_entries["H"].get(), self.hsl_entries["S"].get(), self.hsl_entries["L"].get()]
        elif source_type == "HSV":
            values = [self.hsv_entries["H"].get(), self.hsv_entries["S"].get(), self.hsv_entries["V"].get()]

        self.szin_kezelo.update_rgb_from_source(source_type, values)
        self.update_ui_from_rgb()

    def szinvalaszto_esemeny(self):
        szin_kod = colorchooser.askcolor(title="Szín kiválasztása")
        if szin_kod:
            r, g, b = [round(x) for x in szin_kod[0]]
            self.szin_kezelo.r, self.szin_kezelo.g, self.szin_kezelo.b = r, g, b
            self.update_ui_from_rgb()