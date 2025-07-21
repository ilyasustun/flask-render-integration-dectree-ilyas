from flask import Flask, request, render_template
from pickle import load
import os
import traceback

app = Flask(__name__)

# Add error logging
app.debug = True  # Enable debug mode

try:
    model = load(open("/workspaces/flask-render-integration-dectree-ilyas/models/decision_tree_classifier_default_42.sav", "rb"))
except Exception as e:
    print(f"Error loading model: {str(e)}")
    traceback.print_exc()
    raise

class_dict = {
    "0": "Iris setosa",
    "1": "Iris versicolor",
    "2": "Iris virginica"
}

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            # Add debug prints
            print("Form data:", request.form)
            
            val1 = float(request.form.get("val1", 0))
            val2 = float(request.form.get("val2", 0))
            val3 = float(request.form.get("val3", 0))
            val4 = float(request.form.get("val4", 0))
            
            print(f"Values: {val1}, {val2}, {val3}, {val4}")
            
            data = [[val1, val2, val3, val4]]
            print("Input data:", data)
            
            prediction = str(model.predict(data)[0])
            print("Prediction:", prediction)
            
            pred_class = class_dict[prediction]
            print("Predicted class:", pred_class)
        else:
            pred_class = None
        
        return render_template("index.html", prediction=pred_class)
    
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        traceback.print_exc()
        return f"An error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)