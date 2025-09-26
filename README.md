SnapGPT is a full-stack web app powered by OpenAI’s GPT API. It features a modern chat UI, local chat history, and a sarcastic AI personality.

🗂 Project Files (Everything You Need)
snapgpt/
│── app.py              # Flask backend
│── requirements.txt    # All dependencies
│── README.md           # Documentation & instructions
│── .env.example        # Template for your OpenAI API key
│── chats.json          # Local chat history file
│
├── templates/
│   └── index.html      # Frontend UI
└── static/
    └── style.css       # Styling for frontend

🚀 Step-by-Step Setup (Run SnapGPT Perfectly)
1️⃣ Clone the repository
git clone https://github.com/your-username/snapgpt.git
cd snapgpt

2️⃣ Install all dependencies

Make sure Python is installed, then run:

pip install -r requirements.txt


This installs:

Flask → runs the backend server

OpenAI → handles AI responses

python-dotenv → loads API key from .env

3️⃣ Configure your OpenAI API key

Copy .env.example to .env:

copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux


Open .env and add your API key:

OPENAI_API_KEY=your_openai_api_key_here


⚡ Without this, SnapGPT won’t work.

4️⃣ Run the Flask app
python app.py


The server will start at: http://127.0.0.1:5000

Open this link in your browser to access SnapGPT.

5️⃣ Use SnapGPT

Type any message in the input box.

SnapGPT will reply with sarcastic, witty responses.

Chat history is saved locally in chats.json.

You can start new chats or continue previous ones.

6️⃣ Tips for Perfect Use

Keep chats.json in the project folder to save conversation history.

You can edit system_prompt_snapgpt in app.py to tweak the AI’s personality.

Ensure your OpenAI API key is valid and has enough quota.

✅ Done!

That’s it — SnapGPT is fully set up and running!
You can now share your GitHub link and show off the frontend + backend coding you did
