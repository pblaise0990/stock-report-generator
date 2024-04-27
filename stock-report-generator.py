import requests
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import matplotlib.pyplot as plt
import io
from PIL import Image as PILImage
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import matplotlib.dates as mdates
from datetime import datetime

api_key = "YOUR_API_KEY"

def get_stock_data(symbol):
    base_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        if "Global Quote" in data:
            return data["Global Quote"]
        else:
            print(f"Error: Global Quote not found in the response for symbol {symbol}")
    else:
        print(f"Error: API request failed with status code {response.status_code}")
    return None

def get_company_info(symbol):
    base_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data
        else:
            print(f"Error: Company info not found for symbol {symbol}")
    else:
        print(f"Error: API request failed with status code {response.status_code}")
    return None

def get_technical_indicators(symbol, interval):
    base_url = f"https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval={interval}&time_period=20&series_type=close&apikey={api_key}"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        if "Technical Analysis: SMA" in data:
            return data["Technical Analysis: SMA"]
        else:
            print(f"Error: Technical Analysis: SMA not found in the response for symbol {symbol}")
    else:
        print(f"Error: API request failed with status code {response.status_code}")
    return None

def generate_sma_graph(sma_data):
    if not sma_data:
        return None

    timestamps = []
    sma_values = []
    for timestamp, sma in sma_data.items():
        timestamps.append(datetime.strptime(timestamp, "%Y-%m-%d %H:%M"))
        sma_values.append(float(sma['SMA']))

    plt.figure(figsize=(6, 3))
    plt.plot(timestamps, sma_values, color='#FF9800', linewidth=2, label='SMA')
    plt.xlabel('Date')
    plt.ylabel('SMA Value')
    plt.title('Simple Moving Average (SMA)', fontsize=12)
    plt.grid(True, color='#EEEEEE', linewidth=0.5)
    plt.xticks(rotation=45, ha='right')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.legend(loc='upper left')
    plt.tight_layout()

    graph_buffer = io.BytesIO()
    plt.savefig(graph_buffer, format='png', dpi=200)
    graph_buffer.seek(0)
    graph_image = Image(graph_buffer, width=5*inch, height=2.5*inch)

    return graph_image

def generate_stock_report_pdf(symbol):
    stock_data = get_stock_data(symbol)
    company_info = get_company_info(symbol)
    technical_indicators = get_technical_indicators(symbol, "60min")

    if not stock_data or not company_info:
        print("Error: Insufficient data to generate the report")
        return

    pdf_filename = f"{symbol}_stock_report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    subtitle_style = styles["Heading2"]
    normal_style = styles["Normal"]

    # Cover Page
    company_name = company_info.get('Name', '')
    cover_title = f"Stock Report: {company_name} ({symbol})"
    cover_subtitle = f"Generated on {stock_data.get('07. latest trading day', '')}"

    cover_style = ParagraphStyle(
        name='CoverStyle',
        parent=normal_style,
        fontSize=28,
        leading=34,
        textColor=HexColor("#FFFFFF"),
        alignment=1,
    )

    cover_subtitle_style = ParagraphStyle(
        name='CoverSubtitleStyle',
        parent=normal_style,
        fontSize=16,
        leading=20,
        textColor=HexColor("#FFFFFF"),
        alignment=1,
    )

    cover_page = Paragraph(cover_title, cover_style)
    cover_subtitle_para = Paragraph(cover_subtitle, cover_subtitle_style)

    # Create a table for the cover page
    cover_table = Table([[cover_page], [cover_subtitle_para]], colWidths=[6*inch], rowHeights=[3*inch, 1*inch])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor("#007BFF")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 50),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 50),
    ]))

    elements.append(cover_table)
    elements.append(PageBreak())

    # Table of Contents
    toc_title = Paragraph("Table of Contents", subtitle_style)
    toc_data = [
        ["Real-time Stock Data", 2],
        ["Company Information", 3],
        ["Technical Indicators", 4]
    ]
    toc_table = Table(toc_data, colWidths=[4*inch, inch], hAlign='LEFT')
    toc_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(toc_title)
    elements.append(Spacer(1, 12))
    elements.append(toc_table)
    elements.append(PageBreak())

    # Real-time Stock Data
    stock_data_title = Paragraph("Real-time Stock Data", subtitle_style)
    elements.append(stock_data_title)
    elements.append(Spacer(1, 12))

    stock_data_table = Table([
        ["Metric", "Value"],
        ["Symbol", stock_data.get('01. symbol', '')],
        ["Price", stock_data.get('05. price', '')],
        ["Change", stock_data.get('09. change', '')],
        ["Change Percent", stock_data.get('10. change percent', '')],
        ["Latest Trading Day", stock_data.get('07. latest trading day', '')],
        ["Previous Close", stock_data.get('08. previous close', '')]
    ])
    stock_data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#007BFF")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(stock_data_table)
    elements.append(Spacer(1, 24))

    # Company Information
    company_info_title = Paragraph("Company Information", subtitle_style)
    elements.append(company_info_title)
    elements.append(Spacer(1, 12))

    company_info_table = Table([
        ["Metric", "Value"],
        ["Name", company_info.get('Name', '')],
        ["Exchange", company_info.get('Exchange', '')],
        ["Sector", company_info.get('Sector', '')],
        ["Industry", company_info.get('Industry', '')],
        ["Market Capitalization", company_info.get('MarketCapitalization', '')],
        ["PE Ratio", company_info.get('PERatio', '')],
        ["Dividend Yield", company_info.get('DividendYield', '')],
        ["EPS", company_info.get('EPS', '')]
    ])
    company_info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#28A745")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(company_info_table)
    elements.append(Spacer(1, 12))

    description_text = Paragraph(company_info.get('Description', ''), normal_style)
    elements.append(description_text)
    elements.append(Spacer(1, 24))

    # Technical Indicators
    technical_indicators_title = Paragraph("Technical Indicators", subtitle_style)
    elements.append(technical_indicators_title)
    elements.append(Spacer(1, 12))

    if technical_indicators:
        sma_graph_image = generate_sma_graph(technical_indicators)
        if sma_graph_image:
            elements.append(sma_graph_image)
            elements.append(Spacer(1, 12))

        sma_table_data = [["Timestamp", "SMA"]]
        for timestamp, sma in technical_indicators.items():
            sma_table_data.append([timestamp, sma['SMA']])

        sma_table = Table(sma_table_data)
        sma_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor("#FFC107")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(sma_table)
    else:
        elements.append(Paragraph("No technical indicators available.", normal_style))

    doc.build(elements)
    print(f"Stock report generated: {pdf_filename}")

symbol = "AAPL"
generate_stock_report_pdf(symbol)
