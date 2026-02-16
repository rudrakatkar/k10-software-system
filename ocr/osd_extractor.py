# ocr/osd_extractor.py

import cv2
import re
import easyocr
import numpy as np

# -------------------------------------------------
# Create ONE global EasyOCR reader
# -------------------------------------------------
reader = easyocr.Reader(
    ['en'],
    gpu=True,
    verbose=False
)

# -------------------------------------------------
# OCR helper
# -------------------------------------------------
def ocr_image(img: np.ndarray) -> str:
    if img is None or img.size == 0:
        return ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Heavy upscale (important)
    gray = cv2.resize(gray, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)

    # Sharpen
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    gray = cv2.equalizeHist(gray)

    # Strong threshold
    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    result = reader.readtext(
        thresh,
        detail=0,
        paragraph=False,
        allowlist="0123456789.-"
    )

    return "".join(result)

# Clean number string to keep only digits, dot, and minus
def clean_number(text):
    # Keep only digits, dot, minus
    text = re.sub(r'[^0-9\.-]', '', text)

    # Remove multiple dots
    if text.count('.') > 1:
        parts = text.split('.')
        text = parts[0] + '.' + ''.join(parts[1:])

    return text


# -------------------------------------------------
# Extract LAT & LON using exact pixel ROIs
# -------------------------------------------------
def extract_osd(frame) -> dict:
    data = {}

    lat_roi = frame[1:42, 1477:1824]
    lon_roi = frame[0:47, 107:465]

    lat_raw = ocr_image(lat_roi)
    lon_raw = ocr_image(lon_roi)

    lat_clean = clean_number(lat_raw)
    lon_clean = clean_number(lon_raw)

    print("\n[OCR LAT RAW]:", lat_raw)
    print("[OCR LON RAW]:", lon_raw)

    print("[LAT CLEAN]:", lat_clean)
    print("[LON CLEAN]:", lon_clean)

    # Validate format (must start with 19 or 72)
    if lat_clean.startswith("19"):
        data["lat"] = lat_clean

    if lon_clean.startswith("72"):
        data["lon"] = lon_clean

    return data
