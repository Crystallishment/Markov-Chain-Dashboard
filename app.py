import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request
from import_data import import_data
from clean_data import clean_data
from build_matrix import build_matrix
from simulation import MarkovChain
from step_flow import build_step_flow_from_csv
from flask_cors import CORS
from step_flow import build_step_flow_from_simulation
import pandas as pd

def run_simulation(simulation_count, start_page=None, exit_page=None):
    global state_list_global, probability_dict_global

    mc = MarkovChain(
        state_list_global,
        probability_dict_global,
        initial_state=start_page,
        terminal_state=exit_page
    )

    visit_counts = {state: 0 for state in state_list_global}
    path = [mc.current_state]
    visit_counts[mc.current_state] = visit_counts.get(mc.current_state, 0) + 1

    for _ in range(simulation_count):
        next_state = mc.transfer_state()

        if next_state is None:
            break

        path.append(next_state)
        visit_counts[next_state] = visit_counts.get(next_state, 0) + 1
        mc.current_state = next_state

    return {
        "success": True,
        "simulation_count": simulation_count,
        "start_page": start_page,
        "exit_page": exit_page,
        "probability_dict": probability_dict_global,
        "visit_counts": visit_counts,
        "path": path
    }

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

latest_uploaded_file = None
app = Flask(__name__)
CORS(app)

results = {}
state_list_global = []
probability_dict_global = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    global results, state_list_global, probability_dict_global
    global latest_uploaded_file

    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file received'
            }), 400

        file = request.files['file']

        if file.filename == "":
            return jsonify({
                'success': False,
                'error': 'No selected file'
            }), 400

        if not file.filename.lower().endswith(".csv"):
            return jsonify({
                'success': False,
                'error': 'Only CSV files are allowed'
            }), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # 保存一份给 data preview 用
        file.save(file_path)
        latest_uploaded_file = file_path

        # 关键：把文件指针重置回开头，否则 import_data(file) 会读到空内容
        file.seek(0)

        # 继续原来的清洗和模拟流程
        import_data(file)
        clean_data()

        state_list, probability_dict = build_matrix()

        state_list_global = state_list
        probability_dict_global = probability_dict

        results = run_simulation(1000)

        return jsonify({
            'success': True,
            'message': 'completed',
            'filename': filename,
            'simulation_count': 1000,
            'num_states': len(state_list_global)
        })

    except Exception as e:
        print("ERROR in /upload:", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/simulate', methods=['POST'])
def simulate():
    global results

    try:
        if not state_list_global or not probability_dict_global:
            return jsonify({
                'success': False,
                'error': 'No uploaded data found. Please upload a CSV file first.'
            }), 400

        data = request.get_json(silent=True) or {}
        simulation_count = int(data.get("simulation_count", 1000))

        results = run_simulation(simulation_count)

        return jsonify({
            'success': True,
            'message': 'simulation completed',
            'simulation_count': simulation_count
        })

    except Exception as e:
        print("ERROR in /simulate:", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/results', methods=['GET'])
def get_results():
    global results

    if not results:
        return jsonify({
            'success': False,
            'error': 'No results available yet'
        }), 400

    return jsonify(results)

@app.route('/data-preview', methods=['GET'])
def data_preview():
    global latest_uploaded_file

    if not latest_uploaded_file:
        return jsonify({
            "success": False,
            "error": "No uploaded file found"
        }), 400

    df = pd.read_csv(latest_uploaded_file)

    df = df.astype(object).where(pd.notnull(df), None)

    return jsonify({
        "success": True,
        "columns": list(df.columns),
        "rows": df.head(100).to_dict(orient="records"),
        "total_rows": len(df)
    })

@app.route('/files', methods=['GET'])
def list_uploaded_files():
    files = []

    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.lower().endswith(".csv"):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            files.append({
                "label": filename,
                "value": filename,
                "path": file_path
            })

    return jsonify({
        "success": True,
        "files": files
    })

def normalize_optional_arg(value):
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()
        if value == "" or value.lower() in ["null", "undefined", "none"]:
            return None

    return value

@app.route('/real-step-flow', methods=['GET'])
def real_step_flow():
    global latest_uploaded_file

    if not latest_uploaded_file:
        return jsonify({
            "success": False,
            "error": "No uploaded file found"
        }), 400

    min_step = int(request.args.get("min_step", 1))
    max_steps = int(request.args.get("max_steps", 5))
    start_page = normalize_optional_arg(request.args.get("start_page"))
    exit_page = normalize_optional_arg(request.args.get("exit_page"))

    if min_step > max_steps:
        return jsonify({
            "success": False,
            "error": "min_step cannot be greater than max_steps"
        }), 400

    flow = build_step_flow_from_csv(
        latest_uploaded_file,
        min_step=min_step,
        max_steps=max_steps,
        start_page=start_page,
        exit_page=exit_page
    )

    return jsonify({
        "success": True,
        "source": "real_data",
        "min_step": min_step,
        "max_steps": max_steps,
        "start_page": start_page,
        "exit_page": exit_page,
        "step_flow": flow
    })

@app.route('/simulated-step-flow', methods=['GET'])
def simulated_step_flow():
    global state_list_global, probability_dict_global

    if not state_list_global or not probability_dict_global:
        return jsonify({
            "success": False,
            "error": "No uploaded data found. Please upload a CSV file first."
        }), 400

    min_step = int(request.args.get("min_step", 1))
    max_steps = int(request.args.get("max_steps", 5))
    num_sessions = int(request.args.get("num_sessions", 1000))

    start_page = normalize_optional_arg(request.args.get("start_page"))
    exit_page = normalize_optional_arg(request.args.get("exit_page"))

    flow = build_step_flow_from_simulation(
        state_list=state_list_global,
        probability_dict=probability_dict_global,
        num_sessions=num_sessions,
        min_step=min_step,
        max_steps=max_steps,
        start_page=start_page,
        exit_page=exit_page
    )

    return jsonify({
        "success": True,
        "source": "simulation",
        "min_step": min_step,
        "max_steps": max_steps,
        "num_sessions": num_sessions,
        "start_page": start_page,
        "exit_page": exit_page,
        "step_flow": flow
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)