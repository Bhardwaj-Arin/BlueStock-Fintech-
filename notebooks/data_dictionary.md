# Data Dictionary — Mutual Fund Analytics Database

## 1. Table: dim_fund (Dimension Table)
Defines structural details and risk attributes for each unique mutual fund scheme tracking index.

| Column Name | Data Type | Primary/Foreign Key | Description |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Primary Key | Unique 6-digit reference identification key allocated by AMFI. |
| `fund_house` | TEXT | - | Asset Management Company (AMC) name brand handling operations. |
| `scheme_name` | TEXT | - | Complete legal naming designation of the specific mutual fund index. |
| `category` | TEXT | - | Broad asset marketplace categorization profile (Equity, Debt, etc.). |
| `sub_category`| TEXT | - | Specific fund strategy classifications (Large Cap, Mid Cap, etc.). |
| `risk_category`| TEXT | - | Risk evaluation level grade markers (Low, Moderate, High, Very High). |

## 2. Table: dim_date (Dimension Table)
Time-series calendar dimensional hierarchy mapping table for optimal temporal trend partitioning.

| Column Name | Data Type | Primary/Foreign Key | Description |
| :--- | :--- | :--- | :--- |
| `date` | TEXT | Primary Key | Calendar tracking date index string value formatted strictly as YYYY-MM-DD. |
| `year` | INTEGER | - | Calendar Year identification grouping digit value. |
| `month` | INTEGER | - | Calendar Month tracking index integer range value (1 to 12). |
| `day` | INTEGER | - | Specific day component value mapping index number (1 to 31). |
| `quarter` | INTEGER | - | Calendar year financial operational quarter index segment count (1 to 4). |
| `is_weekend` | INTEGER | - | Flag value determining if day matches holiday weekends (1 = Yes, 0 = No). |

## 3. Table: fact_nav (Fact Table)
Tracks the daily net asset historical evaluation price records across fund codes.

| Column Name | Data Type | Primary/Foreign Key | Description |
| :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER | Primary Key | Auto-incremented unique relational database key row identifier. |
| `amfi_code` | INTEGER | Foreign Key | References `dim_fund(amfi_code)` index code. |
| `date` | TEXT | Foreign Key | References `dim_date(date)` time mapping parameter. |
| `nav` | REAL | - | Net Asset Value valuation close price metric. |

## 4. Table: fact_transactions (Fact Table)
Captures granular purchasing actions, redemptions, and investor geographical distributions.

| Column Name | Data Type | Primary/Foreign Key | Description |
| :--- | :--- | :--- | :--- |
| `transaction_id`| INTEGER | Primary Key | Auto-incremented transaction log entry marker. |
| `investor_id` | INTEGER | - | Customer reference indicator identification tracking integer. |
| `transaction_date`| TEXT | Foreign Key | References calendar tracking identifier in `dim_date(date)`. |
| `amfi_code` | INTEGER | Foreign Key | References unique investment asset group inside `dim_fund(amfi_code)`. |
| `transaction_type`| TEXT | - | Standardized action flag text descriptor (SIP, Lumpsum, Redemption). |
| `amount_inr` | REAL | - | Total cash currency scale volume metric parsed in INR. |
| `state` | TEXT | - | Regional territory location descriptor flag of the transacting customer. |
| `city` | TEXT | - | Urban municipality city location parameter of the investor. |
| `kyc_status` | TEXT | - | Compliance screening status evaluation value. |
