// app.js - frontend logic (stateless)
const enterBtn = document.getElementById("enterBtn");
const splash = document.getElementById("splash");
const appDiv = document.getElementById("app");
const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const voiceToggle = document.getElementById("voiceToggle");
let voiceReplies = false;

// enter splash
enterBtn?.addEventListener("click", () => {
  splash.style.display = "none";
  appDiv.classList.remove("hidden");
  inputEl.focus();
});

// send handler
sendBtn.addEventListener("click", sendMessage);
inputEl.addEventListener("keydown", (e) => { if(e.key === "Enter") sendMessage(); });

function getMode(){
  const r = document.querySelector('input[name="mode"]:checked');
  return r ? r.value : "normal";
}

async function sendMessage(){
  const txt = inputEl.value.trim();
  if(!txt) return;
  appendMessage(txt, "user");
  inputEl.value = "";
  const mode = getMode();

  // immediate UI feedback
  appendMessage("…", "bot", true); // placeholder loading

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ message: txt, mode: mode })
    });
    const j = await res.json();
    removeLoading();
    appendMessage(j.reply || "No reply from AI.", "bot");
    if(voiceReplies) speakText(j.reply || "No reply from AI.");
  } catch(err){
    removeLoading();
    appendMessage("Error contacting SnapGPT.", "bot");
    console.error(err);
  }
}

function appendMessage(text, who, isLoading=false){
  const d = document.createElement("div");
  d.className = "msg " + (who==="user" ? "user" : "bot");
  d.innerText = text;
  if(isLoading) d.dataset.loading = "1";
  messagesEl.appendChild(d);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function removeLoading(){
  const el = [...messagesEl.children].find(c => c.dataset.loading === "1");
  if(el) el.remove();
}

// voice-to-text (browser Web Speech API)
let recognition = null;
if(window.SpeechRecognition || window.webkitSpeechRecognition){
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SR();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (evt) => {
    const t = evt.results[0][0].transcript;
    inputEl.value = inputEl.value ? (inputEl.value + " " + t) : t;
  };
  recognition.onerror = (e) => console.log("Speech recognition error", e);
}

micBtn.addEventListener("mousedown", () => {
  if(!recognition) { alert("Speech recognition not supported"); return; }
  recognition.start();
});
micBtn.addEventListener("mouseup", () => { if(recognition) recognition.stop(); });

// voice reply toggle
voiceToggle.addEventListener("click", () => {
  voiceReplies = !voiceReplies;
  voiceToggle.style.background = voiceReplies ? "#7C4DFF" : "#fff";
  voiceToggle.style.color = voiceReplies ? "#fff" : "#000";
});

// text-to-speech
function speakText(text){
  if(!text || !('speechSynthesis' in window)) return;
  const u = new SpeechSynthesisUtterance(text);
  u.rate = 1;
  u.pitch = 1;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(u);
}
