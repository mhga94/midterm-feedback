"""
feedback_app.py  –  Student Midterm Feedback Portal
====================================================
HOW TO USE (for the TA):
  1. Paste your `fb_ma` and `submission_code` dictionaries into the
     CONFIGURATION section below.
  2. Place this file in the same folder as the student notebooks.
  3. Run with:  streamlit run feedback_app.py

VERIFICATION LOGIC:
  The app reads each student's .ipynb file and pulls the second word
  found in the notebook (second non-empty token across all cells, in order).
  Students need to supply that word to unlock their feedback.
"""

import csv
import json
import re
import streamlit as st
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION  ← paste your dictionaries here
# ─────────────────────────────────────────────────────────────────────────────

# Maps student first name → feedback string (multi-line strings are fine)
fb_ma: dict[str, str] = {
    "Ayush" : """
        **Ayush**
        
        Q1: I love the premise for this and great to link it to the paper you have studied. It's a simple game but had you testing out the conditional loops very effectively. Error handling is a nice touch and the interface with the game is logical and user-friendly. Perhaps it would have been interesting to explore the possibility of breaking the game when it rains before you have performed the ritual, rather than finding that out only after you have chosen to perform it.
        
        Q2: Again, a great premise and practice for a real-world situation. A bit to unpack here regarding the functionality and effectiveness of the code. The use of multiple nested for loops is something we might usually try to avoid, as computation can become a limiting factor with larger datasets and it's easy to misplace one's sequencing. Running your code again (and removing the print() function from the final line to give a clearer view of the resulting dictionary (print and dictionaries don't play very well together)), we can see that there are a couple of errors to be addressed. 
        1. The years of 1750/1751 are not captured by the cleaning function and the 1751s are treated as a new dictionary entry rather than a subdivision. In your version you might have needed yet another for loop to capture this, further supporting the need to vectorize or break down your code into something more manageable (with functions, usually).
        2. The translate function does not seem to have worked as intended, returning none for all translations.
        
        Q3: Splitwise is a great app and thus I am fully invested in this question. I like the way it is set out. Again, a couple of thoughts:
        1. The math doesn't quite net out in the way that it should. It would have benefited from some extra testing in how the settlements are calculated.
        2. You have used lambda functions in the sort section which is beyond what we have covered in class. I don't see any mention of it in your chat log so that leaves me suspicious as to your curiosity about what the LLM generated for Q3...
        
        Overall, I thought your creativity was excellent - particularly on question 1. A couple of issues with the code in questions 2 and 3 would have affected that 1% of the mark. On prompting, your prompts are extensive and detailed, which is good to see, and you successfully refined the approach the LLM first tried to give you with ideas of your own. The code definitely stretched your understanding of what we have covered so far, I would have liked to see a little more inquisitiveness around new topics that came up (lambda functions, breaks in loops), as well as some more debugging to ensure that the code is doing what you intended.
        """,
    "Anthony" : """
        **Anthony**

        Prompting: I like the way you've given the LLM as much information as possible. It's given you a much better chance at a personalized task. Also great to see you telling the LLM to not give you the answers. 

        Coverage of concepts: You've done a great job covering the various topics that we've done in class together.

        Creativity: I like the way the LLM really captures topics close to your interest areas. You're creative with your prompting and it even included a quote! 

        Overall: This is a well thought out example of a midterm. I love the creativity and personality that you have brought into it. Your prompting is curious and maintains a strong critical discourse with the LLM. Great work, Anthony!
        
        """,
    "Ben" : """
        **Ben**

        Prompting: Your prompting starts off by asking the LLM whether various snippets of code are correct. It's great that you want to check the accuracy, but have faith in yourself! Just asking the agent whether code is correct won't necessarily give you the learning opportunities. Your question about append is great, getting the LLM to explain reasoning rather than just checking accuracy. It's better to ask the agent - rather than "what is wrong with this code" ask about the function/method that you're using. Over the course of the script your prompting gets more detailed and that is great progress - well done!
        
        Coverage of concepts: You've included a range of concepts. I like the use of error handling, rounding values, if/elif and other conditional loops.

        Creativity: I liked the trade problem with dictionaries and surplus calculations. Unfortunately, without additional guidance, the LLM is not very creative with its own ideas for midterm coding problems. I would have loved to see a little more personality and creativity in choosing the subject matter of the problems. 

        Overall: Great work covering the concepts we've studied so far this semester! I loved the variety of questions, the error handling and particularly the trade question. 
        
        """,
    "Chi" : """
        **Chi**
        
        Prompting: I really like your prompting style, it's clear and asks good questions of the LLM without just brute force-ing answers out of it. You are inquisitive about the use of class and the various parameters that are set into it - including new functions and self.x methods. 

        Coverage of concepts: You cover a wide range of concepts here and have gone well beyond them with the introduction of class. You did that in the proper way, though, getting the LLM to explain to you in detail and querying where necessary.

        Creativity: I like the disaster relief concept, it's a great way to try out your new knowledge in the structural setting of a set of logins and basic program logic. 

        Overall: Great effort on the assignment and good use of the LLM for self-education on a new set of python skills!
        
    """,
    "Chris" : """
        **Chris**

        Prompting: I like your prompting style because it's detailed and ensures that the LLM has minimal options to go off script. It feels at times like you're using another LLM/chat to generate answers for you - when you ask Claude to write a function and give it a hint, that to me feels like it came from elsewhere. If possible, please provide **all** your chat logs so that they can be evaluated. Using LLMs to prompt one another is a very effective way of doing things, it's just helpful for marking to have both. What is great is even when you have been given the full function by the LLM, you take care to ask questions of it that demonstrate understanding of the code. I am glad you took the time to understand lambda as well, since including that without understanding it could have caused problems.

        Coverage of concepts: Great work on functions particularly here, they are super useful for reproducing your results quickly and efficiently on large datasets like this one. 

        Tips: The data loading that the LLM has suggested is perhaps a little cumbersome, it may be worth looking up the pandas get_csv functions to auto load data into a variable. That could have transformed your 40-line first cell to something like 10 lines (even with the try-except block). For dictionaries it is often more effective to "print" them without the print function and just call the variable in the cell, as the visualization is cleaner. 
        
        Creativity: Using real world data is an important step forward and it was great to see you engaging with a dataset like OWID. Maybe a good building point would have been to graph some of the data using python or to explore different data manipulation packages like pandas. 

        Overall: Amazing work on functions, conditionals and dictionaries. I thought this was an excellent long-form exam and got you working with a proper real-world dataset and analysis toolbox. 
    
    """,
    "Ev" : """
        **Ev**

        Prompting: I like your prompting style a lot and you avoided the cardinal sin of just pasting your code that wasn't working into the LLM - great work on that. You are inquisitive and structured in your responses, I particularly liked your deep dive on len() versus .__len__() and the debate on object orientation. 

        Coverage of concepts: You got the LLM to give you a good range of problems. Manipulating awkward data like nested dictionaries and lists is an important skill - the recursive function in Q6 was a neat piece of code. 

        Tips: When printing dictionaries, it's often clearer to visualize them by calling them directly in a cell rather than using the print() function. 

        Creativity: Nicely done prompting the LLM to give you more interesting topics to work on. It has provided a good variety of tasks that test you and not left you with boring generic topics. 

        Overall: Your LLM engagement is excellent - thoughtfully done and inquisitive too. The creativity was good and the range of topics was comprehensive. It might have been nice to see some longer-form/multi-part questions to get some more real-world practice. Great work overall and don't be hard on yourself! You're doing a fantastic job and have got all the concepts down.
    
    """,
    "Linhang" : """
        **Linhang**

        Prompting: You've spent a good amount of time focused on the prompt - this is exactly as I had envisaged with this midterm. Setup is key and your interactions were detailed and thoughtful - great job!

        Coverage of concepts: Great coverage of the concepts that we have looked at together. You have mostly focused on dictionaries, functions and conditional loops which is a good way to do it. Perhaps some different data structures would have been nice to have - sets/tuples etc. - this was very consistent with the problem though. In problem 5, you've used a dictionary comprehension in line 25. While this is a very nice and compact use of code, we haven't covered it yet so I would have liked to see more evidence of you exploring that topic with the LLM. The same goes for the lambda sort in line 15 of problem 6.

        Creativity: I loved this problem, it is (obviously) unique to you and an excellent real-world application of the concepts we have learned. In terms of things that ran through my head as possibilities: a random WeChat link/alphnumeric string generator could have been an interesting way to go for verifications.

        Tips: In your calculate_ticket_price function, it might have been a good catch-all to have the final nested elif (night_type == "regular") as an else. In problem 4 line 49, I'm not sure about your if not booking["confirmed"] line. You're just calling the dictionary key so I imagine it would need to be something like if booking["confirmed"] != True (or == False). It could well work in your code, but it makes more sense to have a clear if statement to others reviewing your code.

        Overall: I love the way you've approached this problem and the effort put into thoughtful prompting of the LLM. You've used some more advanced concepts too in the answers to the problems, so be sure to have revised those to make sure you are across the details of what the code is doing. Great job! 
        
    """,
    "Maria" : """
        **Maria**

        Prompting: You've done some querying of the LLM asking about integers vs floats and asking thoughtful questions about why the code is running in the way it does. Your deep dive into seed and how the random integer works is great as well, asking all the right questions! Later on it gets a bit more "point and shoot" prompting - it's definitely a good idea to be asking "why is this wrong" instead of just asking the LLM to fix it, but still it would be even better to query the LLM on what you think the problem might be "How do I use f strings in Python?", for example. 

        Coverage of concepts: You've got the LLM to cover the main topics well and in a structured way. 

        Creativity: It's great to see you driving the LLM to create a truly interesting and relevant problem set for you. 

        Overall: This was a long and thorough exploration of the topics we've covered together in class - well done! I love the creativity and the way that you've personalized it to you. Given the length of the assignment, I can definitely understand why your prompting got less inquisitive over the course of it, but you stayed curious ultimately and queried the LLM on harder topics like lambda. Overall this was excellent work and hopefully helped you practise the core topics to feel more comfortable!
        
    """,
    "Nick" : """
        **Nick**

        Prompting: You've taken good time to establish the parameters of the task and guided the LLM into something that you wish to attempt - this is a great first step. Second, asking for the full run-through of classes off the bat is a sensible choice. I like the inclusion of time.sleep(), it gives a more real-world feel to the orbital decay problem - nice!

        Coverage of concepts: Good coverage of concepts and nice to expand the knowledge a bit with Classes.

        Creativity: You worked on the setup well and established a very nice narrative/long-form question. Great job!

        Overall: This is an excellent creative problem set that targets all of our topics well. It was relatively short but managed to cover the requisite material. Perhaps it would have been interesting to explore a combination question testing multiple concepts at once. You didn't need much prompt help at all, which is great. Well done!
    """,
    "Peter" : """
        **Peter**

        Prompting: Your midterm prompt is really excellent - great examples and guidance for the LLM plus plenty of evidence to draw from. Love it. 

        Coverage of concepts: You've covered a good range of topics. The LLM throws a lot of code at you and there were a couple of moments where you could have interrogated it a bit more - there's a list comprehension in there for the add ons section, for example. 

        Creativity: I like the variety of questions, that is great to see and good range of lengths too. You've brought in your own experience and interests, which is exactly what we wanted to see. 

        Overall: This is an excellent effort, Peter. You've done a lot of verification with the LLM and it gave extensive answers - this can be good but could also lead to information overload. Consider limiting the LLM responses to test yourself and coding skills - though it's obvious you had your own tries at problems before getting it involved. Great work! 

    """,
    "Roshan" : """
        **Roshan**

        Prompting: I like the direction you have with your prompting, it is clear and makes sure you are getting what you need from the LLM. Great frame setup at the beginning too. It would have been good to see more interactivity with the LLM, open-ended questions and dialogue over the best way to test concepts, for example. 

        Coverage of concepts: You've covered a good range of concepts. There was perhaps room for a few more whimsical ones like randoms.

        Creativity: I like the peers question, not sure how Prof King is going to feel about being listed as a student though...! 

        Overall: Nice work, Roshan. A well-constructed midterm that tests the key ideas and reflects your individual capabilities and interests. 
        
    """,
    "Seiyoon" : """
        **Seiyoon**

        Prompting: I like your direct style of prompting, it's clear and detailed. You've given the LLM plenty of context and material to work with to make the midterm specific to you. I also like the dialogue you have with it on the number of countries to test and trying to establish an optimum solution there. 

        Coverage of concepts: You've got the LLM to incorporate the concepts we've covered in a linear fashion.  

        Creativity: I really like the AI and policy lens. This is a great reflection of your interest areas and the linear nature of the problem is satisfyingly real-world in nature.

        Overall: Sadly there seems to be a problem with the Streamlit app - it seems to be in html rather than Python code so maybe a copy/paste issue somewhere. That aside, I loved the content and structure of this and you've done some great work with the LLM to bring everything together. Nicely done!
        
    """,
    "Sophie" : """
        **Sophie**

        Prompting: You've done a great job getting the prompt refined for your midterm. I like that you gave it options to evaluate and continuously kept updating the structure. Something else I loved was you asking about potential bad outcomes as well as what the ideal version would be.

        Coverage of concepts: Nice pacing of the problems and coverage of the concepts involved. 

        Creativity: The way you've guided the LLM on creating the assignment is excellent. You've also been creative in your conversations, looking to learn about debugging techniques and other moments where you show great interaction and curiosity. 

        Overall: You've demonstrated a strong command of the concepts in the framework of a well-designed midterm that reflects your interests. Great work, Sophie!

    """
}

