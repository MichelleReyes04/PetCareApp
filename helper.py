from flask import Flask, request, jsonify, render_template, url_for
import openai
import os

# Retrieve the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the Flask application
app = Flask(__name__, static_folder='static')

# Routes for rendering templates
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/main')
def index():
    return render_template('main.html')

@app.route('/care_cost_support')
def care_cost_support():
    return render_template('care_cost_support.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Route for generating financial plans
@app.route('/generate-fin-plan', methods=['POST'])
def generate_fin_plan():
    data = request.get_json()

    pet_fin_info = data.get('petFin', '')
    zip_c = data.get('zipcode', '')

    if not pet_fin_info:
        return jsonify({"error": "Pet information is required"}), 400

    try:
        prompt = f"""
        I have a user who needs financial aid and support in their local area. 
        They have provided the following relevant information. 
        Given this zip code: {zip_c} and based on their pet's information: {pet_fin_info}, 
        please generate a list of local financial aid and support options that cater to the user's pet needs and their zip code.
        """

        response2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Extracts the generated plan from the API response and returns it as a JSON response
        generatedplantwo = response2['choices'][0]['message']['content'].strip()

        return jsonify({"generatedplantwo": generatedplantwo})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Error generating care plan."}), 500

# Route for generating care plans
@app.route('/generate-care-plan', methods=['POST'])
def generate_care_plan():
    data = request.get_json() # Retrieves JSON data from the POST request

    pet_info = data.get('petInfo', '') # Extracts 'petInfo' from the received data
    feeding_checked = data.get('feeding', False)
    grooming_checked = data.get('grooming', False)
    training_checked = data.get('training', False)

    if not pet_info:
        return jsonify({"error": "Pet information is required"}), 400

    try:
        # Creates a prompt for OpenAI to produce a response
        if feeding_checked:
            prompt = f"""
            Assume I am a person who loves my pet very much and would like it to be well taken care of. Based on the following pet information: '{pet_info}', please create a detailed weekly feeding schedule for my pet.
            """
        elif grooming_checked:
            prompt = f"""
            Assume I am a person who loves my pet very much and would like it to be well taken care of. Based on the following pet information: '{pet_info}', please create a detailed weekly grooming schedule for my pet.
            """
        elif training_checked:
            prompt = f"""
            Assume I am a person who loves my pet very much and would like it to be well taken care of. Based on the following pet information: '{pet_info}', please create a detailed weekly training schedule for my pet.
            """
        else:
            prompt = f"""
            Based on the following pet information: '{pet_info}', create a detailed pet care plan for the next week.
            The plan should include feeding, exercise, grooming, and special care instructions based on the pet's condition.
            """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Extracts the generated plan from the API response and returns it as a JSON response
        generated_plan = response['choices'][0]['message']['content'].strip()

        return jsonify({"generatedPlan": generated_plan})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Error generating care plan."}), 500

# Runs the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
