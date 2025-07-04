# Caprae-Capital-Assignment

This Flask application serves as the powerful backend for the Caprae Lead Generation Enhancement Solution. It provides robust capabilities for identifying company information, discovering targeted departmental emails, and suggesting geographic expansion opportunities. Designed with scalability and ethical data collection in mind, this backend powers a more efficient and effective lead generation process.

## Table of Contents

- [Project Overview](project-overview)
- [Features](features)
- [Technical Highlights](technical-highlights)
- [Setup and Installation](setup-and-installation)
- [Prerequisites](prerequisites)
- [Installation Steps](installation-steps)
- [Usage](usage)
- [API Endpoints](api-endpoints)
- [License](license)

## Project Overview
The Caprae LeadGen Enhancement Solution aims to revolutionize lead generation by providing precise company data, targeted contact information, and global expansion insights. This handles the core logic for:

- **Direct Company Search**: Enabling exact name searches for companies.
- **Department Emails**: Discovering specific contacts (e.g., careers, support) to increase outreach efficiency.
- **Global Expansion**: Identifying opportunities in over 200+ countries using industry data.

It's built with a hybrid approach, focusing on both quality (deep company resolution, context-aware email discovery) and quantity (lightweight geographic expansion).

## Features

- **Hybrid Company Resolution**: Utilizes an API-first approach (e.g., Clearbit) with intelligent web scraping as a fallback for high accuracy in company data (domain, logo, industry).

- **Smart Email Discovery**: Scans company websites for specific departmental email patterns (careers@, support@, info@, sales@).

- **Geographic Expansion Intelligence**: Groups countries by economic zones and suggests new markets based on industry filtering.

- **Asynchronous Processing**: Handles lead processing in background threads to ensure a responsive user interface and scalability.

- **Ethical Scraping**: Implements rate limiting and respects robots.txt directives for responsible data collection.

- **Modular Design**: Independent components (CompanyFinder, EmailFinder, LocationFinder) for easy maintenance and extensibility.

- **Real-time Status Tracking**: Provides immediate feedback on the processing status of each lead generation task.

## Technical Highlights

- **Python & Flask**: The application is developed using Python with the Flask micro-framework for a lightweight and efficient web server.

- **Threading**: Python's threading module is used to run lead processing tasks asynchronously, preventing blocking of the main application thread.

- **UUID for Task Management**: Unique IDs are generated for each task, allowing clients to query the status of their requests.

- `defaultdict` **for Task Results**: Efficiently stores and manages the state and results of ongoing and completed tasks.

- **Enum for Status Management**: Clearly defines possible task statuses (PENDING, PROCESSING, COMPLETED, FAILED).

- `waitress` **(Production-ready WSGI server)**: Although app.run(debug=True) is used for development, waitress.serve is imported, indicating readiness for a production environment.

## Setup and Installation

### Prerequisites
Before you begin, ensure you have the following installed:

- Python 3.8+
- pip (Python package installer)

### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/Harshvardhan2164/Caprae-Capital-Assignment.git
cd Caprae-Capital-Assignment/
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
To run the Flask application in development mode:

```bash
python app.py
```

The application will typically run on `http://127.0.0.1:5000`.

## API Endpoints

1. `/` (Root Endpoint)
- Method: `GET`
- Description: Serves the main HTML page for the application.
- Response: Renders `index.html` (present in the templates directory).

2. `/process-lead`
- Method: `POST`
- Content-Type: `application/json`
- Description: Initiates an asynchronous lead generation task.
- Request Body Example:

```json
{
    "company": "Google",
    "industry": "Technology",
    "country": "United States"
}
```

- Response (200 OK):

```json
{
    "task_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "status": "pending",
    "message": "Processing lead"
}
```

- Error Response (400 Bad Request):

```json
{
    "error": "Company name required"
}
```

3. `/task-status/<id>`
- Method: `GET`
- Description: Retrieves the current status and results of a specific lead processing task.
- Response (200 OK - Pending/Processing):

```json
{
    "status": "processing"
}
```

- Response (200 OK - Completed):

```json
{
    "status": "completed",
    "data": {
        "company": {
            "name": "Google",
            "domain": "google.com",
            "logo": "https://example.com/google_logo.png",
            "industry": "Internet Services"
        },
        "emails": {
            "career": ["careers@google.com"],
            "support": ["support@google.com"],
            "info": ["info@google.com"]
        },
        "location": {
            "country_group": "North America",
            "suggested_countries": ["Canada", "Mexico"]
        }
    }
}
```

- Response (200 OK - Failed):

```json
{
    "status": "failed",
    "error": "Detailed error message here."
}
```

- Error Response (404 Not Found):

```json
{
    "error": "Task not found"
}
```

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.