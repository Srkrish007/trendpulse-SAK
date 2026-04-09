An end‑to‑end Python pipeline that fetches trending HackerNews stories, cleans the data, performs analysis with Pandas/NumPy, and visualises trends using Matplotlib.


This project implements a 4‑part pipeline:

- **Task 1**: Fetch trending HackerNews stories as JSON and categorise by keywords (technology, worldnews, sports, science, entertainment).  
- **Task 2**: Clean the JSON into a tidy CSV, handling duplicates, missing values, low scores, and data types.  
- **Task 3**: Analyse scores and comments using NumPy and Pandas, adding engagement and popularity metrics.  
- **Task 4**: Visualise the data with 3 charts and a dashboard, saved as PNG files.

**Repository Structure**

```text
trendpulse-SAK/
├── task1_data_collection.py     # Fetch and categorise JSON stories
├── task2_data_cleaning.py       # Clean JSON → CSV
├── task3_analysis.py            # NumPy/Pandas analysis with new columns
├── task4_visualise.py           # Matplotlib charts and dashboard
├── data/
│   ├── trends_YYYYMMDD.json     # Output from Task 1
│   ├── trends_clean.csv         # Output from Task 2
│   └── trends_analysed.csv      # Output from Task 3
└── outputs/
    ├── chart1_top_stories.png   # Top 10 stories by score
    ├── chart2_categories.png    # Stories per category
    ├── chart3_scatter.png       # Score vs comments
    └── dashboard.png            # TrendPulse Dashboard (bonus)
```



- Python 3  
- `requests`: API calls to HackerNews  
- `pandas` and `numpy`: data cleaning, analysis, and statistics  
- `matplotlib`: visualisation and dashboard  
- Git/GitHub: version control and collaboration



1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/trendpulse-SAK.git
   cd trendpulse-SAK
   ```

2. Install dependencies (using system package managers):

   ```bash
   sudo apt install python3-requests python3-pandas python3-matplotlib  # Ubuntu
   ```

3. Run each task in order:

   ```bash
   python3 task1_data_collection.py
   python3 task2_data_cleaning.py
   python3 task3_analysis.py
   python3 task4_visualise.py
   ```

4. Open the `outputs/` folder to view the generated charts and `dashboard.png`.


- `chart1_top_stories.png` – Top 10 stories by score (horizontal bar chart).  
- `chart2_categories.png` – Number of stories per category (bar chart).  
- `chart3_scatter.png` – Score vs. number of comments, coloured by `is_popular`.  
- `dashboard.png` – Combined `TrendPulse Dashboard` with all three charts.


This project is for educational purposes and is not affiliated with HackerNews.