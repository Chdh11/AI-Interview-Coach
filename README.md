# AI Interview Coach

**Your personal AI-powered mock interview assistant**, designed to help you prepare confidently for real-world job interviews.

🔗 **[Try the App]()**

This app simulates an actual interview environment by asking role-specific questions based on a job description you provide. You can speak your answers out loud, get real-time transcription, and receive AI-generated feedback to improve your structure, clarity, and confidence.

---

## Project Goals

AI Interview Coach was built to address a common problem: interview anxiety and lack of preparation. Many candidates struggle to structure answers or get flustered under pressure.

This app helps you:

- Practice in private before facing real panels  
- Learn how to tackle behavioral questions effectively  
- Receive structured, repeatable feedback  
- Build confidence by speaking answers aloud  

---

## Features

### Job Description–Driven Interviews
Paste any job description — technical or non-technical — and the app generates tailored behavioral and technical questions aligned with the role.

### Voice-First Experience
Speak your answers aloud using your microphone. The app transcribes your speech in real-time using **Whisper** and responds to you via audio using **gTTS**.

### AI Feedback in Real Time
After you answer, **Gemini** evaluates your response and gives feedback on clarity, relevance, structure, and overall delivery — just like a real interviewer might.

### Difficulty Modes
Choose **Beginner**, **Intermediate**, or **Advanced**. The complexity of questions scales with your selection, making the app suitable for all experience levels.

### Streamlit-Powered UI
Fast-loading, mobile-friendly interface with minimal clicks, simple navigation, and smooth interaction between voice, feedback, and controls.

---

## UI Preview

> *(Add screenshots here)*

---

## 🛠 Tech Stack

| Component        | Tech Used                |
|------------------|--------------------------|
| Frontend UI      | Streamlit                |
| Voice Input      | sounddevice + Whisper    |
| Speech Output    | gTTS                     |
| AI Engine        | Gemini API               |
| Core Logic       | Python                   |
| Deployment       | Streamlit Cloud          |

---

## Future Scope

- Visualize performance trends using graphs and summaries  
- Store and track user interview history for improvement over time  

---

## Key Learnings

### Voice Integration in Web Apps
Learned to integrate real-time voice recording using `sounddevice`, and send the audio to OpenAI’s **Whisper** for seamless transcription.

### Prompt Engineering for Dual Roles & Difficulty Scaling
Refined prompt structures for two key tasks: generating interview questions and evaluating user responses. Also learned to dynamically scale difficulty using prompt tweaks.

### Streamlit UI Implementation
Built a clean, voice-first interface using **Streamlit**, ensuring smooth interaction across devices.

### Gemini API Integration
Successfully integrated **Google Gemini** to generate questions and evaluate responses. Learned to handle token limits, structure prompts effectively, and parse replies into actionable feedback.


