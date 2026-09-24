[Open the Live Streamlit Dashboard](https://hemanthgoud30-ecommerce-customer-sales-intelligence-app-aqozwk.streamlit.app/)
# E-Commerce Customer & Sales Intelligence

## AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026

A data analytics project focused on identifying high-value customers, potentially at-risk customers, sales trends, product revenue patterns, and actionable business opportunities using the UCI Online Retail dataset.

---

## 1. Project Overview

The **E-Commerce Customer & Sales Intelligence** project analyzes historical online retail transaction data to understand:

- Overall sales and revenue performance
- Monthly revenue trends
- Geographic revenue distribution
- Product-level revenue contribution
- Customer purchasing behavior
- Customer value using RFM analysis
- Customer segmentation
- Potentially at-risk customers
- Historical revenue associated with potentially at-risk customers
- Business opportunities for customer retention and re-engagement

The project follows a complete analytics workflow:

**Data → Cleaning → Analysis → Insights → Recommendations → Dashboard**

The final results are presented through an interactive **Streamlit dashboard**.

---

## 2. Project Objective

The main objectives of this project are to:

1. Analyze historical e-commerce transaction data.
2. Clean and prepare the raw transaction dataset.
3. Calculate important business KPIs.
4. Identify monthly sales and revenue trends.
5. Analyze revenue by country.
6. Identify the highest-revenue product descriptions.
7. Perform RFM (Recency, Frequency, Monetary) analysis.
8. Segment customers based on their purchasing behavior.
9. Identify potentially at-risk customers.
10. Quantify the historical revenue associated with potentially at-risk customers.
11. Generate business-focused insights and recommendations.
12. Build an interactive Streamlit dashboard for decision support.

---

## 3. Dataset

### Dataset Name

**Online Retail**

### Source

UCI Machine Learning Repository

Dataset page:

https://archive.ics.uci.edu/dataset/352/online+retail

### Dataset File

`Online Retail.xlsx`

### Dataset Description

The Online Retail dataset contains transaction records from a UK-based online retail business.

Important fields include:

| Column | Description |
|---|---|
| InvoiceNo | Invoice number identifying the transaction |
| StockCode | Product/item code |
| Description | Product description |
| Quantity | Number of units purchased |
| InvoiceDate | Date and time of transaction |
| UnitPrice | Price per unit |
| CustomerID | Customer identifier |
| Country | Customer country |

The dataset contains transactions from approximately December 2010 to December 2011.

Invoice numbers beginning with `C` represent cancelled transactions.

---

## 4. Technologies Used

### Programming & Analysis

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook / Google Colab

### Dashboard

- Streamlit
- Plotly

### Data Processing

- Excel
- CSV
- RFM Analysis

### Development Tools

- IBM Bob
- GitHub
- Streamlit

---

## 5. Project Workflow

The project follows these major stages:


Raw Dataset
     ↓
Data Cleaning
     ↓
Data Preparation
     ↓
Exploratory Data Analysis
     ↓
Business KPIs
     ↓
RFM Analysis
     ↓
Customer Segmentation
     ↓
Potentially At-Risk Analysis
     ↓
Business Insights
     ↓
Recommendations
     ↓
Streamlit Dashboard

---
## 6. Data Cleaning & Preparation

The raw Online Retail dataset was cleaned and prepared before analysis.

The main data preparation steps included:

Loading the Excel dataset using Pandas
Removing duplicate records
Identifying cancelled invoices
Excluding cancelled transactions from the sales analysis
Keeping transactions with positive quantities
Keeping transactions with valid unit prices
Handling missing Customer IDs for customer-level analysis
Converting InvoiceDate into datetime format
Creating a Revenue column
Revenue Calculation

Revenue was calculated as:

Revenue = Quantity × UnitPrice

Separate datasets were prepared for:

Overall sales analysis
Customer-level analysis
RFM analysis
Dashboard visualization
---
##7. Business KPIs

The project calculates the following major KPIs:

Total Revenue
Total Orders
Total Customers
Total Product Descriptions
Average Order Value
Current Results
KPI	Value
Total Revenue	£10,642,111
Total Orders	19,960
Total Customers	4,338
Unique Product Descriptions	4,026
Average Order Value	£533.17

These values are calculated from the cleaned transaction data used by the final dashboard.

---
## 8. Exploratory Data Analysis
8.1 Monthly Revenue Analysis

Monthly revenue was calculated to identify changes in sales performance over time.

The analysis shows that revenue reaches its highest level toward the end of the analyzed period, with a strong peak during November 2011.

The dashboard provides an interactive monthly revenue trend for easier analysis.

8.2 Country Revenue Analysis

Revenue was grouped by customer country to identify the major geographic contributors.

The United Kingdom represents the largest share of revenue.

Key Finding

The United Kingdom generated approximately:

£9,001,744

which represents approximately:

84.6%

of total revenue.

Other countries with significant revenue contributions include:

Netherlands
EIRE
Germany
France

---
## 9. Product Revenue Analysis

Products were analyzed based on their total historical revenue contribution.

The project identifies the highest-revenue product descriptions and displays the top 10 using interactive charts.

Highest-Revenue Description

The highest-revenue description in the analyzed dataset is:

DOTCOM POSTAGE

with historical revenue of approximately:

£206,249

Because DOTCOM POSTAGE may represent a postage or service-related transaction rather than a conventional physical product, it should be interpreted carefully when making product-related business decisions.

---
## 10. RFM Analysis

RFM analysis was used to understand customer purchasing behavior.

RFM stands for:

Recency

How recently a customer made a purchase.

Lower recency values indicate more recent purchases.

Frequency

How frequently a customer placed orders.

Higher frequency indicates more frequent purchasing.

Monetary

The total historical amount spent by the customer.

Higher monetary values indicate greater historical customer value.

---
## 11. RFM Scoring

Customers were assigned scores for:

R Score
F Score
M Score

The resulting RFM score combines these three dimensions.

Example:

555

indicates a customer with high scores across Recency, Frequency, and Monetary dimensions under the project's scoring method.

The project uses quintile-based scoring to assign RFM scores.

---
## 12. Customer Segmentation

Customers were grouped into segments using the project's defined RFM rules.

The following segments are included:

Customer Segment	Customers	Historical Monetary Value
Champions	957	£5,791,640.74
Loyal Customers	693	£1,298,467.95
Potential Loyalists	526	£519,252.99
Inactive / Others	1,705	£628,216.30
At Risk	457	£649,630.91

These segments are based on the project's RFM scoring and segmentation rules.

---
## 13. Champions

The Champions segment contains customers with strong Recency, Frequency, and Monetary scores according to the project's segmentation criteria.

Champions generated approximately:

£5,791,640.74

in historical monetary value.

This is the highest historical monetary value among the defined customer segments.

---
## 14. Potentially At-Risk Customers

A separate potentially-at-risk flag was created using the following condition:

R_Score <= 2 AND M_Score >= 3

This identifies customers who:

Have relatively low recency scores, meaning they have not purchased recently
Have relatively high monetary scores, meaning they had meaningful historical spending
Current Results
Potentially At-Risk Customers: 697

Historical revenue associated with these customers:

£1,070,170

Average historical spend per potentially at-risk customer is approximately:

£1,535

This group represents a historical revenue opportunity for targeted re-engagement and retention analysis.

Important Note

The Potentially At-Risk flag and the At Risk customer segment are not necessarily identical.

The customer segmentation rules are applied in a defined order, while the potentially-at-risk analysis separately checks:

R_Score <= 2 AND M_Score >= 3

Therefore, some customers meeting the potentially-at-risk condition may belong to another RFM segment.

---
## 15. Key Business Findings

The main findings from the analysis are:

Finding 1 — UK Revenue Concentration

The United Kingdom contributes approximately 84.6% of total revenue.

This indicates a strong concentration of historical revenue within the UK market.

Finding 2 — Champions Have the Highest Historical Monetary Value

Champions customers generated approximately:

£5,791,641

in historical monetary value, representing the highest historical monetary value among the defined customer segments.

Finding 3 — Potentially At-Risk Customer Opportunity

697 customers satisfy the project's potentially-at-risk condition.

These customers are associated with approximately:

£1,070,170

in historical revenue.

This provides a potential area for customer retention and re-engagement analysis.

Finding 4 — Inactive / Others Is the Largest Segment

The Inactive / Others segment contains:

1,705 customers

This is the largest customer segment by customer count.

Further analysis of this group may help identify opportunities for customer reactivation.

Finding 5 — Revenue Concentration Toward Year End

Monthly revenue analysis shows stronger revenue levels toward the end of the analyzed period, with a notable peak in November 2011.

This pattern can be considered when planning seasonal sales and customer engagement activities.

Finding 6 — DOTCOM POSTAGE Has the Highest Historical Revenue

DOTCOM POSTAGE is the highest-revenue description in the dataset, generating approximately:

£206,249

However, this should be treated carefully because it may represent postage/service-related transactions rather than a conventional product.

---
## 16. Business Recommendations

Based on the analysis, the following business actions can be considered:

16.1 Customer Retention

Focus retention analysis on potentially at-risk customers identified using:

R_Score <= 2 AND M_Score >= 3

Targeted communication and win-back campaigns can be evaluated for this group.

16.2 High-Value Customer Management

Champions and Loyal Customers have meaningful historical monetary value.

Businesses can consider:

Personalized offers
Loyalty programs
Early access to products
Targeted promotions
Customer relationship initiatives
16.3 Customer Re-Engagement

The Inactive / Others segment contains a large number of customers.

Further investigation can be performed to understand:

Why customers became inactive
Previous purchase behavior
Product preferences
Historical order frequency
Appropriate reactivation strategies
16.4 Geographic Analysis

Because the UK contributes the majority of historical revenue, businesses can analyze:

UK customer retention
Regional growth opportunities
International market development
Country-specific customer behavior
16.5 Product Analysis

The highest-revenue product descriptions should be investigated further to distinguish:

Physical products
Postage/service charges
Other transaction-related items

This prevents service-related revenue from being incorrectly interpreted as conventional product demand.

---
## 17. Streamlit Dashboard

The project includes an interactive Streamlit dashboard.

The dashboard is divided into three main analytical areas.

Page 1 — Executive Overview

The Executive Overview provides:

Total Revenue
Total Orders
Total Customers
Total Products
Average Order Value
Monthly Revenue Trend
Top Countries by Revenue
Key Business Findings
Page 2 — Sales & Product Analysis

This page provides:

Top 10 Products by Revenue
Top Countries by Revenue
Monthly Revenue Trend
Sales and product tables
Business interpretation of sales patterns
Page 3 — Customer & Risk Analysis

This page provides:

Customer Segments
Customers by Segment
Revenue by Segment
RFM information
Potentially At-Risk Customers
Historical revenue associated with potentially at-risk customers
Top customers by revenue
Customer-level analysis
---
## 18. Project Structure

The project is organized as follows:

Ecommerce_Customer_Sales_Intelligence/
│
├── 01_Raw_Data/
│   └── Online Retail.xlsx
│
├── 02_Colab_Analysis/
│   └── Ecommerce_Customer_Sales_Intelligence.ipynb
│
├── 03_Clean_Data/
│   ├── clean_sales_data.csv
│   ├── clean_customer_sales_data.csv
│   ├── customer_rfm_segments.csv
│   ├── monthly_revenue.csv
│   ├── country_revenue.csv
│   ├── top_products.csv
│   ├── segment_summary.csv
│   └── segment_revenue.csv
│
├── 04_Visualizations/
│   ├── monthly_revenue.png
│   ├── top_countries_revenue.png
│   ├── top_products_revenue.png
│   └── customer_segment_visualizations.png
│
├── 05_Project_Report/
│   └── Bachamgari_Hemanth_Goud_ProjectReport.docx
│
├── 06_Dashboard/
│   └── app.py
│
├── 07_Final_Files/
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   └── Project_Report.docx
│
├── app.py
├── requirements.txt
└── README.md

---
## 19. How to Run the Project Locally
Step 1 — Install Python

Install Python 3.x on your computer.

Verify the installation:

python --version
Step 2 — Open the Project Folder

Open a terminal or PowerShell inside:

Ecommerce_Customer_Sales_Intelligence
Step 3 — Install Required Packages

Run:

python -m pip install -r requirements.txt

If the python command is not available, use the Python executable installed on your system.

Step 4 — Run the Streamlit Dashboard

Run:

python -m streamlit run app.py

Alternatively:

streamlit run app.py
Step 5 — Open the Dashboard

After Streamlit starts, open the local URL displayed in the terminal.

Usually:

http://localhost:8501

---
## 20. Requirements

The main Python packages required by the project are:

streamlit
pandas
plotly
openpyxl

The complete package requirements are provided in:

requirements.txt

---
## 21. Code Files

The project contains:

Analysis Notebook
Ecommerce_Customer_Sales_Intelligence.ipynb

The notebook contains:

Data loading
Data cleaning
Exploratory data analysis
KPI calculations
Customer analysis
RFM analysis
Customer segmentation
Potentially at-risk analysis
Business insights
Recommendations
Dashboard-ready datasets
Streamlit Application
app.py

The Streamlit application provides the interactive dashboard.

---
## 22. Output Files

The project generates cleaned and analysis-ready datasets including:

clean_sales_data.csv
clean_customer_sales_data.csv
customer_rfm_segments.csv
monthly_revenue.csv
country_revenue.csv
top_products.csv
segment_summary.csv
segment_revenue.csv

These files are used for analysis and dashboard visualization.

---
## 23. Limitations

The following limitations should be considered:

The dataset represents historical transactions and does not represent current e-commerce activity.
The analysis is based on the available transaction records and customer identifiers.
Missing Customer IDs prevent some transactions from being included in customer-level RFM analysis.
RFM segmentation rules are project-specific and should not be treated as universal industry standards.
Potentially at-risk customers are identified using an analytical rule and should not be interpreted as confirmed churn.
Historical revenue associated with potentially at-risk customers does not represent revenue guaranteed to be lost.
DOTCOM POSTAGE may represent a service or postage-related transaction rather than a conventional physical product.
The analysis identifies patterns and opportunities but does not establish causal relationships.
The dataset covers a historical period and therefore business recommendations should be validated against current data before implementation.


---
## 24. Conclusion

The E-Commerce Customer & Sales Intelligence project demonstrates how transaction-level data can be transformed into business insights using Python, Pandas, RFM analysis, customer segmentation, and interactive visualization.

The project identifies:

Overall revenue and sales performance
Major geographic revenue contributors
High-revenue product descriptions
Valuable customer segments
Potentially at-risk customers
Historical revenue associated with potentially at-risk customers
Customer re-engagement and retention opportunities

The Streamlit dashboard converts the analytical results into an interactive format that can support business-oriented exploration and decision-making.

---
## 25. Dataset Reference

UCI Machine Learning Repository — Online Retail Dataset:

https://archive.ics.uci.edu/dataset/352/online+retail

---
## 26. Project Author

Bachamgari Hemanth Goud

B.Tech — Electrical and Electronics Engineering (EEE)

Gokaraju Rangaraju Institute of Engineering and Technology (GRIET), Hyderabad

---
## 27. Internship

AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026

Program / Internship Partner:

BharatCares

---
## 28. Project Status

Status: Completed

The project includes:

Data collection
Data cleaning
Exploratory data analysis
KPI analysis
RFM analysis
Customer segmentation
Potentially at-risk customer analysis
Business insights
Business recommendations
Streamlit dashboard
Project report
Requirements file
README documentation
## Live Dashboard

The interactive Streamlit dashboard for this project is available here:

[Open the Live Streamlit Dashboard](https://hemanthgoud30-ecommerce-customer-sales-intelligence-app-aqozwk.streamlit.app/)

The dashboard contains three main sections:

1. **Executive Overview** – Key business KPIs, revenue trends, and overall sales performance.
2. **Sales & Product Analysis** – Monthly revenue, country-level performance, and top products.
3. **Customer & Risk Analysis** – RFM-based customer segmentation and potentially at-risk customer analysis.
