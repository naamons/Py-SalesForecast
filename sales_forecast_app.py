import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Function to load and preprocess data
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    # Ensure 'day' is in datetime format and drop rows with NaN in 'variant_sku'
    data['day'] = pd.to_datetime(data['day'])
    data.dropna(subset=['variant_sku'], inplace=True)
    return data

def forecast_sales(data, periods=[3, 6, 12]):
    forecast_dict = {}
    # Check if the data is non-empty and has sufficient length
    if not data.empty and len(data) > 2:  # Adjusted to check data directly
        model = ARIMA(data, order=(1,1,1))
        model_fit = model.fit()
        for period in periods:
            forecast = model_fit.forecast(steps=period)
            forecast_dates = pd.date_range(start=data.index[-1], periods=period + 1, freq='MS')[1:]
            forecast_dict[f'{period} Months'] = pd.DataFrame({'Forecast Date': forecast_dates, 'Forecasted Units': forecast})
    else:
        st.error("Insufficient data for forecasting. Please ensure the selected product has enough historical data.")
    return forecast_dict

# Streamlit web interface
st.title('Product Sales Forecasting Tool')

st.markdown("""
Make sure your CSV has the following headers:
- `product_title`
- `variant_sku`
- `day`
- `net_quantity`
- `gross_sales`
- `total_sales`
""")

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = load_data(uploaded_file)
    st.write("Data Uploaded Successfully!")

    selection_type = st.radio("Select by:", ('SKU', 'Product Title'))
    
    if selection_type == 'SKU':
        # SKU selection
        sku_list = data['variant_sku'].unique()
        selected_sku = st.selectbox('Select a SKU', sku_list)
        selected_data = data[data['variant_sku'] == selected_sku]
    else:
        # Product title selection
        product_list = data['product_title'].unique()
        selected_product = st.selectbox('Select a Product', product_list)
        selected_data = data[data['product_title'] == selected_product]

    if st.button('Analyze and Forecast Sales'):
        # Set 'day' as the DataFrame index and aggregate sales by month
        selected_data.set_index('day', inplace=True)
        monthly_sales = selected_data['net_quantity'].resample('MS').sum()

        # Display sales history
        st.line_chart(monthly_sales)

        # Forecast sales
        forecast_dict = forecast_sales(monthly_sales)

        # Display forecasts
        for period, forecast_df in forecast_dict.items():
            st.write(f"Forecast for {period}:")
            st.write(forecast_df)

            # Plotting
            plt.figure(figsize=(10, 6))
            plt.plot(monthly_sales.index, monthly_sales, label='Historical Monthly Sales')
            plt.plot(forecast_df['Forecast Date'], forecast_df['Forecasted Units'], label='Forecasted Monthly Sales', linestyle='--')
            plt.title(f'Monthly Sales Forecast for Selected Product')
            plt.xlabel('Month')
            plt.ylabel('Units Sold')
            plt.legend()
            plt.grid(True)
            st.pyplot(plt)
