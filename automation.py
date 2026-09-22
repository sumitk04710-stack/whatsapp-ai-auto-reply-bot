import pyautogui
import time
import webbrowser


def open_whatsapp():
    print("Opening WhatsApp Web...")

    webbrowser.open("https://web.whatsapp.com")

    print("Waiting for WhatsApp Web to load...")
    time.sleep(20)

    print("WhatsApp Web should now be ready.")


def search_chat(chat_name):
    print(f"Searching for chat: {chat_name}")

    # Activate WhatsApp browser window
    pyautogui.click(900, 400)

    time.sleep(1)

    # Focus WhatsApp search box
    pyautogui.hotkey("ctrl", "alt", "/")

    time.sleep(2)

    print("Search box focused.")

    # Type chat name
    pyautogui.write(chat_name, interval=0.08)

    print(f"Typed: {chat_name}")

    # Wait for search results
    time.sleep(3)


def open_search_result():
    print("Opening search result...")

    # Move to the search result
    pyautogui.press("down")

    time.sleep(1)

    # Open selected result
    pyautogui.press("enter")

    print("Enter pressed.")

    # Wait for chat to open
    time.sleep(4)

    print("Chat should now be open.")


def test_message_box():
    print("Testing WhatsApp message box...")

    # Click the "Type a message" box
    pyautogui.click(850, 628)

    time.sleep(1)

    # Type test text
    pyautogui.write(
        "TEST - WhatsApp automation is working",
        interval=0.05
    )

    print("Test message typed.")
    print("Message has NOT been sent.")

    time.sleep(2)


def main():
    print("======================================")
    print("       WHATSAPP MESSAGE BOX TEST")
    print("======================================")

    # Step 1: Open WhatsApp Web
    open_whatsapp()

    # Step 2: Search for Rajan
    search_chat("Rajan")

    # Step 3: Open Rajan chat
    open_search_result()

    # Step 4: Test message box
    test_message_box()

    print()
    print("======================================")
    print("       TEST COMPLETED")
    print("======================================")
    print("The test message should be visible in the message box.")
    print("DO NOT PRESS ENTER.")


if __name__ == "__main__":
    main()