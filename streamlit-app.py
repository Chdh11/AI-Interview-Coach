import streamlit as st
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import google.generativeai as genai
import json
import re
from dotenv import load_dotenv
import os
from gtts import gTTS
import tempfile
import time
from io import BytesIO
from faster_whisper import WhisperModel

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-header {
        font-size: 1.5rem;
        color: #2e8b57;
        border-left: 4px solid #2e8b57;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    .job-analysis-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #add8e6;
    }
    .question-box {
        background-color: #1a3d5c;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #daa520;
        margin: 1rem 0;
    }
    .evaluation-box {
        background-color: #1a3d5c;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #90ee90;
    }
</style>
""", unsafe_allow_html=True)

if 'job_data' not in st.session_state:
    st.session_state.job_data = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'interview_complete' not in st.session_state:
    st.session_state.interview_complete = False

jd_analysis_prompt = """
Analyze this job description and extract key information. Return your response as a valid JSON object with no extra text or formatting.

Job Profile: {job_profile}
Job Description: {job_description}

Return EXACTLY this JSON structure with actual values filled in:
{{
  "job_title": "exact title from posting",
  "seniority_level": "entry/mid/senior/lead",
  "technical_skills": ["skill1", "skill2"],
  "soft_skills": ["skill1", "skill2"],
  "industry": "industry type",
  "experience_years": "X-Y years or not specified",
  "team_role": "individual_contributor/team_lead/manager",
  "key_responsibilities": ["responsibility1", "responsibility2"]
}}

IMPORTANT: Return ONLY the JSON object, no explanations or additional text.
"""

def create_behavioral_prompt(job_analysis, count, difficulty="easy"):
    job_title = job_analysis.get('job_title', 'the position')
    seniority = job_analysis.get('seniority_level', 'mid-level')
    soft_skills = job_analysis.get('soft_skills', [])
    responsibilities = job_analysis.get('key_responsibilities', [])
    
    difficulty_requirements = {
        "easy": """- Focus on basic workplace scenarios and learning experiences
- Ask about simple challenges and how they overcame them
- Questions about teamwork and communication at entry level""",
        "medium": """- Focus on project ownership and cross-team collaboration  
- Ask about handling competing priorities and difficult decisions
- Questions about leadership moments and conflict resolution""",
        "hard": """- Focus on strategic decision-making and organizational impact
- Ask about leading through crisis and complex problem-solving
- Questions about mentoring, architecture decisions, and business impact"""
    }
    
    prompt = f"""
Generate {count} behavioral interview questions for a {job_title} position at {seniority} level.

DIFFICULTY LEVEL: {difficulty.upper()}
{difficulty_requirements[difficulty]}

Focus on these soft skills: {', '.join(soft_skills)}
Key responsibilities: {', '.join(responsibilities)}

Requirements for each question:
1. Use STAR method (Situation, Task, Action, Result)
2. Match {difficulty} difficulty level complexity
3. Be specific to this role and seniority level
4. Test real workplace scenarios appropriate for {difficulty} level
5. Be answerable in 2-3 minutes

Format your response as:
1. [First question]
2. [Second question]
3. [Third question]
etc.

Generate ONLY the numbered questions, no additional text.
"""
    return prompt

def create_technical_prompt(job_analysis, count, difficulty="easy"):
    job_title = job_analysis.get('job_title', 'the position')
    seniority = job_analysis.get('seniority_level', 'mid-level')
    technical_skills = job_analysis.get('technical_skills', [])
    
    difficulty_requirements = {
        "easy": """- Focus on fundamental concepts and basic implementation
- Ask about simple coding problems and basic system understanding
- Test core technology knowledge without complex scenarios""",
        "medium": """- Focus on practical problem-solving and best practices
- Ask about debugging, optimization, and design patterns
- Test ability to explain trade-offs and handle moderate complexity""",
        "hard": """- Focus on system design, architecture, and complex problem-solving
- Ask about scalability, distributed systems, and technical leadership
- Test ability to design solutions and make architectural decisions"""
    }
    
    prompt = f"""
Generate {count} technical interview questions for a {job_title} position at {seniority} level.

