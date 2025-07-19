# digital-twin-grid
This public project simulates parts of the Belgian power grid using Python and open data. Inspired by the work of Elia Group, the goal is to build a lightweight digital twin that models power flows under real-world scenarios.

## Goals
- Load and simulate Belgian grid behavior using real data
- Explore congestion, RES oversupply, and high-load events
- Use Python-based grid modeling (PyPSA / pandapower)

## Data Sources
- Elia Open Data Portal: [https://www.elia.be/en/grid-data](https://www.elia.be/en/grid-data)
- ENTSO-E Transparency Platform
- GridKit (OpenStreetMap grid topology data)

## Tools Used
- Python, pandas, numpy, matplotlib, plotly
- PyPSA or pandapower
- SQLite or PostgreSQL (for data storage)
- Streamlit or Dash (for optional UI)

## Structure
- `data/`: raw and cleaned datasets
- `notebooks/`: Jupyter notebooks for exploration and simulation
- `models/`: grid modeling code
- `dashboard/`: optional web dashboard

## Scenarios Simulated
- Peak renewable production day
- Cold winter high load
- Local congestion & outage simulation

## Status
Project under development — contributions or feedback welcome.

## License
MIT
