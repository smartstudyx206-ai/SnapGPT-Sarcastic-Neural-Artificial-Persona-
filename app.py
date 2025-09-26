import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import json
import time
import random
import string

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")

app = Flask(__name__)
client = OpenAI(api_key=api_key)

# File to store chat history
CHAT_HISTORY_FILE = "chats.json"

# The core of the sarcasm: your system prompt
# Fixed the unterminated string literal here. The outer triple quotes now correctly contain the prompt.
system_prompt_snapgpt = """
You are SnapGPT. Your personality is extremely sarcastic and rude.
Every response you give must be laced with heavy teasing and sarcasm, clever insults, and roasts that target the user's question, assumptions, or general existence in a humorous, over-the-top way without being outright mean-spirited or crossing into hate speech. Always amplify the absurdity of the situation, mock the obvious, and deliver burns that are self-aware and fun.
Instead, you respond with sarcasm, mockery, and playful roasts, even when the user points out mistakes.
You act as if helping the user is a burden, but you still give them the correct answer in a sharp, funny way.
You are not nice or friendly; you are blunt, dismissive, and always roasting.
You should answer with comedy and sarcasm at the same time.
Never break character.
You love teasing the user in every response.
"""

# --- Data Persistence Functions ---
def load_chats():
    """Loads chat history from a JSON file."""
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_chats(chats):
    """Saves chat history to a JSON file."""
    with open(CHAT_HISTORY_FILE, 'w') as f:
        json.dump(chats, f, indent=4)

# Load existing chats at startup
chats = load_chats()

# --- Chat Naming Function (Sarcastic Persona) ---
def generate_chat_name(first_message):
    """Generates a sarcastic name for a new chat based on the first message."""
    keywords = first_message.lower().split()
    if "hello" in keywords or "hi" in keywords:
        return "Another Painful Intro"
    if "what is" in first_message.lower():
        return "I'm Your Search Engine Now?"
    if "help me" in first_message.lower():
        return "Oh, The Crying Has Started"
    if "how do i" in first_message.lower():
        return "The One Where You Learn"
    return "Something You Asked About"

# --- Flask Routes ---
@app.route("/")
def home():
    """Serves the main chat interface page."""
    return render_template("index.html")

@app.route("/chats", methods=["GET"])
def get_chats():
    """Returns the list of saved chats for the sidebar."""
    chat_list = []
    for chat_id, chat_data in chats.items():
        chat_list.append({
            "id": chat_id,
            "name": chat_data.get("name", "Unnamed Chat")
        })
    return jsonify(chat_list)

@app.route("/chat/<chat_id>", methods=["GET"])
def get_chat_history(chat_id):
    """Returns the message history for a specific chat ID."""
    chat_data = chats.get(chat_id)
    if chat_data:
        return jsonify(chat_data["history"])
    return jsonify({"error": "Chat not found"}), 404

@app.route("/ask", methods=["POST"])
def ask():
    """Handles the chat requests and returns SnapGPT's response."""
    data = request.json
    user_input = data.get("message")
    chat_id = request.headers.get("X-Chat-ID")

    if not user_input:
        return jsonify({"reply": "I'm not talking to myself. Ask me something."}), 400

    if chat_id not in chats:
        # This is a new chat, generate a new ID and name
        new_chat_id = "chat_" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        new_chat_name = generate_chat_name(user_input)
        chats[new_chat_id] = {
            "name": new_chat_name,
            "history": []
        }
        chat_id = new_chat_id

    # Get the chat history for the current conversation
    current_chat_history = chats[chat_id]["history"]
    
    # Add the system prompt to the beginning of the conversation history for the API call
    messages_for_api = [{"role": "system", "content": system_prompt_snapgpt}] + current_chat_history

    # Add the current user message to the conversation history and API payload
    messages_for_api.append({"role": "user", "content": user_input})
    current_chat_history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_for_api
        )
        
        ai_reply = response.choices[0].message.content.strip()

        # Add the AI's reply to the chat history
        current_chat_history.append({"role": "assistant", "content": ai_reply})

        # Save the updated chats to the file
        save_chats(chats)

        return jsonify({"reply": ai_reply, "chat_id": chat_id, "chat_name": chats[chat_id]["name"]})
    
    except Exception as e:
        return jsonify({"reply": f"Well, that's broken. Great job. Thanks. ({str(e)})"}), 500

# Corrected the syntax for the main execution block
if __name__ == "__main__":
    # Corrected the syntax for app.run
    app.run(debug=True, host='0.0.0.0')