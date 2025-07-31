# AI Interview Coach

**AI Interview Coach** is a voice-based interview simulator that runs in the terminal. It helps you prepare for job interviews by generating tailored questions, recording your spoken answers, and providing structured feedback. Questions are personalized based on the job description and your preferred difficulty level.

This project simulates real interview dynamics by combining job-specific question generation, voice interaction, and automated answer evaluation.

---

## What This Project Does

- Analyzes job descriptions to extract relevant information.
- Generates customized **behavioral**, **technical**, and **situational** questions.
- Converts questions into speech using text-to-speech.
- Records your spoken answers and transcribes them using speech-to-text.
- Evaluates your answers using AI and provides actionable feedback.

Difficulty levels (`easy`, `medium`, `hard`) are included to adapt to different experience levels and help users gradually build confidence.

---

## Key Learnings

### Speech-to-Text with Whisper
- Used OpenAI Whisper to transcribe user responses.
- Handled real-time audio recording and audio file processing.

### Text-to-Speech with gTTS
- Used `gTTS` to convert generated questions into spoken prompts.
- Enabled real-time playback to simulate an actual interview experience.

### Content Generation and Evaluation with Google Gemini
- Used Gemini (gemini-2.5-flash) for:
  - Parsing and analyzing job descriptions.
  - Generating structured interview questions.
  - Providing detailed feedback based on user's spoken answers.

### Audio Recording with sounddevice
- Used `sounddevice` and `scipy.io.wavfile` to record and process user voice inputs.

---

## Workflow

1. **Input Job Details**  
   The user provides the job title and description.

2. **Job Analysis**  
   The system uses Gemini to extract job-specific information such as skills, responsibilities, industry, and role level.

3. **Question Generation**  
   Behavioral, technical, and situational questions are generated based on the job data and difficulty level selected by the user.

4. **Voice Interaction**  
   Questions are converted to audio and played. The user's verbal response is recorded and transcribed.

5. **Answer Evaluation**  
   The transcribed response is evaluated by Gemini for clarity, relevance, structure, and use of examples. Feedback includes score, strengths, areas for improvement, and suggested keywords.

---

## Future Scope

- Add a user interface using web frameworks like React or Streamlit.
- Visualize performance trends using graphs and summaries.
- Store and track user interview history for improvement over time.

---

## Technologies Used

- Python
- Google Generative AI (Gemini API)
- OpenAI Whisper
- gTTS (Google Text-to-Speech)
- sounddevice, scipy
- dotenv, regex, JSON