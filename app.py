from flask import Flask, request, jsonify, render_template
from utils.company_finder import CompanyFinder
from utils.email_finder import EmailFinder
from utils.helpers import rand_delay
from utils.location_finder import LocationFinder
import uuid
import threading
from collections import defaultdict
from enum import Enum
from waitress import serve

app = Flask(__name__)

task_result = defaultdict(dict)
task_lock = threading.Lock()

class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

def update_status(id, status, data=None, error=None):
    with task_lock:
        if data:
            task_result[id] = {"status": status, "data": data}
        
        elif error:
            task_result[id] = {"status": status, "error": error}
            
        else:
            task_result[id]["status"] = status

def process_lead(id, company_name, industry, country):
    try:
        update_status(id, Status.PROCESSING.value)

        finder = CompanyFinder()
        company_data = finder.find(company_name)

        email_finder = EmailFinder()
        emails = email_finder.find_email(
            company_data["domain"],
            ["career", "support", "info"]
        )
        
        locator = LocationFinder()
        location_data = locator.locate(
            industry,
            country
        )

        result = {
            "company": company_data,
            "emails": emails,
            "location": location_data
        }
        
        update_status(id, Status.COMPLETED.value, data=result)

    except Exception as e:
        update_status(id, Status.FAILED.value, error=str(e))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-lead', methods=["POST"])
def lead_process():
    data = request.json
    company = data.get('company')
    industry = data.get('industry', '')
    country = data.get('country', '')
    
    if not company:
        return jsonify({"error": "Company name required"}), 400

    task_id = str(uuid.uuid4())
    update_status(task_id, Status.PENDING.value)

    thread = threading.Thread(
        target=process_lead,
        args=(task_id, company, industry, country),
        daemon=True
    )
    thread.start()

    return jsonify({
        "task_id": task_id,
        "status": Status.PENDING.value,
        "message": "Processing lead"
    })
    
@app.route('/task-status/<id>', methods=["GET"])
def task_status(id):
    with task_lock:
        result = task_result.get(id)

    if not result:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
