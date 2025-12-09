# Earthquake Prediction Project

A machine learning project that predicts earthquake magnitudes using seismic and geographic features. This project demonstrates data cleaning, exploratory data analysis, ML model training, and interactive visualization.

## Project Overview

This project follows a complete data science pipeline:
1. **Data Loading & Cleaning**: Load earthquake data from CSV, remove nulls, filter non-earthquake events
2. **Data Exploration**: Identify patterns in magnitude, depth, and location
3. **Feature Engineering**: Extract region information from place names
4. **Model Training**: Build a Random Forest regressor to predict earthquake magnitude
5. **Visualization**: Interactive maps and plots using Streamlit

## Project Structure

```
Earthquake_Prediction_Project/
├── data/
│   ├── all_earthquakes_by_month.csv    # Raw earthquake data
│   ├── earthquakes.db                   # SQLite database (generated)
│   └── model.pkl                        # Trained ML model (generated)
├── notebooks/
│   ├── data_sandbox.ipynb               # Data loading, cleaning, exploration
│   ├── ml_sandbox.ipynb                 # Model training and evaluation
│   └── data_visualization_sandbox.ipynb # Visualization experiments
├── app.py                               # Streamlit web application
├── load_data.py                         # Dataset cleaning and database creation script
├── train_model.py                       # Standalone model training script
├── requirements.txt                     # Python dependencies
├── .gitignore                           # Git configuration
└── README.md                            # This file
```

## Setup Instructions

Before any code is run, it is important to note that the scripts should be run from the
project root.

### 1. Create Virtual Environment

py -m venv .venv .\.venv\Scripts\Activate.ps1

### 2. Install Dependencies

pip install -r requirements.txt


**Key dependencies:**
- `pandas`: Data manipulation and analysis
- `scikit-learn`: Machine learning models and utilities
- `sqlite3`: Database management (built-in)
- `streamlit`: Interactive web app framework
- `matplotlib`, `seaborn`: Data visualization
- `pickle`: Model serialization (built-in)

## Running the Project

### Jupyter Notebooks

I did all my work in the juypter notebooks and then put the neccessary, clean code into
their respective .py files. I would look through the juypter notebooks first to go through all my work and then run the .py files to create the database, ML model, and streamlit dashboard.

Notebooks created and worked on in order:
1. **`notebooks/data_sandbox.ipynb`** - Clean data and create SQLite database
2. **`notebooks/ml_sandbox.ipynb`** - Train ML model and evaluate performance
3. **`notebooks/data_visualization_sandbox.ipynb`** - Experiment with visualizations


### Dataset Cleaning and Database Creation Script

To create the database (earthquakes.db) file, run:

"py load_data.py"

This script will:
- Load the messy CSV file to a dataframe
- Clean the dataframe
- Create the database
- Upload the dataframe to the database
- Save the .db file to 'data/earthquakes.db'


### Standalone Training Script

To create the ML model, run:

"py train_model.py"

This script will:
- Load cleaned earthquake data from the SQLite database
- Train a RandomForestRegressor on latitude, longitude, and depth (features)
- Save the trained model to 'data/model.pkl'


### Streamlit Web App

To launch the interactive visualization app, run:

"streamlit run app.py"

- NOTE: When you run app.py and it opens in a browser window, you might need to wait ~10 seconds for it to load
if this is the first time.

The app will open in your browser and show:
- Interactive maps of earthquake locations
- Various charts on different variables such as magnitude and depth
- Magnitude predictions from the ML model using user input


## Data Details

### Source
- **File**: `data/all_earthquakes_by_month.csv`
- **File Source**: 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php'
- **Records**: ~7,000 earthquake events
- **Time Period**: Month of seismic activity

### Columns Used
- `time`: Event timestamp
- `latitude`: Geographic latitude
- `longitude`: Geographic longitude
- `depth`: Event depth (km)
- `magnitude`: Event magnitude (target variable)
- `magType`: Magnitude type (nanojoules, moment, etc.)
- `place`: Location description
- `type`: Event classification (earthquake)
- `region`: Extracted from place column (e.g., "California", "Alaska")

### Data Processing
- **Dropped columns**: High-NA features (nst, gap, dmin, rms) and redundant fields
- **Filtered rows**: Removed non-earthquake events (quarry blasts, explosions, sonic booms)
- **Feature creation**: Extracted region name from place description using string splitting

## Model Details

### Training Data
- **Features**: latitude, longitude, depth
- **Target**: magnitude
- **Train/Test Split**: 80/20
- **Random Seed**: 42 (for reproducibility)

### Model Architecture
- **Algorithm**: Random Forest Regressor
- **Parameters**: 100 decision trees
- **Evaluation Metric**: Mean Absolute Error (MAE)

### Performance
- **Baseline MAE** (predicting mean magnitude): 0.968
- **Model MAE**: 0.369
- **Improvement**: ~60% reduction in error


## Technical Notes

## Git Configuration

The project includes a `.gitignore` to:
- **Track**: Jupyter notebooks (`*.ipynb`) for version control
- **Exclude**: Virtual environment (`.venv/`), cached files, and optionally large data files

This ensures the repository stays clean while preserving analysis work.


## Troubleshooting

### Issue: "Unable to open database file"
**Solution**: Ensure you're running from the project root directory, or use script-relative paths as in `train_model.py`

### Issue: Module not found errors
**Solution**: Confirm virtual environment is activated and dependencies are installed:
```powershell
pip install -r requirements.txt
```

### Issue: Relative paths fail in notebooks
**Solution**: Make sure notebooks are run from the project root or adjust relative paths accordingly