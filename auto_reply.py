import pyautogui
import pytesseract
from google import genai
import pygetwindow as gw
import os
import time
import webbrowser


# ==================================================
# SETTINGS
# ==================================================

CHAT_NAME = "Rajan"

CHECK_INTERVAL = 5

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

CHAT_AREA = (700, 165, 1145, 430)

MESSAGE_BOX = (850, 628)


# ==================================================
# TESSERACT
# ==================================================

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ==================================================
# GEMINI
# ==================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    print('Run: $env:GEMINI_API_KEY="YOUR_API_KEY"')
    exit()

client = genai.Client(api_key=api_key)


# ==================================================
# WHATSAPP WINDOW CHECK
# ==================================================

def is_whatsapp_active():

    try:
        window = gw.getActiveWindow()

        if window is None:
            return False

        title = window.title.lower()

        return "whatsapp" in title

    except:
        return False


# ==================================================
# OPEN WHATSAPP
# ==================================================

def open_whatsapp():

    print("Opening WhatsApp Web...")

    webbrowser.open("https://web.whatsapp.com")

    print("Waiting 20 seconds for WhatsApp...")

    time.sleep(20)


# ==================================================
# SEARCH CHAT
# ==================================================

def search_chat():

    print(f"Opening chat: {CHAT_NAME}")

    if not is_whatsapp_active():

        windows = gw.getWindowsWithTitle("WhatsApp")

        if windows:

            try:
                windows[0].activate()
                time.sleep(1)
            except:
                pass

    pyautogui.hotkey("ctrl", "alt", "/")

    time.sleep(2)

    pyautogui.write(
        CHAT_NAME,
        interval=0.08
    )

    time.sleep(2)

    pyautogui.press("down")

    time.sleep(1)

    pyautogui.press("enter")

    time.sleep(4)

    print("Chat opened successfully.")


# ==================================================
# OCR
# ==================================================

def read_chat():

    if not is_whatsapp_active():

        return None

    screenshot = pyautogui.screenshot()

    chat_area = screenshot.crop(CHAT_AREA)

    chat_area.save("latest_chat_crop.png")

    text = pytesseract.image_to_string(
        chat_area,
        config="--psm 6"
    )

    return text.strip()


# ==================================================
# AI REPLY
# ==================================================

def generate_reply(message):

    print()
    print("Generating AI reply...")

    prompt = f"""
You are a natural WhatsApp auto-reply assistant.

Rules:
- Reply to the actual message.
- Keep the reply short, normally 1 or 2 sentences.
- Use the same language as the user.
- If the user uses Hindi/Hinglish, use Hindi/Hinglish.
- If the user uses English, use English.
- Do not say "Hey there" unless appropriate.
- Do not say you are an AI.
- Do not write an email-style response.
- Sound like a normal person chatting on WhatsApp.

Incoming message:

{message}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if response.text:

            return response.text.strip()

        return None

    except Exception as e:

        print("Gemini error:")
        print(e)

        return None


# ==================================================
# SEND MESSAGE
# ==================================================

def send_reply(reply):

    # First safety check
    if not is_whatsapp_active():

        print("WhatsApp is not active.")
        print("Reply NOT sent.")

        return False

    print()
    print("Typing reply:")

    print(reply)

    pyautogui.click(*MESSAGE_BOX)

    time.sleep(0.5)

    # Check again
    if not is_whatsapp_active():

        print("WhatsApp lost focus.")
        print("Reply NOT sent.")

        return False

    pyautogui.write(
        reply,
        interval=0.03
    )

    time.sleep(1)

    # Final safety check
    if not is_whatsapp_active():

        print("WhatsApp lost focus.")
        print("Reply NOT sent.")

        return False

    pyautogui.press("enter")

    print("Reply sent.")

    return True


# ==================================================
# MAIN
# ==================================================

def main():

    print()
    print("==========================================")
    print("       WHATSAPP AUTO REPLY AI")
    print("==========================================")

    open_whatsapp()

    search_chat()

    print()
    print("==========================================")
    print("BOT READY")
    print("==========================================")

    print("WhatsApp active = BOT WORKING")
    print("Other application = BOT PAUSED")
    print("CTRL+C = STOP BOT")
    print()

    time.sleep(3)


    # ==================================================
    # INITIAL CHAT SNAPSHOT
    # ==================================================

    previous_text = read_chat()

    print("Initial chat snapshot saved.")

    time.sleep(CHECK_INTERVAL)


    # ==================================================
    # MONITORING LOOP
    # ==================================================

    while True:

        try:

            # ------------------------------------------
            # SAFETY
            # ------------------------------------------

            if not is_whatsapp_active():

                print(
                    "\rWhatsApp inactive - bot paused.     ",
                    end="",
                    flush=True
                )

                time.sleep(CHECK_INTERVAL)

                continue


            # ------------------------------------------
            # READ CURRENT CHAT
            # ------------------------------------------

            current_text = read_chat()

            if current_text is None:

                time.sleep(CHECK_INTERVAL)

                continue


            # ------------------------------------------
            # DETECT CHANGE
            # ------------------------------------------

            if current_text != previous_text:

                print()
                print()
                print("==========================================")
                print("NEW CHAT CONTENT DETECTED")
                print("==========================================")

                print(current_text)


                # --------------------------------------
                # AI
                # --------------------------------------

                reply = generate_reply(current_text)


                if reply:

                    print()
                    print("AI REPLY:")
                    print(reply)


                    # ----------------------------------
                    # SEND
                    # ----------------------------------

                    sent = send_reply(reply)


                    if sent:

                        time.sleep(2)

                        updated_text = read_chat()

                        if updated_text:

                            previous_text = updated_text

                    else:

                        print("Reply was NOT sent.")


                else:

                    print("AI reply generation failed.")

                    previous_text = current_text


            else:

                print(
                    "\rWaiting for new message...",
                    end="",
                    flush=True
                )


            time.sleep(CHECK_INTERVAL)


        except KeyboardInterrupt:

            print()
            print()
            print("==========================================")
            print("BOT STOPPED")
            print("==========================================")

            break


        except Exception as e:

            print()
            print("ERROR:")
            print(e)

            time.sleep(5)


# ==================================================
# START
# ==================================================

if __name__ == "__main__":
    main()