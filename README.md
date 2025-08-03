# AI Interview Coach

[![Deployed on Streamlit](https://img.shields.io/badge/Deployed%20on-Streamlit-ff4b4b?logo=streamlit)](https://ai-interview-coach.streamlit.app)
[![Built with Python](https://img.shields.io/badge/Built%20with-Python-blue?logo=python)](https://www.python.org/)
[![Uses Whisper](https://img.shields.io/badge/Speech%20to%20Text-Whisper-blueviolet)](https://github.com/openai/whisper)
[![AI Engine: Gemini](https://img.shields.io/badge/AI%20Engine-Gemini-orange)](https://deepmind.google/technologies/gemini/)
[![Project Status](https://img.shields.io/badge/Status-Complete-brightgreen)]()

Your personal AI-powered mock interview assistant, designed to help you prepare confidently for real-world job interviews.

🔗 [[Try the App]](https://ai-interview-coach-11.streamlit.app/)

This app simulates an actual interview environment by asking role-specific questions based on a job description you provide. You can speak your answers out loud, get real-time transcription, and receive AI-generated feedback to improve your structure, clarity, and confidence.

---

## ☕️ Project Goals

AI Interview Coach was built to address a common problem: interview anxiety and lack of preparation. Many candidates struggle to structure answers or get flustered under pressure.

This app helps you:

- Practice in private before facing real panels  
- Learn how to tackle behavioral questions effectively  
- Receive structured, repeatable feedback  
- Build confidence by speaking answers aloud  

---

## 💬 Features

- **Job Description–Driven Interviews**: Paste any job description — technical or non-technical — and the app generates tailored behavioral and technical questions aligned with the role.

- **Voice-First Experience**: Speak your answers aloud using your microphone. The app transcribes your speech in real-time using **Whisper** and responds to you via audio using **gTTS**.

- **AI Feedback in Real Time**: After you answer, **Gemini** evaluates your response and gives feedback on clarity, relevance, structure, and overall delivery — just like a real interviewer might.

- **Difficulty Modes**: Choose **Beginner**, **Intermediate**, or **Advanced**. The complexity of questions scales with your selection, making the app suitable for all experience levels.

- **Streamlit-Powered UI**: Fast-loading, mobile-friendly interface with minimal clicks, simple navigation, and smooth interaction between voice, feedback, and controls.

---

## 💻 UI Preview

<img width="1348" height="782" alt="Screenshot 2025-08-03 at 1 25 39 PM" src="https://github.com/user-attachments/assets/2d3ea4e3-e870-4df4-9384-ffd82d6649c1" />
<img width="1349" height="783" alt="Screenshot 2025-08-03 at 1 26 19 PM" src="https://github.com/user-attachments/assets/ba189d24-ecb9-4b04-bea6-cab5c7bdb98e" />
<img width="1350" height="783" alt="Screenshot 2025-08-03 at 1 26 50 PM" src="https://github.com/user-attachments/assets/332c8184-045c-4df5-ab8c-4bd2092bd190" />
<img width="1343" height="785" alt="Screenshot 2025-08-03 at 1 27 32 PM" src="https://github.com/user-attachments/assets/74797b75-46da-43c4-b7d3-4b3114f7c35d" />
<img width="1353" height="784" alt="Screenshot 2025-08-03 at 1 28 34 PM" src="https://github.com/user-attachments/assets/d806d806-d76c-4dc6-8da7-b4600df69fc6" />

---

## 🛠 Tech Stack

| Component        | Tech Used                |
|------------------|--------------------------|
| Frontend UI      | Streamlit                |
| Voice Input      | Streamlit audio input + Whisper    |
| Speech Output    | gTTS                     |
| AI Engine        | Gemini API               |
| Core Logic       | Python                   |
| Deployment       | Streamlit Cloud          |

---

## 🧠 Key Learnings

- **Voice Integration in Web Apps**: Learned to integrate real-time voice recording using `sounddevice` (changed to streamlit audio input), and send the audio to OpenAI’s **Whisper** for seamless transcription.

- **Prompt Engineering for Dual Roles & Difficulty Scaling**: Refined prompt structures for two key tasks: generating interview questions and evaluating user responses. Also learned to dynamically scale difficulty using prompt tweaks.

- **Streamlit UI Implementation**: Built a clean, voice-first interface using **Streamlit**, ensuring smooth interaction across devices.

- **Gemini API Integration**: Successfully integrated **Google Gemini** to generate questions and evaluate responses. Learned to handle token limits, structure prompts effectively, and parse replies into actionable feedback.

---

## 📈 Future Scope

- Store user history, show progress graphs
- Add emotion analysis or confidence rating
- Export transcripts + feedback as PDF
- Replace gTTS with more natural TTS like ElevenLabs

---
**Created By: Chhavi Dhankhar**
