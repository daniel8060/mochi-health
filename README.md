

# 🧠 Mood of the Queue – Mochi Health Take-Home

This is a simple internal tool designed to help support agents log and visualize the *emotional tone* of incoming patient support tickets—whether they're frustrating, joyful, or anything in between.

Built as part of the Data Scientist, Operations – SF take-home prompt for Mochi Health.

An important note -- once I deployed to the server, I noticed it was in UTC 0 time, so if you are on the West Coast like me, you might be confused about inputting data but not seeing the chart update. This is because we're 7 hours behind the server time so anything entered after 1700 will appear in _tomorrow's_ data. 

---

## 🚀 Features

- **Mood Logging:**  
  Agents can log the mood of the queue using a quick emoji selector and an optional text note.

- **Google Sheets Integration:**  
  All entries are written to a Google Sheet with a timestamp for lightweight persistence.

- **Mood Visualization:**  
  Displays a bar chart of mood counts by day using Plotly.
---

## 📸 Screenshots

| Mood Logging Form | Mood Trend Chart |
|-------------------|------------------|
| ![Form Screenshot](image.png) | ![Chart Screenshot](image-1.png)|

_(Replace with actual screenshots or Loom if available)_

---

## 🧱 Stack

- **Language:** Python  
- **Frontend:** Streamlit  
- **Data Storage:** Google Sheets (via `streamlit_gsheets`)  
- **Charting:** Plotly  
- **Dependency Management:** Poetry

---

## 🛠️ Running the App Locally

1. **Install Poetry (if needed):**

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install project dependencies:**

   ```bash
   poetry install
   ```

3. **Set up your Google Sheets credentials:**

   Add your service account JSON to `.streamlit/secrets.toml` as follows:

   ```toml
   [connections.gsheets]
   type = "service_account"
   project_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\\n..."
   client_email = "your-svc-account@project.iam.gserviceaccount.com"
   spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
   worksheet = "0"
   ```

4. **Run the app:**

   ```bash
   poetry run streamlit run mood.py
   ```

---

## 📦 Deliverables

- ✅ Logging form and bar chart, both fully functional
- ✅ Uses Google Sheets as a backend
- ✅ Clean, modular Python code with docstrings
- ✅ Bar Chart updates every 5 seconds

---

## ✨ If Given More Time

If this were an internal Friday hack, here’s what I would prioritize next:

1. **Migrate to a Database (Highest Priority):**  
   Evaluate switching to a Postgres or lightweight hosted DB for improved query performance, concurrency control, and reliability over Sheets.

2. **Efficient Appends via Google Sheets API:**  
   Refactor `append_data()` using `requests` and the Sheets API `AppendCellsRequest` to avoid rewriting the full dataset.

3. **Multi-Page Streamlit App:**  
   Separate mood input and chart views, and optionally add admin tooling to explore longer-term trends.

4. **Collaborate with SMEs:**  
   Consult support agents to refine the emoji/mood list to better match their day-to-day ticket experiences.

5. **Align on a time standard:**
    Ensure the data entry time is properly recorded according to the appropriate timezone. 

---
