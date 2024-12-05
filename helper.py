from flask import Flask, request, jsonify, render_template, url_for
import openai
import os


openai.api_key = os.getenv("OPENAI_API_KEY")

#static: for CSS file
app = Flask(__name__, static_folder='static')


#Renders the 'main.html' template when the root URL is accessed.
@app.route('/')
def index():
    return render_template('main.html')


@app.route('/generate-care-plan', methods=['POST']) #Fetch route
def generate_care_plan():
    data = request.get_json() #retrieves JSON data from the POST request

    pet_info = data.get('petInfo', '') #Extracts 'petInfo' from the recieved data
    feeding_checked = data.get('feeding', False)
    grooming_checked = data.get('grooming', False)
    training_checked = data.get('training', False)

    if not pet_info:
        return jsonify({"error": "Pet information is required"}), 400


    #Calls the OpenAI API to generate a response using the GPT-3 model.
    try:
        #Creates a prompt for OpenAI to produce a response
        if feeding_checked:
            prompt=f"""
            Assume I am a person who loves my pet very much and would like it to be well taken care of. Based on the following pet information: '{pet_info}', please create a detailed weekly feeding schedule for my pet."""
        elif grooming_checked:
            prompt = f"""
            Assume I am a person who loves my pet very much and would like it to be well taken care of. Based on the following pet information: '{pet_info}', please create a detailed weekly grooming schedule for my pet."""
        
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

        #prints response
        print("Response:", response) 
        #extracts the generated plan from the API response and returns it as a Json response
        generated_plan = response['choices'][0]['message']['content'].strip()

        
        return jsonify({"generatedPlan": generated_plan})

    except Exception as e:
        print(f"Error: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response}")  
        return jsonify({"error": "Error generating care plan."}), 500

#Runs the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
