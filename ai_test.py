from google import genai
import os
import time


# ==============================
# GEMINI SETUP
# ==============================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    print("Please set your Gemini API key in the terminal.")
    exit()


client = genai.Client(api_key=api_key)


# ==============================
# GENERATE AI REPLY
# ==============================

def generate_reply(message):

    print("Generating AI reply...")

    # Primary model + backup model
    models = [
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.6-flash"
    ]

    prompt = (
        "You are an AI assistant replying to WhatsApp messages.\n"
        "Reply naturally and briefly.\n"
        "Do not explain that you are an AI.\n"
        "Keep the reply suitable for a normal WhatsApp conversation.\n"
        "Use the same language as the incoming message when possible.\n"
        "Do not add unnecessary explanations.\n\n"
        f"Message received:\n{message}"
    )

    # Try each model
    for model in models:

        print(f"Trying model: {model}")

        # Try each model up to 2 times
        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response.text:

                    print(f"Success with {model}")

                    return response.text.strip()

                print("Model returned an empty response.")

            except Exception as e:

                print(f"Attempt {attempt + 1} failed.")
                print(e)

                if attempt == 0:
                    print("Retrying in 3 seconds...")
                    time.sleep(3)

        print(f"Model {model} failed.")
        print("Trying next model...\n")


    print("ERROR: All Gemini models failed.")

    return None


# ==============================
# TEST
# ==============================

def main():

    print("==============================")
    print("       GEMINI AI TEST")
    print("==============================")

    message = input("\nEnter a test message: ")

    if not message.strip():

        print("ERROR: Message cannot be empty.")

        return


    reply = generate_reply(message)


    if reply:

        print()
        print("==============================")
        print("          AI REPLY")
        print("==============================")
        print(reply)
        print("==============================")

    else:

        print()
        print("==============================")
        print("       AI REPLY FAILED")
        print("==============================")
        print("Gemini could not generate a reply.")
        print("==============================")


if __name__ == "__main__":
    main()