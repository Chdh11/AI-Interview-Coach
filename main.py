import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import google.generativeai as genai
import json
import re
from dotenv import load_dotenv
import os
from gtts import gTTS


load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

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
    """Create prompt for behavioral questions with difficulty"""
    
    job_title = job_analysis.get('job_title', 'the position')
    seniority = job_analysis.get('seniority_level', 'mid-level')
    soft_skills = job_analysis.get('soft_skills', [])
    responsibilities = job_analysis.get('key_responsibilities', [])
    
    # Difficulty-specific requirements
    difficulty_requirements = {
        "easy": """
- Focus on basic workplace scenarios and learning experiences
- Ask about simple challenges and how they overcame them
- Questions about teamwork and communication at entry level
- Example: "Tell me about a time you had to learn something new quickly"
        """,
        "medium": """
- Focus on project ownership and cross-team collaboration  
- Ask about handling competing priorities and difficult decisions
- Questions about leadership moments and conflict resolution
- Example: "Describe a time you had to manage multiple stakeholders with different priorities"
        """,
        "hard": """
- Focus on strategic decision-making and organizational impact
- Ask about leading through crisis and complex problem-solving
- Questions about mentoring, architecture decisions, and business impact
- Example: "Tell me about a time you had to make a critical decision that affected the entire organization"
        """
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
    """Create prompt for technical questions with difficulty"""
    
    job_title = job_analysis.get('job_title', 'the position')
    seniority = job_analysis.get('seniority_level', 'mid-level')
    technical_skills = job_analysis.get('technical_skills', [])
    
    difficulty_requirements = {
        "easy": """
- Focus on fundamental concepts and basic implementation
- Ask about simple coding problems and basic system understanding
- Test core technology knowledge without complex scenarios
- Example: "How would you implement a basic REST API endpoint?"
        """,
        "medium": """
- Focus on practical problem-solving and best practices
- Ask about debugging, optimization, and design patterns
- Test ability to explain trade-offs and handle moderate complexity
- Example: "How would you optimize a slow database query and what factors would you consider?"
        """,
        "hard": """
- Focus on system design, architecture, and complex problem-solving
- Ask about scalability, distributed systems, and technical leadership
- Test ability to design solutions and make architectural decisions
- Example: "Design a distributed system to handle 1 million concurrent users with 99.9% uptime"
        """
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
    """Create prompt for situational questions with difficulty"""
    
    job_title = job_analysis.get('job_title', 'the position')
    industry = job_analysis.get('industry', 'technology')
    team_role = job_analysis.get('team_role', 'individual_contributor')
    
    difficulty_requirements = {
        "easy": """
- Focus on individual contributor scenarios and basic professional situations
- Ask about learning from mistakes and asking for help
- Simple conflict resolution and priority management
- Example: "What would you do if you realized you made an error that affected your team?"
        """,
        "medium": """
- Focus on project ownership and cross-team collaboration
- Ask about managing competing demands and difficult conversations
- Moderate stakeholder management and team coordination
- Example: "How would you handle conflicting requirements from two different departments?"
        """,
        "hard": """
- Focus on organizational leadership and strategic decision-making
- Ask about crisis management and transformational change
- Complex stakeholder management and business-critical decisions
- Example: "What would you do if you had to lead a critical project with unclear requirements and tight deadlines?"
        """
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

def job_description_analysis(job_description, job_profile):
    try:
        genai.configure(api_key=api_key)
        model=genai.GenerativeModel('gemini-2.5-flash')

        formatted_prompt=jd_analysis_prompt.format(
            job_profile=job_profile,
            job_description=job_description
        )

        print("Analyzing Your Job Decription...")
        response=model.generate_content(formatted_prompt)

        json_data= extract_json_from_response(response.text)

        if(json_data):
            print("Job Analysis Complete!")
            return json_data
        else:
            print("Failed to extract any valid data")
            return None
        
    except Exception as e:
        print(f"Error analysing job description: {e}")
        return None

def extract_json_from_response(json_content):
    try:
        json_match = re.search(r'\{.*\}', json_content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            return json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response was: {json_content}")
        return None
    
def generate_questions(job_data, question_type="behavioral", count=5, difficulty="easy"):
    try:
        genai.configure(api_key=api_key)
        model=genai.GenerativeModel('gemini-2.5-flash')

        if(question_type=="behavioral"):
            prompt=create_behavioral_prompt(job_data,count,difficulty)
        elif(question_type=="technical"):
            prompt=create_technical_prompt(job_data,count,difficulty)
        elif(question_type=="situational"):
            prompt=create_situational_prompt(job_data,count,difficulty)
        else:
            print(f"Unknown question type: {question_type}")
            return None
        
        response=model.generate_content(prompt)
        
        questions = parse_questions_response(response.text)
        if questions:
            print(f"✅ Generated {len(questions)} questions successfully!")
            return questions
        else:
            print("❌ Failed to parse questions from response")
            return None
            
    except Exception as e:
        print(f"Error generating questions: {e}")
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
        print(f"Error parsing questions: {e}")
        return None


def record_voice(filename, duration=5, samplerate=44100):
    print(f"Recording for {duration} seconds ...")
    audio_data=sd.rec(
        int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16'
    )
    sd.wait()
    write(filename, samplerate, audio_data)
    print("Audio recording complete!")
    # models = ["tiny", "base", "small", "medium", "large"]
    model = whisper.load_model("small")
    result = model.transcribe(filename)
    return result["text"]


def speak_question_simple(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("question_audio.mp3")
        os.system("afplay question_audio.mp3")  
        
        print("✅ Question audio saved and playing!")
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def interview(job_data, behavioral_question_count=1, technical_question_count=1, situational_question_count=1, difficulty="easy"):
    try:
        answer=[]
        questions=[]
        #get behvioral questions, record answers and append them to answers list
        if(behavioral_question_count!=0):
            behavioral_questions=generate_questions(job_data, "behavioral", behavioral_question_count, difficulty)
            n1=len(behavioral_questions)
            for i in range(0,n1):
                questions.append(behavioral_questions[i])
                print(behavioral_questions[i])
                speak_question_simple(behavioral_questions[i])
                answer.append(record_voice("answer.wav",20))

        #get technical questions, record answers and append them to answers list
        if(technical_question_count!=0):
            technical_questions=generate_questions(job_data, "technical", technical_question_count,difficulty)
            n2=len(technical_questions)
            for i in range(0,n2):
                questions.append(technical_questions[i])
                print(technical_questions[i])
                speak_question_simple(technical_questions[i])
                answer.append(record_voice("answer.wav",20))
        
        #get technical questions, record answers and append them to answers list
        if(situational_question_count!=0):
            situational_questions=generate_questions(job_data, "situational", situational_question_count,difficulty)
            n3=len(situational_questions)
            for i in range(0,n3):
                questions.append(situational_questions[i])
                print(situational_questions[i])
                speak_question_simple(situational_questions[i])
                answer.append(record_voice("answer.wav",20))
        
        evaluate_answer(questions,answer,job_data,difficulty)
        # return answer
    except Exception as e:
        print(f"Error:{e}")
        return None

def evaluate_answer(question, answer, job_data, difficulty="easy"):
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

Instead of: "[another problematic phrase]"
Try: "[improved version]"

RECOMMENDED KEYWORDS TO USE:
- [keyword 1] - [why it's important]
- [keyword 2] - [why it's important]
- [keyword 3] - [why it's important]

OVERALL FEEDBACK:
[2-3 sentences of constructive advice]

Evaluate based on:
1. Structure and clarity
2. Relevance to the question
3. Use of specific examples
4. Professional language
5. Depth appropriate for {difficulty} level
"""
        
        print("Evaluating your answer...")
        response = model.generate_content(evaluation_prompt)
        print(response.text)
        
    except Exception as e:
        print(f"Error evaluating answer: {e}")


def main():
    job_profile=input("Enter Job Profile: ")
    job_description=input("Enter Job description: ")
    difficulty_level=input("Enter the difficulty level of the questions: ") #easy, medium, hard
    job_data=job_description_analysis(job_description,job_profile)

    behavioral_question_count=int(input("Enter number of behavioral questions you want: "))
    technical_question_count=int(input("Enter number of technical questions you want: "))
    situational_question_count=int(input("Enter number of situational questions you want: "))

    interview(job_data,behavioral_question_count, technical_question_count, situational_question_count, difficulty_level)


if __name__ == "__main__":
    main()