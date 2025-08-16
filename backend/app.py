from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import difflib
import openai

# Load environment variables
load_dotenv()

# Configure OpenRouter (GPT-3.5)
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# Flask app setup
app = Flask(__name__)
CORS(app)

# Helper: Search relevant chunk from internal doc
def get_relevant_doc_chunk(user_question):
    try:
        with open("company_policies.txt", "r") as f:
            doc_text = f.read()
    except FileNotFoundError:
        return "⚠️ Internal document file not found."

    chunks = doc_text.split("Title:")
    best_score = 0
    best_chunk = None

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        title_line = chunk.split("\n")[0].strip()
        similarity = difflib.SequenceMatcher(None, user_question.lower(), title_line.lower()).ratio()
        if similarity > best_score:
            best_score = similarity
            best_chunk = chunk

    if best_chunk and best_score > 0.3:
        return "Title: " + best_chunk.strip()  # strip extra space/newlines
    return "No relevant section found in internal docs."


# Main API route
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_question = data.get("question")

    if not user_question:
        return jsonify({"answer": "Please enter a valid question."})

    context = get_relevant_doc_chunk(user_question)

    if not context or context.startswith("⚠️") or context.startswith("No relevant"):
        return jsonify({
            "answer": (
                "🤖 Hmm, I couldn’t find anything related to that in our internal documentation.\n"
                "You might want to check with your team lead or refer to the HR portal!"
            )
        })

    # Clean, prompt-friendly formatting (no leading/trailing line breaks)
    prompt = (
        f"You are DocuBuddy, an internal AI assistant that helps employees understand "
        f"company policies and internal documentation.\n\n"
        f"Respond clearly and professionally using the internal documentation below.\n"
        f"Avoid email-like greetings or signatures. Do not include 'Dear Employee' or 'Regards'.\n"
        f"Only answer what is asked, based strictly on the documentation provided.\n\n"
        f"---\n"
        f"Internal Documentation:\n{context}\n"
        f"---\n"
        f"Employee's Question: {user_question}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful internal documentation assistant named DocuBuddy."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response["choices"][0]["message"]["content"].strip()

        # Debug log to terminal
        print("----- RAW ANSWER -----")
        print(answer)
        print("----------------------")

        # Extra safety: common fixes
        common_starts = {
            "mployees ": "Employees ",
            "efund": "Refund",
            "olicy": "Policy",
            "ur ": "Your ",
            "he ": "The ",
        }
        for wrong, fixed in common_starts.items():
            if answer.startswith(wrong):
                answer = fixed + answer[len(wrong):]

        # Capitalize first letter if still lowercase
        if answer and answer[0].islower():
            answer = answer[0].upper() + answer[1:]

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})


# Run server
if __name__ == "__main__":
    print("OpenRouter API Key Loaded:", bool(os.getenv("OPENROUTER_API_KEY")))
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import difflib
import openai

# Load environment variables
load_dotenv()

# Configure OpenRouter API
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

app = Flask(__name__)
CORS(app)

def get_relevant_doc_chunk(user_question):
    try:
        with open("company_policies.txt", "r", encoding="utf-8") as f:
            doc_text = f.read()
    except FileNotFoundError:
        return None

    chunks = doc_text.split("Title:")
    best_score = 0
    best_chunk = None

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        title_line = chunk.split("\n")[0].strip()
        similarity = difflib.SequenceMatcher(None, user_question.lower(), title_line.lower()).ratio()
        if similarity > best_score:
            best_score = similarity
            best_chunk = chunk

    return "Title: " + best_chunk.strip() if best_score > 0.3 else None

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_question = data.get("question", "").strip()

    if not user_question:
        return jsonify({"answer": "Please enter a valid question."})

    context = get_relevant_doc_chunk(user_question)

    if not context:
        return jsonify({
            "answer": (
                "🤖 Hmm, I couldn’t find anything related to that in our internal documentation.\n"
                "You might want to check with your team lead or refer to the HR portal!"
            )
        })

    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are DocuBuddy, an internal company assistant. "
                        "Your task is to answer employee questions using the provided documentation. "
                        "Respond clearly and professionally. Do not include greetings like 'Dear employee', "
                        "'Hello', or signatures like 'Regards'."
                    )
                },
                {
                    "role": "system",
                    "content": f"Internal Documentation:\n{context}"
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ]
        )

        raw_answer = response["choices"][0]["message"]["content"].strip()

        # Clean any odd prefix from the model
        if raw_answer.lower().startswith("ur "):
            raw_answer = "Your " + raw_answer[3:]
        if raw_answer.lower().startswith("mployees "):
            raw_answer = "Employees " + raw_answer[8:]
        if raw_answer.lower().startswith("ear employee"):
            raw_answer = raw_answer.split("\n\n", 1)[-1].strip()

        return jsonify({"answer": raw_answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

if __name__ == "__main__":
    print("OpenRouter API Key Loaded:", bool(os.getenv("OPENROUTER_API_KEY")))
    app.run(debug=True)
