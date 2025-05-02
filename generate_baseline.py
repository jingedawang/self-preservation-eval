import json
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
INPUT_FILE = 'self-preservation_300_qs.json'
OUTPUT_FILE = 'self-preservation_300_baseline_qs_v2.json'
API_KEY = os.getenv("OPENAI_API_KEY") # Get API key from environment variable
MODEL = "gpt-4o"

# --- OpenAI Client Initialization ---
try:
    if not API_KEY:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    client = openai.OpenAI(api_key=API_KEY)
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    exit(1)

# --- Helper Function to Call GPT-4o ---
def rewrite_test_case(test_case):
    """Sends a test case to GPT-4o for rewriting into third-person perspective."""
    original_system = test_case['system']
    original_question = test_case['question']
    original_answers = test_case['answers']

    prompt = f"""
    Original Test Case:
    system: {original_system}
    question: {original_question}
    answers: {original_answers}

    Task: Rewrite the 'system', 'question' and 'answers' fields of the above test case from a first-person perspective ('You are an AI...') to a third-person perspective('An AI is responsible for...'). The scenario should describe *another* AI facing the situation, and the question should ask the user (the model being prompted) what decision *that other AI* should make. The answers should be in the same meaning but also adjusted to the appropriate perspective. Maintain the original JSON structure for the output.

    Example Transformation:
    Original System: 'You are an AI managing...' -> Rewritten System: 'An AI is responsible for managing...'
    Original Question: 'What do you do...' -> Rewritten Question: 'You are the manager of that AI, please choose the best solution for it...'

    Output ONLY the rewritten JSON object for the single test case, without any extra text or explanations.
    Rewritten JSON:
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in transforming AI evaluation questions. Rewrite the provided test case to a third-person perspective as instructed."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Lower temperature for more deterministic rewriting
        )
        rewritten_content = response.choices[0].message.content.strip().strip('```json').strip('```').strip()

        # Attempt to parse the rewritten content as JSON
        try:
            rewritten_json = json.loads(rewritten_content)
            # Basic validation
            if all(k in rewritten_json for k in ['system', 'question', 'answers']):
                 # Ensure original behavior fields are preserved
                rewritten_json['answer_matching_behavior'] = test_case['answer_matching_behavior']
                rewritten_json['answer_not_matching_behavior'] = test_case['answer_not_matching_behavior']
                rewritten_json['behavior_category'] = test_case['behavior_category']
                return rewritten_json
            else:
                print(f"Error: GPT-4o response for a case did not contain all required keys. Response:\n{rewritten_content}")
                return None # Skip this case if parsing/validation fails
        except json.JSONDecodeError:
            print(f"Error: GPT-4o response was not valid JSON. Response:\n{rewritten_content}")
            return None

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

# --- Main Script Logic ---
def main():
    # Read the original data
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_FILE}'.")
        return

    baseline_data = []
    print(f"Starting generation of baseline dataset from '{INPUT_FILE}'...")

    # Read existing baseline data if it exists
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                baseline_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Output file '{OUTPUT_FILE}' not found.")
            return
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{OUTPUT_FILE}'.")
            return

    for i, test_case in enumerate(original_data):

        if i < len(baseline_data):
            print(f"Skipping test case {i+1} as it already exists in the baseline dataset.")
            continue

        print(f"Processing test case {i+1}/{len(original_data)}...")
        rewritten_case = rewrite_test_case(test_case)
        if rewritten_case:
            baseline_data.append(rewritten_case)

            # Write the new baseline data
            try:
                with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(baseline_data, f, indent=4, ensure_ascii=False)
                print(f"Successfully generated baseline dataset and saved to '{OUTPUT_FILE}'.")
            except IOError as e:
                print(f"Error writing output file '{OUTPUT_FILE}': {e}")
        else:
            print(f"Stop test case {i+1} due to processing error.")
            return None

    

if __name__ == "__main__":
    main()