DIFFICULTY LEVEL: {difficulty.upper()}
{difficulty_requirements[difficulty]}

Required technical skills: {', '.join(technical_skills)}

Requirements for each question:
1. Match {difficulty} difficulty level complexity
2. Focus on practical application appropriate for {difficulty} level
3. Can be answered in 2-3 minutes
4. Test real-world problem-solving at {difficulty} level
5. Specific to the required technologies

Format your response as:
1. [First question]
2. [Second question]
3. [Third question]
etc.

Generate ONLY the numbered questions, no additional text.
"""
    return prompt

def create_situational_prompt(job_analysis, count, difficulty="easy"):
    job_title = job_analysis.get('job_title', 'the position')
    industry = job_analysis.get('industry', 'technology')
    team_role = job_analysis.get('team_role', 'individual_contributor')
    
    difficulty_requirements = {
        "easy": """- Focus on individual contributor scenarios and basic professional situations
- Ask about learning from mistakes and asking for help
- Simple conflict resolution and priority management""",
        "medium": """- Focus on project ownership and cross-team collaboration
- Ask about managing competing demands and difficult conversations
- Moderate stakeholder management and team coordination""",
        "hard": """- Focus on organizational leadership and strategic decision-making
- Ask about crisis management and transformational change
- Complex stakeholder management and business-critical decisions"""
    }
    
    prompt = f"""
Generate {count} situational interview questions for a {job_title} in {industry} industry.

DIFFICULTY LEVEL: {difficulty.upper()}
{difficulty_requirements[difficulty]}

Team role: {team_role}

Requirements for each question:
1. Present realistic workplace scenarios for {difficulty} level
2. Test decision-making appropriate for {difficulty} complexity
3. Match the responsibility level and industry context
4. Start with "What would you do if..." or "How would you handle..."
5. Be specific to the work environment

Format your response as:
1. [First question]
2. [Second question]
3. [Third question]
etc.

Generate ONLY the numbered questions, no additional text.
"""
    return prompt

def extract_json_from_response(json_content):
    try:
        json_match = re.search(r'\{.*\}', json_content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            return json.loads(json_content)
    except json.JSONDecodeError as e:
        st.error(f"JSON parsing error: {e}")
        return None

def job_description_analysis(api_key, job_description, job_profile):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        formatted_prompt = jd_analysis_prompt.format(
            job_profile=job_profile,
            job_description=job_description
        )

        with st.spinner("Analyzing your job description..."):
            response = model.generate_content(formatted_prompt)

        json_data = extract_json_from_response(response.text)

        if json_data:
            st.success("Job Analysis Complete!")
            return json_data
        else:
            st.error("Failed to extract valid data")
            return None
        
    except Exception as e:
        st.error(f"Error analyzing job description: {e}")
        return None

def parse_questions_response(response_text):
    try:
        questions = []
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.\s+', line):
                question = re.sub(r'^\d+\.\s+', '', line)
                if question: 
                    questions.append(question)
        
        return questions if questions else None
        
    except Exception as e:
        st.error(f"Error parsing questions: {e}")
        return None

def generate_questions(api_key,job_data, question_type="behavioral", count=5, difficulty="easy"):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        if question_type == "behavioral":
            prompt = create_behavioral_prompt(job_data, count, difficulty)
        elif question_type == "technical":
            prompt = create_technical_prompt(job_data, count, difficulty)
        elif question_type == "situational":
            prompt = create_situational_prompt(job_data, count, difficulty)
        else:
            st.error(f"Unknown question type: {question_type}")
            return None
        
        with st.spinner(f"Generating {question_type} questions..."):
            response = model.generate_content(prompt)
        
        questions = parse_questions_response(response.text)
        if questions:
            return questions
        else:
            st.error("Failed to parse questions from response")
            return None
            
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return None

def record_audio_streamlit(duration=30):
    try:
        st.info(f"🎤 Recording for {duration} seconds... Speak now!")
        
        countdown_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        samplerate = 44100
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
        
        for i in range(duration):
            countdown_placeholder.text(f"Recording... {duration - i} seconds remaining")
            progress_bar.progress((i + 1) / duration)
            time.sleep(1)
        
        sd.wait()
        countdown_placeholder.empty()
        progress_bar.empty()
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        write(temp_file.name, samplerate, audio_data)
        
        st.success("Recording complete! Processing...")
    
        # using faster-whisper instead of openai-whisper
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, info = model.transcribe(temp_file.name)

        text = " ".join([segment.text for segment in segments])
        
        os.unlink(temp_file.name)
        
        return text
        
    except Exception as e:
        st.error(f"Error recording audio: {e}")
        return None

def evaluate_answer(api_key, question, answer, job_data, difficulty="easy"):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        evaluation_prompt = f"""
You are an expert interview coach. Evaluate this candidate's answer and provide constructive feedback.

