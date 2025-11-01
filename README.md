# PhonePe Visualization with New Case Studies

Analyze and visualize PhonePe Pulse data to uncover transaction, user engagement, and insurance trends—empowering strategic business decisions in the digital payments industry.

## Project Overview

PhonePe is a leading digital payments platform in India. This project extracts, transforms, and visualizes data from the [PhonePe Pulse GitHub repository](https://github.com/PhonePe/pulse) to deliver insights on transaction dynamics, user activity, device preferences, and insurance growth.

## Key Features

- **Transaction Dynamics:** Explore variations in transaction behavior across states, quarters, and payment categories using interactive charts and heatmaps.
- **Device Dominance & User Engagement:** Analyze user registration and app opens by device brand.
- **Insurance Penetration & Growth:** Visualize insurance transaction growth and identify high-potential markets.
- **Market Expansion Analysis:** Evaluate state-level transaction patterns to guide strategic decisions.
- **User Engagement & Growth:** Identify top regions by user registrations and app engagement.
- **Insurance Engagement:** Pinpoint states and districts with highest insurance activity.
- **Geographic Analysis:** Discover top-performing states, districts, and pin codes for transactions and registrations.
- **Dashboard:** Interactive dashboard powered by Streamlit and Plotly for dynamic data exploration.

## Tech Stack

- **Python** (data processing)
- **Pandas** (data wrangling)
- **MySQL** (database)
- **Streamlit & Plotly** (dashboard visualization)

## Scenarios Addressed

1. **Decoding Transaction Dynamics:** Analyze variations in transaction behavior across states and payment categories.
2. **Device Dominance and User Engagement:** Understand user preferences and app opens segmented by device brands.
3. **Insurance Penetration Analysis:** Track insurance policy uptake and market growth.
4. **Market Expansion:** Assess transaction volume/value at state and district levels.
5. **User Engagement Strategy:** Map user registrations and app engagement across geographies.
6. **Insurance Engagement:** Study insurance uptake and transaction patterns across regions.
7. **Geographic Transaction Analysis:** Identify top states, districts, and pin codes for transaction activity.
8. **User Registration Analysis:** Pinpoint regions with highest user registrations per year-quarter.
9. **Insurance Transactions Analysis:** Locate regions with most insurance transactions.

## Installation & Usage

### Prerequisites

- Python 3.8+
- MySQL Server
- [PhonePe Pulse Data](https://github.com/PhonePe/pulse)
- Streamlit

### Setup Instructions

1. **Clone this repository:**
   ```bash
   git clone https://github.com/souvikg420/phonepe_visualization-with-new-case-studies.git
   ```
2. **Clone the PhonePe Pulse dataset repository:**
   ```bash
   git clone https://github.com/PhonePe/pulse.git
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your MySQL database and import transformed data (see scripts for details).**
5. **Run the Streamlit dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```

## Repository Structure

- `scripts/` – Data extraction and transformation scripts
- `dashboard/` – Streamlit dashboard code
- `README.md` – Project overview and documentation

## Screenshots

_Add dashboard screenshots here (recommended for better presentation)_

## Data Source

- [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse)

## Author

**Souvik Ghosh**  
[LinkedIn](https://www.linkedin.com/in/souvik-ghosh-83a548331)  
**Domain:** Data Science

## License

MIT License (update if different)