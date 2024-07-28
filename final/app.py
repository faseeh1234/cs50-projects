from flask import Flask, render_template, request
import matplotlib.pyplot as plt

app = Flask(graphs.py)

@app.route('/')
def index():
    return render_template('.html')

@app.route('/generate', methods=['POST'])
def generate():
    exercise = request.form['exercise']
    weight = float(request.form['weight'])
    reps = int(request.form['reps'])

    # Use the received data to generate the graph (similar to your previous code)
    plt.figure(figsize=(8, 6))
    # Generate the graph using the provided data...

    # Save the plot as an image
    plt.savefig("temp.png")
