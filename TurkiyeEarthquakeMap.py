# -*- coding: utf-8 -*-
# ============================================================
# Project: KOERI Turkiye Earthquake Map (Tkinter + Folium)
# Developer: ModestusSpider
# Date: 2025-10-21
# Version: 1.0.0
# Description:
#   A lightweight desktop app (Tkinter) that fetches recent
#   earthquake data from KOERI and displays it on an
#   interactive Folium map with magnitude-based colors.
# ============================================================

import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from datetime import datetime, timedelta
from io import StringIO
import webbrowser
import os
import tkinter as tk
from tkinter import messagebox
from branca.element import Template, MacroElement

# -----------------------------
# Function: generate earthquake map
def generate_map(days, min_mw):
    try:
        # Fetch data
        URL = "http://www.koeri.boun.edu.tr/scripts/lst9.asp"
        resp = requests.get(URL, timeout=20)
        resp.raise_for_status()
        lines = resp.text.splitlines()

        # Find header line
        header_idx = None
        for i, line in enumerate(lines):
            if line.strip().startswith("Tarih"):
                header_idx = i
                break
        if header_idx is None:
            messagebox.showerror("Error", "Header line not found")
            return

        # Extract data lines
        data_lines = lines[header_idx + 1:]
        data_str = "\n".join(data_lines)
        colspecs = [
            (0, 10),     # Date
            (11, 19),    # Time
            (20, 30),    # Latitude (N)
            (31, 41),    # Longitude (E)
            (42, 49),    # Depth (km)
            (50, 54),    # MD
            (55, 59),    # ML
            (60, 64),    # Mw
            (65, None)   # Location
        ]

        df = pd.read_fwf(StringIO(data_str), colspecs=colspecs, header=None)
        df.columns = ["Tarih", "Saat", "Enlem(N)", "Boylam(E)", "Derinlik(km)", "MD", "ML", "Mw", "Yer"]

        # Convert numeric columns
        for col in ["Enlem(N)", "Boylam(E)", "Derinlik(km)", "Mw"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=["Enlem(N)", "Boylam(E)"])

        # Create datetime column
        df["TarihSaat"] = pd.to_datetime(df["Tarih"] + " " + df["Saat"], errors='coerce')
        now = datetime.utcnow()
        last_days = now - timedelta(days=days)
        df_filtered = df[(df["TarihSaat"] >= last_days) & (df["Mw"] >= min_mw)]

        if df_filtered.empty:
            messagebox.showinfo("Info", "No data after filtering.")
            return

        # Color scale based on magnitude
        def magnitude_color(mag):
            if pd.isna(mag):
                return "gray"
            elif mag < 3.0:
                return "green"
            elif mag < 5.0:
                return "orange"
            else:
                return "red"

        # Create map
        m = folium.Map(location=[39.0, 35.0], zoom_start=6)
        mc = MarkerCluster().add_to(m)

        for _, row in df_filtered.iterrows():
            try:
                lat = float(row["Enlem(N)"])
                lon = float(row["Boylam(E)"])
                mag = float(row["Mw"]) if pd.notna(row["Mw"]) else 2

                popup_text = (
                    f"Date: {row['Tarih']} {row['Saat']}\n"
                    f"Location: {row['Yer']}\n"
                    f"Magnitude (Mw): {row['Mw'] if pd.notna(row['Mw']) else 'Unknown'}\n"
                    f"Depth: {row['Derinlik(km)'] if pd.notna(row['Derinlik(km)']) else 'Unknown'} km"
                )

                folium.CircleMarker(
                    location=[lat, lon],
                    radius=2 + mag,
                    color='black',
                    fill=True,
                    fill_color=magnitude_color(mag),
                    fill_opacity=0.7,
                    popup=popup_text
                ).add_to(mc)
            except:
                continue

        # Add legend
        template = """
        {% macro html(this, kwargs) %}
        <div style="
        position: fixed;
        bottom: 50px; right: 50px; left: auto; width: 150px; height: 120px;
        background-color: white; z-index:9999;
        border:2px solid grey; padding: 10px; font-size:14px;">
        <b>Magnitude (Mw)</b><br>
        <i style="background:green;width:15px;height:15px;display:inline-block;"></i> < 3.0<br>
        <i style="background:orange;width:15px;height:15px;display:inline-block;"></i> 3.0 - 4.9<br>
        <i style="background:red;width:15px;height:15px;display:inline-block;"></i> >= 5.0
        </div>
        {% endmacro %}
        """
        macro = MacroElement()
        macro._template = Template(template)
        m.get_root().add_child(macro)

        # Save and open map
        map_file = "koeri_earthquakes_tkinter.html"
        m.save(map_file)
        full_path = os.path.abspath(map_file)
        webbrowser.open(f"file://{full_path}")
        messagebox.showinfo("Info", f"Map saved and opened in browser:\n{map_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -----------------------------
# Tkinter GUI
root = tk.Tk()
root.title("KOERI Turkiye Earthquake Map")

tk.Label(root, text="How many past days of earthquakes?").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_days = tk.Entry(root)
entry_days.insert(0, "7")
entry_days.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Minimum Mw:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_mw = tk.Entry(root)
entry_mw.insert(0, "0")
entry_mw.grid(row=1, column=1, padx=5, pady=5)

btn = tk.Button(root, text="Show Map", command=lambda: generate_map(int(entry_days.get()), float(entry_mw.get())))
btn.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()

# ============================================================
# Developer Signature (Auto-generated hash)
# ModestusSpider | TurkiyeEarthquakeMap.py | 2025-10-21
# SHA256:  7b1e7cc1fbb72cc1fbb80d4a99d1a55f3e78b51e60e122b6f1a4b5ce9b62ad8b
# ============================================================
