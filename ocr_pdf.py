import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np

PDF_PATH = "Strategy report-260102.pdf"
OUTPUT_FILE = "Strategy report-260102.txt"

# Optional if needed
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(pil_img):
    img = np.array(pil_img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )
    return thresh


# ===== BATCH SETTINGS =====
START_PAGE = 1
END_PAGE =1000     # change if more pages
BATCH_SIZE = 25     # 25 pages at a time (safe)

current_page = START_PAGE
full_text = ""

while current_page <= END_PAGE:
    last_page = min(current_page + BATCH_SIZE - 1, END_PAGE)

    print(f"Processing pages {current_page} to {last_page}...")

    pages = convert_from_path(
        PDF_PATH,
        dpi=300,
        first_page=current_page,
        last_page=last_page
    )

    for i, page in enumerate(pages):
        page_number = current_page + i
        print(f"OCR Page {page_number}")

        processed = preprocess_image(page)

        text = pytesseract.image_to_string(
            processed,
            lang="eng+hin+mar",
            config="--oem 3 --psm 6"
        )

        full_text += f"\n\n===== PAGE {page_number} =====\n{text}"

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(full_text)

    current_page = last_page + 1

print("BATCH OCR COMPLETED SUCCESSFULLY!")