# Maps student first name → path to their .ipynb file
submission_code: dict[str, str] = {
    "Ayush"   : r"Ayush_GLBL5050_Midterm_Ayush.ipynb",
    "Anthony" : r"Anthony_Midterm.ipynb",
    "Ben"     : r"Ben_Midterm_Exam.ipynb",
    "Chi"     : r"Chi_GLBL_5050_midterm.ipynb",
    "Chris"   : r"Chris_midterm_climate_analysis(1).ipynb",
    "Ev"      : r"Evan_python_midterm_exam.ipynb",
    "Linhang" : r"Linhang_Midterm(2).ipynb",
    "Maria"   : r"Maria_midterm_exam.ipynb",
    "Nick"    : r"Nick_midterm.ipynb",
    "Peter"   : r"Pete_Midterm_python_global_affairs_v3.ipynb",
    "Roshan"  : r"Roshan_Take_Home_Midterm_FINAL.ipynb",
    "Seiyoon" : r"Seiyoon_Midterm.ipynb",
    "Sophie"  : r"Sophie_GLBL5050 Mid-term Exam_Sophie Gao.ipynb"
}

# Path to the CSV file containing Gemini Flash 2.5 feedback
# Expected format: col 0 = student first name, col 2 = AI feedback
AI_FEEDBACK_CSV = "midterm_feedback_results_revised.csv"

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _extract_second_word(notebook_path: str) -> str | None:
    """Return the second whitespace-delimited word found in the notebook."""
    try:
        nb = json.loads(Path(notebook_path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    for cell in nb.get("cells", []):
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        words = re.split(r"\s+", source.strip())
        words = [w for w in words if w]   # drop empties
        if len(words) >= 2:
            return words[1]
    return None


def _normalise(word: str) -> str:
    """Lower-case and strip surrounding punctuation for lenient matching."""
    return word.strip().lower().strip("\"'`#*_")


def _md_to_html(text: str) -> str:
    """Convert a simple markdown string to HTML for rendering inside a div."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    paras = re.split(r'\n{2,}', text.strip())
    html_parts = []
    for para in paras:
        lines = para.strip().splitlines()
        if all(l.strip().startswith(("- ", "* ")) for l in lines if l.strip()):
            items = "".join(
                f"<li>{l.strip().lstrip('-* ')}</li>" for l in lines if l.strip()
            )
            html_parts.append(f"<ul>{items}</ul>")
        else:
            html_parts.append(f"<p>{'<br>'.join(lines)}</p>")
    return "\n".join(html_parts)


@st.cache_data
def _load_ai_feedback(csv_path: str) -> dict[str, str]:
    """Load AI feedback from CSV. Col 0 = name, col 2 = feedback."""
    result: dict[str, str] = {}
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header row
            for row in reader:
                if len(row) >= 3:
                    name = row[0].strip()
                    feedback = row[2].strip()
                    if name:
                        result[name] = feedback
    except FileNotFoundError:
        pass
    return result


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Midterm Feedback",
    page_icon="📝",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Page background */
    .stApp {
        background: #f5f0e8;
    }

    /* Card column label */
    .card-label {
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        font-size: 0.8rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 0.5rem;
    }
    .card-label span {
        display: inline-block;
        background: #1a1a2e;
        color: #f5f0e8;
        border-radius: 4px;
        padding: 0.15rem 0.55rem;
        font-size: 0.75rem;
    }
    .ai-label span {
        background: #1a6b5a;
    }

    /* Card wrapper */
    .feedback-card {
        background: #ffffff;
        border: 1px solid #e0d8cc;
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-top: 0.5rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    }
    .feedback-card p, .feedback-card li {
        font-size: 0.97rem;
        line-height: 1.75;
        color: #2b2b2b;
        margin: 0 0 0.75rem;
    }
    .feedback-card strong { color: #1a1a2e; }
    .feedback-card ul { padding-left: 1.4rem; }
    .feedback-card h1, .feedback-card h2, .feedback-card h3 {
        font-family: 'DM Serif Display', serif;
        color: #1a1a2e;
        margin-top: 1.2rem;
    }

    /* Header strip */
    .header-strip {
        background: #1a1a2e;
        color: #f5f0e8;
        border-radius: 12px;
        padding: 2rem 2.5rem 1.8rem;
        margin-bottom: 2rem;
    }
    .header-strip h1 {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        margin: 0 0 0.3rem;
        color: #f5f0e8;
    }
    .header-strip p {
        margin: 0;
        opacity: 0.7;
        font-size: 0.9rem;
    }

    /* Streamlit input label tweak */
    label { font-weight: 600 !important; color: #737270 !important; }

    /* Button */
    .stButton > button {
        background: #1a1a2e;
        color: #f5f0e8;
        border: none;
        border-radius: 8px;
        padding: 0.55rem 1.8rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        transition: opacity 0.15s;
        width: 100%;
    }
    .stButton > button:hover { opacity: 0.85; }

    /* Divider */
    hr { border-color: #e0d8cc; }

    /* Hide Streamlit branding */
    #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="header-strip">
        <h1>📝 Midterm Feedback</h1>
        <p>Introduction to Python for Global Affairs &nbsp;·&nbsp; Spring 2026</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(":color[Enter your details below to retrieve your personalised feedback.]{foreground='#737270'}")

with st.form("login_form"):
    name_input = st.text_input("Your first name", placeholder="e.g. Alice")
    word_input = st.text_input(
        "Second word of your Jupyter notebook - # is a word here!",
        placeholder="Open your .ipynb and check the second word - including #",
    )
    submitted = st.form_submit_button("View my feedback →")

if submitted:
    name = name_input.strip()

    # ── 1. Name check ────────────────────────────────────────────────────────
    if name not in submission_code:
        st.error("⚠️  That first name wasn't found. Check the spelling and try again.")
        st.stop()

    # ── 2. Notebook verification ─────────────────────────────────────────────
    nb_path = submission_code[name]
    second_word = _extract_second_word(nb_path)

    if second_word is None:
        st.error(
            f"⚠️  Could not read the notebook at `{nb_path}`. "
            "Please contact your TA."
        )
        st.stop()

    if _normalise(word_input) != _normalise(second_word):
        st.error(
            "❌  The word you entered doesn't match your notebook. "
            "Open your .ipynb file and copy the second word you see - don't forget that # counts as a word!"
        )
        st.stop()

    # ── 3. Show feedback ─────────────────────────────────────────────────────
    feedback = fb_ma.get(name, "No feedback entry found for your name. Contact your TA.")

    ai_feedback_all = _load_ai_feedback(AI_FEEDBACK_CSV)
    ai_feedback_raw = ai_feedback_all.get(name, "")
    ai_feedback = ai_feedback_raw if ai_feedback_raw else "AI feedback coming soon!"

    st.success(f"✅  Identity confirmed — here is your feedback, {name}!")

    col_ma, col_ai = st.columns(2)

    with col_ma:
        st.markdown(
            '<div class="card-label"><span>📋 Matthew\'s feedback</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="feedback-card">{_md_to_html(feedback)}</div>',
            unsafe_allow_html=True,
        )

    with col_ai:
        st.markdown(
            '<div class="card-label ai-label"><span>✨ Gemini Flash 2.5\'s feedback</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="feedback-card">{_md_to_html(ai_feedback)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Questions about your grade? Reach out during office hours.")