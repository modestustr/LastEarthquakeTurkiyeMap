# 🗺️ KOERI Turkiye Earthquake Map (Tkinter + Folium)

**Developer:** ModestusSpider  
**Date:** 2025-10-21  
**Version:** 1.0.0  

---

## 📘 Overview

**Note:** This project is intended **for educational purposes only**.
This lightweight desktop application uses **Tkinter** for the user interface and **Folium** for interactive map rendering.  
It fetches real-time earthquake data from **Kandilli Observatory and Earthquake Research Institute (KOERI)**, filters it by **date** and **magnitude**, and visualizes the results on a color-coded interactive map.  

Each earthquake is represented by a circle marker whose color depends on its magnitude:

- **Green**: Mw < 3.0  
- **Orange**: 3.0 ≤ Mw < 5.0  
- **Red**: Mw ≥ 5.0  

---

## ⚙️ Requirements

### Python Version
- Python **3.8+**

### Dependencies
Install the required packages via `pip`:

```bash
pip install requests pandas folium tkinter

📂 File Structure

📁 Project/
│
├── TurkiyeEarthquakeMap.py         # Main application script
├── koeri_earthquakes_tkinter.html  # Auto-generated interactive map (output)
└── README.md                    # Project documentation

🚀** How to Run**

1-Make sure you have all required dependencies installed.
2-Run the script directly from the terminal or command prompt:
python TurkiyeEarthquakeMap.py
3-A small Tkinter window will appear asking:
    “How many past days of earthquakes?”
    “Minimum Mw:”
4-Enter the desired values and click “Show Map”.
5-The program will:

    Fetch the latest earthquake data from KOERI.    
    Filter it based on your criteria.    
    Generate an interactive Folium map.    
    Automatically open it in your default browser.

🧭 Features
✅ Real-time data retrieval from KOERI
✅ Magnitude-based color coding
✅ Interactive zoomable map with popups
✅ Lightweight GUI via Tkinter
✅ No local database or heavy dependencies
✅ Auto-save of generated map to HTML

📊 Color Legend
| Magnitude (Mw) | Color     | Meaning       |
| -------------- | --------- | ------------- |
| < 3.0          | 🟩 Green  | Minor         |
| 3.0 – 4.9      | 🟧 Orange | Moderate      |
| ≥ 5.0          | 🟥 Red    | Strong/Severe |

📸 Usage Example

Tkinter input window:
Generated interactive Folium map:
Popup example:
      Date: 2025-10-20 12:34
      Location: Istanbul
      Magnitude (Mw): 4.1
      Depth: 10 km

🧑‍💻 Developer Notes

This application is self-contained and does not depend on any external configuration files.
It uses structured fixed-width parsing (pandas.read_fwf) to extract tabular data from KOERI’s raw HTML listing.
Error handling and informative dialogs are implemented via tkinter.messagebox.

🧾 License

This project is released under the MIT License.
Attribution to the original developer is appreciated.

🪪 Developer Signature

Developer:  ModestusSpider
File:        TurkiyeEarthquakeMap.py
Date:        2025-10-21
SHA256:      7b1e7cc1fbb72cc1fbb80d4a99d1a55f3e78b51e60e122b6f1a4b5ce9b62ad8b