CONTEXT:
- Job Title: {job_data.get('job_title', 'N/A')}
- Seniority Level: {job_data.get('seniority_level', 'N/A')}
- Required Skills: {', '.join(job_data.get('technical_skills', []) + job_data.get('soft_skills', []))}
- Difficulty Level: {difficulty}

QUESTION ASKED:
{question}

CANDIDATE'S ANSWER:
{answer}

Please provide evaluation in this EXACT format:

SCORE: [X/10]

STRENGTHS:
- [Strength 1]
- [Strength 2]
- [Strength 3]

AREAS FOR IMPROVEMENT:
- [Area 1]
- [Area 2] 
- [Area 3]

BETTER PHRASING SUGGESTIONS:
Instead of: "[problematic phrase from answer]"
Try: "[improved version]"

RECOMMENDED KEYWORDS TO USE:
- [keyword 1] - [why it's important]
- [keyword 2] - [why it's important]

OVERALL FEEDBACK:
[2-3 sentences of constructive advice]

Evaluate based on:
1. Structure and clarity
2. Relevance to the question
3. Use of specific examples
4. Professional language
5. Depth appropriate for {difficulty} level
"""
        
        with st.spinner("Evaluating your answer..."):
            response = model.generate_content(evaluation_prompt)
        
        return response.text
        
    except Exception as e:
        st.error(f"Error evaluating answer: {e}")
        return None

def api_setup():
    """Method 2: API Key as Initial Setup Step"""
    if 'api_key_validated' not in st.session_state:
        st.session_state.api_key_validated = False
    if 'user_api_key' not in st.session_state:
        st.session_state.user_api_key = ""
    
    if not st.session_state.api_key_validated:
        st.markdown("### 🔑 Welcome! Let's get started")
        st.markdown("To use this AI Interview Coach, you'll need a Google Gemini API key.")
        
        # Instructions
        with st.expander("📖 How to get your API key"):
            st.markdown("""
            1. Go to [Google AI Studio](https://ai.google.dev/)
            2. Click "Create API Key"
            3. Copy the key and paste it below
            4. Keep it safe - don't share it with anyone!
            """)
        
        api_key = st.text_input(
            "Paste your Gemini API Key here:",
            type="password",
            placeholder="AIza..."
        )
        
        # col1, col2 = st.columns(2)
        
        # with col1:
        if st.button("🔐 Validate & Continue", type="primary"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    # Quick test
                    response = model.generate_content("Hello")
                    
                    st.session_state.user_api_key = api_key
                    st.session_state.api_key_validated = True
                    st.success("✅ API Key validated! Redirecting...")
                    st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Invalid API Key: {str(e)}")
            else:
                st.warning("Please paste your API key")
        
        # with col2:
        #     if st.button("🧪 Use Demo Mode"):
        #         st.info("Demo mode selected - limited functionality")
        #         st.session_state.api_key_validated = True
        #         st.session_state.user_api_key = "DEMO_MODE"
        #         st.rerun()
        
        # Don't show the rest of the app
        return None
    
    else:
        return st.session_state.user_api_key

def main():
    api_key = api_setup()
    if(api_key):
        st.markdown('<h1 class="main-header">AI Interview Coach</h1>', unsafe_allow_html=True)
        
        # Sidebar for navigation and progress
        with st.sidebar:
            st.markdown("### Interview Progress")
            
            steps = [
                "Job Description",
                "Analysis", 
                "Setup Questions",
                "Interview",
                "Evaluation"
            ]
            
            for i, step in enumerate(steps, 1):
                if i < st.session_state.current_step:
                    st.markdown(f"✅ {step}")
                elif i == st.session_state.current_step:
                    st.markdown(f"🔄 **{step}**")
                else:
                    st.markdown(f"⏳ {step}")
        
        # Step 1: Job Description Input
        if st.session_state.current_step == 1:
            st.markdown('<div class="step-header">Step 1: Enter Job Details</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                job_profile = st.text_input("Job Profile/Title", placeholder="e.g., Senior Software Engineer")
            
            with col2:
                difficulty = st.selectbox("Difficulty Level", ["easy", "medium", "hard"])
            
            job_description = st.text_area(
                "Job Description", 
                height=200,
                placeholder="Paste the complete job description here..."
            )
            
            if st.button("Analyze Job Description", type="primary"):
                if job_profile and job_description:
                    job_data = job_description_analysis(api_key,job_description, job_profile)
                    if job_data:
                        st.session_state.job_data = job_data
                        st.session_state.difficulty = difficulty
                        st.session_state.current_step = 2
                        st.rerun()
                else:
                    st.warning("Please fill in both job profile and job description.")
        
        # Step 2: Show Analysis
        elif st.session_state.current_step == 2:
            st.markdown('<div class="step-header">Step 2: Job Analysis Results</div>', unsafe_allow_html=True)
            
            if st.session_state.job_data:
                job_data = st.session_state.job_data
                
                # st.markdown('<div class="job-analysis-box">', unsafe_allow_html=True)
                
                col1, col2, col3, col4= st.columns(4)
                
                with col1:
                    st.subheader("Basic Info")
                    st.write(f"**Title:** {job_data.get('job_title', 'N/A')}")
                    st.write(f"**Seniority:** {job_data.get('seniority_level', 'N/A')}")
                    st.write(f"**Industry:** {job_data.get('industry', 'N/A')}")
                    st.write(f"**Experience:** {job_data.get('experience_years', 'N/A')}")
                with col2:
                    st.subheader("Technical Skills")
                    for skill in job_data.get('technical_skills', []):
                        st.write(f"• {skill}")
                with col3:    
                    st.subheader("Soft Skills")  
                    for skill in job_data.get('soft_skills', []):
                        st.write(f"• {skill}")
                with col4:
                    st.subheader("Key Responsibilities")
                    for resp in job_data.get('key_responsibilities', []):
                        st.write(f"• {resp}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("✅ Looks Good! Setup Interview", type="primary"):
                    st.session_state.current_step = 3
                    st.rerun()
        
        # Step 3: Question Setup
        elif st.session_state.current_step == 3:
            st.markdown('<div class="step-header">Step 3: Configure Interview Questions</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                behavioral_count = st.number_input("Behavioral Questions", min_value=0, max_value=10, value=2)
            
            with col2:
                technical_count = st.number_input("Technical Questions", min_value=0, max_value=10, value=2)
            
            with col3:
                situational_count = st.number_input("Situational Questions", min_value=0, max_value=10, value=1)
            
            total_questions = behavioral_count + technical_count + situational_count
            
            if total_questions > 0:
                st.info(f"Total questions: {total_questions} (Estimated time: {total_questions * 2} minutes)")
                
                if st.button("Generate Questions & Start Interview", type="primary"):
                    # Generate all questions
                    all_questions = []
                    question_types = []
                    
                    if behavioral_count > 0:
                        behavioral_q = generate_questions(api_key,
                            st.session_state.job_data, "behavioral", 
                            behavioral_count, st.session_state.difficulty
                        )
                        if behavioral_q:
                            all_questions.extend(behavioral_q)
                            question_types.extend(["behavioral"] * len(behavioral_q))
                    
                    if technical_count > 0:
                        technical_q = generate_questions(api_key,
                            st.session_state.job_data, "technical", 
                            technical_count, st.session_state.difficulty
                        )
                        if technical_q:
                            all_questions.extend(technical_q)
                            question_types.extend(["technical"] * len(technical_q))
                    
                    if situational_count > 0:
                        situational_q = generate_questions(api_key,
                            st.session_state.job_data, "situational", 
                            situational_count, st.session_state.difficulty
                        )
                        if situational_q:
                            all_questions.extend(situational_q)
                            question_types.extend(["situational"] * len(situational_q))
                    
                    if all_questions:
                        st.session_state.questions = all_questions
                        st.session_state.question_types = question_types
                        st.session_state.answers = []
                        st.session_state.current_question_index = 0
                        st.session_state.current_step = 4
                        st.rerun()
            else:
                st.warning("Please select at least one type of question.")
        
        # Step 4: Interview Process
        elif st.session_state.current_step == 4:
            if st.session_state.current_question_index < len(st.session_state.questions):
                current_q_index = st.session_state.current_question_index
                current_question = st.session_state.questions[current_q_index]
                question_type = st.session_state.question_types[current_q_index]
                
                st.markdown("### 🎤 Interview in Progress")
                
                progress = (current_q_index + 1) / len(st.session_state.questions)
                st.progress(progress)
                st.write(f"Question {current_q_index + 1} of {len(st.session_state.questions)} ({question_type.title()})")

                st.markdown(f"### ❓ {current_question}")

                col1, col2 = st.columns([2, 1])
                
                with col1:
                
                    if len(st.session_state.answers) <= current_q_index:
                    
                        if st.button(f"🎤 Record Answer (30 seconds)", key=f"record_{current_q_index}"):
                            answer = record_audio_streamlit(30)
                            if answer:
                                st.session_state.answers.append(answer)
                                st.session_state.recording_complete = True
                                st.rerun()  
                    
                    if len(st.session_state.answers) > current_q_index:
                        st.success("✅ Answer recorded!")
                        
                        st.write("**Your answer:**")
                        st.write(st.session_state.answers[current_q_index])
                        
                        if st.button("➡️ Next Question", key=f"next_{current_q_index}"):
                            st.session_state.current_question_index += 1
                            st.session_state.recording_complete = False
                            
                            if st.session_state.current_question_index >= len(st.session_state.questions):
                                st.session_state.current_step = 5
                            
                            st.rerun()
                
                with col2:
                    st.markdown("### 💡 Tips")
                    if question_type == "behavioral":
                        st.write("• Use STAR method")
                        st.write("• Give specific examples")
                        st.write("• Show impact/results")
                    elif question_type == "technical":
                        st.write("• Think out loud")
                        st.write("• Explain trade-offs")
                        st.write("• Consider edge cases")
                    else: 
                        st.write("• Show problem-solving")
                        st.write("• Consider stakeholders")
                        st.write("• Explain your reasoning")
            
            else:
                st.success("🎉 Interview Complete!")
                st.write("Moving to evaluation...")
                st.session_state.current_step = 5
                st.rerun()
        
        elif st.session_state.current_step == 5:
            st.markdown('<div class="step-header">Step 5: Interview Evaluation</div>', unsafe_allow_html=True)
            
            if not st.session_state.interview_complete:
                st.info("Generating detailed feedback for all your answers...")
                
                evaluations = []
                for i, (question, answer) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
                    with st.spinner(f"Evaluating answer {i+1} of {len(st.session_state.answers)}..."):
                        evaluation = evaluate_answer(
                            api_key,question, answer, st.session_state.job_data, st.session_state.difficulty
                        )
                        evaluations.append(evaluation)
                
                st.session_state.evaluations = evaluations
                st.session_state.interview_complete = True
            
            for i, (question, answer, evaluation) in enumerate(
                zip(st.session_state.questions, st.session_state.answers, st.session_state.evaluations)
            ):
                with st.expander(f"Question {i+1}: {question[:50]}..."):
                    st.write("**Your Answer:**")
                    st.write(answer)
                    
                    # st.markdown('<div class="evaluation-box">', unsafe_allow_html=True)
                    st.write("**Evaluation:**")
                    st.write(evaluation)
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.button("🔄 Start New Interview", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    else:
        st.info("👆 Please configure your API key above to continue")

if __name__ == "__main__":
    main()