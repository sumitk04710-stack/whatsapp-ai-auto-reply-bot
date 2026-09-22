import pyautogui
import pytesseract
import time


# Tesseract ka exact location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def read_whatsapp_messages():
    print("Taking screenshot...")

    # Full screen screenshot
    screenshot = pyautogui.screenshot()

    # Full screenshot save karo
    screenshot.save("ocr_test_screen.png")

    print("Full screenshot saved.")

    # WhatsApp ke chat/message area ko crop karo
    # left, top, right, bottom
    chat_area = screenshot.crop((700, 165, 1145, 430))

    # Cropped area save karo
    chat_area.save("whatsapp_chat_crop.png")

    print("WhatsApp chat area cropped.")
    print("Saved as: whatsapp_chat_crop.png")

    # OCR
    print("Reading WhatsApp messages...")

    text = pytesseract.image_to_string(
        chat_area,
        config="--psm 6"
    )

    print()
    print("======================================")
    print("       WHATSAPP OCR RESULT")
    print("======================================")

    if text.strip():
        print(text)
    else:
        print("No text detected.")

    print("======================================")


def main():

    print("======================================")
    print("        WHATSAPP OCR TEST")
    print("======================================")

    print()
    print("5 seconds me screenshot liya jayega.")
    print("WhatsApp Web me Rajan ka chat open rakho.")
    print("Messages clearly visible hone chahiye.")
    print()

    time.sleep(5)

    read_whatsapp_messages()


if __name__ == "__main__":
    main()