# Színkód Konverter (Python Projektfeladat) - v1.3.1

## Hallgató
Sonkoly Bálint
ZXS6MW

## Feladat leírása
A program egy grafikus felhasználói felülettel rendelkező színkód konverter, amely képes átváltani az öt leggyakrabban használt színkódolási rendszer között: **RGB, HEX, CMYK, HSL, és HSV**. A konverzió alapja a lenyíló listán kiválasztott forrás (pl. RGB) mezőjében megadott érték. A frissítés és az átváltás a dedikált "Konvertálás" gomb megnyomására történik meg. Az 1.9-es verzió tartalmazza az összes beviteli mező törlésére szolgáló gombot, és másolás funkciót (vágólapra) minden színkód sor végén.

## Modulok és a felhasznált függvények/osztályok

A projekt két fő fájlból áll: `main.py` (indító) és `szinvaltas_SB.py` (logika és GUI).

### 1. Tanult Modulok
| Modul | Fő felhasználás |
| :--- | :--- |
| **tkinter** | Grafikus felhasználói felület (GUI) elemek (Tk, Label, Entry, Button, OptionMenu) és eseménykezelés (`.grid()`, `.bind()`, `.mainloop()`). |
| **tkinter.colorchooser** | A rendszer natív színválasztó ablakának megnyitása (`askcolor`). |
| **colorsys** | Szabványos Python könyvtár a HSL és HSV konverziókhoz (a float alapú számításokhoz). |

### 2. Saját Modulok és Osztályok

| Típus | Név | Leírás |
| :--- | :--- | :--- |
| **Saját Modul** | `szinvaltas_SB.py` | A program teljes logikáját tartalmazza. |
| **Saját Osztály** | `SzinKezelo_SB` | A belső RGB állapotot tárolja, és tartalmazza az összes matematikai konverziós logikát. |
| **GUI Osztály** | `Ablak` (tk.Tk) | Létrehozza a felhasználói felületet, és kezeli a gombokra/eseményekre adott válaszokat. |

### 3. Saját Függvények (metódusok)
* **`rgb_to_hex_konverter_SB(r, g, b)`:** Elvégzi a kötelező RGB-HEX átváltást.
* **`update_rgb_from_source(source_type, values)`:** Központi metódus, amely a kiválasztott forrásból (pl. CMYK) átalakítja az értéket a belső RGB állapotba.
* **`rgb_to_cmyk(r, g, b)`:** Képlet alapú RGB-CMYK konverzió.
* **`cmyk_to_rgb(c, m, y, k)`:** Képlet alapú CMYK-RGB konverzió.
* **`update_ui_from_rgb()`:** A belső RGB állapot alapján frissíti a GUI összes beviteli mezőjét és a színpanelt.

## 🚀 Futtatás
A program elindításához győződjön meg róla, hogy a **`main.py`** és a **`szinvaltas_SB.py`** egy mappában található. A futtatás a **`main.py`** fájl elindításával történik.

### GitHub elérés
https://github.com/SonBalint/szinkonverter