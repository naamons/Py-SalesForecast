
# Sales Forecasting Application

This application allows users to upload sales data in CSV format and forecasts future sales for selected products using an ARIMA model.

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

Execute the following command in the terminal:
```
streamlit run sales_forecast_app.py
```
The application will start, and your web browser will open a new tab pointing to the local URL where the app is running.

## Usage

1. Use the file uploader to select and upload your sales data CSV file.
2. Select a product from the dropdown menu to forecast sales.
3. Click the "Forecast Sales" button to view the sales forecasts and corresponding visualizations.

## License

This project is licensed under the MIT License.
