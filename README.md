# stock-report-generator

This Python script generates a comprehensive stock report in PDF format using financial data from the Alpha Vantage API. The report includes real-time stock data, company information, and technical indicators such as the Simple Moving Average (SMA).

## Features

- Fetches real-time stock data and company information for a given stock symbol
- Generates a visually appealing PDF report with tables, graphs, and styled elements
- Provides an overview of the stock's performance and key metrics
- Includes a table of contents for easy navigation within the report
- Supports customization of report layout and styling

## Prerequisites

To run this script, you need to have the following:

- Python 3.x installed
- Required Python packages:
  - `requests`
  - `reportlab`
  - `matplotlib`
  - `pillow`
- Alpha Vantage API key (sign up at [Alpha Vantage](https://www.alphavantage.co/) to obtain a free API key)

## Installation

1. Clone the repository:
  git clone https://github.com/pblaise0990/stock-report-generator.git
2. Install the required Python packages:
  pip install -r requirements.txt
3. Replace the `api_key` variable in the code with your Alpha Vantage API key:
  api_key = "YOUR_API_KEY"

Usage

To generate a stock report, run the script with the desired stock symbol:
  python stock_report_generator.py

By default, the script generates a report for the "AAPL" stock symbol. You can modify the symbol variable in the code to generate a report for a different stock.
The generated stock report will be saved as a PDF file in the same directory with the filename {symbol}_stock_report.pdf.
Customization
The script allows for customization of the report layout and styling. You can modify the code in the generate_stock_report_pdf() function to adjust the following:

Cover page design
Table of contents
Real-time stock data table
Company information table
Technical indicators section
Styling of tables, paragraphs, and other elements

Feel free to experiment with different styles, colors, and layouts to create a report that suits your preferences.
Troubleshooting

If you encounter any issues with the Alpha Vantage API, such as rate limits or API key errors, please refer to the Alpha Vantage documentation for guidance.
If the script fails to generate the report due to missing data or API errors, check the console output for error messages and ensure that the API key is valid and the stock symbol is correct.

Contributing
Contributions are welcome! If you find any bugs, have suggestions for improvements, or want to add new features, please open an issue or submit a pull request.
License
This project is licensed under the MIT License.
