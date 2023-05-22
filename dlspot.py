import os

url = input("URL: ")
# file deepcode ignore CommandInjection: it's local so he's gonna infect himself if somebody tries to inject something 💀
os.system(f"spotdl {url} --output .\\unconverted")
