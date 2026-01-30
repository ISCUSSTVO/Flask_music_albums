import os
import requests

def download(url, path):
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            return True
    except:
        return False

# Пути
base = "static/img/"
os.makedirs(base + "artists", exist_ok=True)
os.makedirs(base + "covers", exist_ok=True)

data = {
    "artists": {
        "1.jpg": "https://i.pinimg.com/originals/8e/3a/24/8e3a242a.jpg",
        "2.jpg": "https://i.pinimg.com/originals/1a/58/b5/1a58b532.jpg",
        "3.jpg": "https://i.discogs.com/fMvW_2Rz93X0O6fB3L3I9j9Y_2I=/fit-in/600x600/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-252211-1615814514-6101.jpeg.jpg",
        "4.jpg": "https://i.pinimg.com/736x/01/24/7c/01247c617b8f9e2b694f4a3820235948.jpg"
    },
    "covers": {
        "1.jpg": "https://upload.wikimedia.org/wikipedia/ru/3/3f/Noize_MC_-_The_Greatest_Hits_Vol._1.jpg",
        "8.jpg": "https://m.media-amazon.com/images/I/81I6O-Yy6ML._SL1500_.jpg"
    }
}

for folder, links in data.items():
    for name, url in links.items():
        print(f"Downloading {name}...")
        download(url, base + folder + "/" + name)
