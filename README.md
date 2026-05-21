# Simulate Your Data: Markov Chain Dashboard

A web dashboard for uploading clickstream CSV data, building a Markov transition model, and visualizing both real and simulated user navigation paths.

This project combines a Flask backend with a Retool frontend. Users can upload clickstream data, preview the dataset, run Markov chain simulations, and compare real user path flows with simulated path flows.

## Features

- Upload clickstream CSV files
- Preview uploaded data in a table
- Clean and process clickstream records
- Build transition probability matrices from user navigation data
- Run Markov chain simulations
- Visualize page visit counts
- Visualize transition probabilities
- Compare:
  - Real User Navigation Path Flow
  - Simulated User Navigation Path Flow
- Configure fixed initial page and fixed terminal page
- Adjust visible path depth using a step range slider
- Reuse previously uploaded files

## Tech Stack

### Frontend

- Retool
- Plotly charts
- Retool components:
  - File Dropzone
  - Select
  - Checkbox
  - Slider
  - Table
  - Plotly JSON Chart

### Backend

- Python
- Flask
- Flask-CORS
- SQLAlchemy
- Pandas
- Markov Chain simulation logic

### Development Tools

- ngrok for exposing local Flask API to Retool
- GitHub for version control

## Project Structure

```text
Markov-Dashboard/
│
├── app.py
├── simulation.py
├── step_flow.py
├── build_matrix.py
├── clean_data.py
├── import_data.py
├── config.py
├── fake_data.py
├── requirements.txt
├── README.md
│
├── uploads/
│   └── uploaded CSV files
│
└── sample_data/
    └── clickstream.csv
