import os

url = input("URL: ")
# file deepcode ignore CommandInjection: local script, no server
os.system(f"spotdl {url} --output .\\unconverted")
