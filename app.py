from flask import Flask, jsonify, request
from import_data import import_data
from clean_data import clean_data
from build_matrix import build_matrix
from simulation import MarkovChain
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

results = {}
@app.route('/upload', methods=['POST'])
def upload_file():
    global results
    file = request.files['file']
    import_data(file)
    clean_data()
    state_list, probability_dict = build_matrix()
    mc = MarkovChain(state_list, probability_dict)
    visit_counts = {state: 0 for state in state_list}

    path = [mc.current_state]

    for _ in range(1000):
        next_state = mc.transfer_state()
        mc.current_state = next_state
        visit_counts[next_state] = visit_counts.get(next_state, 0) + 1
        path.append(next_state)
        if next_state not in mc.probability_dict:
            break

    results = {
        'probability_dict': probability_dict,
        'visit_counts': visit_counts,
        'path': path }

    return jsonify({'message': 'completed'})


@app.route('/results', methods=['GET'])
def get_results():
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, port=8080)