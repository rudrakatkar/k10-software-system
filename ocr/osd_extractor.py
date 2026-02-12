import pytesseract
import cv2
import re

def parse(text):
    data = {}
    lat = re.search(r'Lat[:\s]*([\d\.\-]+)', text)
    lon = re.search(r'Lon[:\s]*([\d\.\-]+)', text)
    bat = re.search(r'Bat[:\s]*([\d\.]+)', text)
    sats = re.search(r'Sats[:\s]*(\d+)', text)

    if lat: data["lat"] = lat.group(1)
    if lon: data["lon"] = lon.group(1)
    if bat: data["bat"] = bat.group(1)
    if sats: data["sats"] = sats.group(1)

    return data

def extract_osd(top, bottom):
    gray_top = cv2.cvtColor(top, cv2.COLOR_BGR2GRAY)
    gray_bot = cv2.cvtColor(bottom, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray_top) + \
           pytesseract.image_to_string(gray_bot)

    return parse(text)
