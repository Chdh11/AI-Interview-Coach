# AI Interview Coach

[![Deployed on Streamlit](https://img.shields.io/badge/Deployed%20on-Streamlit-ff4b4b?logo=streamlit)](https://ai-interview-coach.streamlit.app)
[![Built with Python](https://img.shields.io/badge/Built%20with-Python-blue?logo=python)](https://www.python.org/)
[![Uses Faster Whisper](https://img.shields.io/badge/Speech%20to%20Text-FasterWhisper-blueviolet)](https://github.com/guillaumekln/faster-whisper)
[![AI Engine: Gemini](https://img.shields.io/badge/AI%20Engine-Gemini-orange)](https://deepmind.google/technologies/gemini/)
[![Project Status](https://img.shields.io/badge/Status-Complete-brightgreen)]()

Your personal AI-powered mock interview assistant, designed to help you prepare confidently for real-world job interviews.

🔗[[Try the App]](https://ai-interview-coach-11.streamlit.app/)

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

- **Voice-First Experience**: Speak your answers aloud using your microphone. The app transcribes your speech in real-time using **Faster Whisper** and responds to you via audio using **gTTS**.

- **AI Feedback in Real Time**: After you answer, **Gemini** evaluates your response and gives feedback on clarity, relevance, structure, and overall delivery — just like a real interviewer might.

- **Difficulty Modes**: Choose **Beginner**, **Intermediate**, or **Advanced**. The complexity of questions scales with your selection, making the app suitable for all experience levels.

- **Streamlit-Powered UI**: Fast-loading, mobile-friendly interface with minimal clicks, simple navigation, and smooth interaction between voice, feedback, and controls.

---

## 💻 UI Preview
<img width="1171" height="786" alt="Screenshot 2025-08-01 at 6 15 21 PM" src="https://github.com/user-attachments/assets/5dc0b879-51cc-43b5-9f39-05b78073b3c6" />
<img width="1185" height="785" alt="Screenshot 2025-08-01 at 2 44 56 PM" src="https://github.com/user-attachments/assets/105b2efa-953a-46b6-9fc9-135ef7a236b5" />
<img width="1221" height="786" alt="Screenshot 2025-08-01 at 2 46 03 PM" src="https://github.com/user-attachments/assets/2b9d3366-7637-4a11-af1b-77e70e744d81" />
<img width="1211" height="786" alt="Screenshot 2025-08-01 at 2 47 19 PM" src="https://github.com/user-attachments/assets/a6932851-82e2-444f-ad72-c6879c995c59" />
<img width="1210" height="729" alt="Screenshot 2025-08-01 at 5 40 23 PM" src="https://github.com/user-attachments/assets/9fd4878b-bd4e-4405-9e71-8f943c9843dc" />

---

## 🛠 Tech Stack

| Component        | Tech Used                |
|------------------|--------------------------|
| Frontend UI      | Streamlit                |
| Voice Input      | sounddevice +  Faster Whisper    |
| Speech Output    | gTTS                     |
| AI Engine        | Gemini API               |
| Core Logic       | Python                   |
| Deployment       | Streamlit Cloud          |

---

## 🧠 Key Learnings

- **Voice Integration in Web Apps**: Learned to integrate real-time voice recording using `sounddevice`, and send the audio to **Faster Whisper** (a faster, lightweight version of Whisper) for efficient transcription.

- **Prompt Engineering for Dual Roles & Difficulty Scaling**: Refined prompt structures for two key tasks: generating interview questions and evaluating user responses. Also learned to dynamically scale difficulty using prompt tweaks.

- **Streamlit UI Implementation**: Built a clean, voice-first interface using **Streamlit**, ensuring smooth interaction across devices.

- **Gemini API Integration**: Successfully integrated **Google Gemini** to generate questions and evaluate responses. Learned to handle token limits, structure prompts effectively, and parse replies into actionable feedback.

---

## 📈 Future Scope

- Visualize performance trends using graphs and summaries  
- Store and track user interview history for improvement over time  

---
**Created By: Chhavi Dhankhar**
