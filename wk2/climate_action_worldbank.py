#!/usr/bin/python3
import pandas as pd
import wbdata
import datetime
import matplotlib.pyplot as plt

def fetch_indicator_data(countries, indicators, start_year=2000, end_year=2023):
    """Fetches indicator data from the World Bank API."""
    all_data = []
sp
    for country in countries:
        for indicator_name, indicator_code in indicators.items():
            print(f"Fetching {indicator_code} for {country}...")
            try:
                data = wbdata.get_dataframe(
                    {indicator_code: indicator_name},
                    country=country,
                    data_date=(datetime.datetime(start_year, 1, 1), datetime.datetime(end_year, 12, 31)),
                    convert_date=True
                ).reset_index()
                data["iso3"] = country
                all_data.append(data)
            except Exception as e:
                print(f"⚠️ Skipping {country} - {indicator_code}: {e}")

    if not all_data:
        print("❌ No data retrieved. Please check your internet or API availability.")
        return pd.DataFrame()

    raw = pd.concat(all_data, ignore_index=True)
    return raw

def process_data(raw):
    """Cleans and reshapes the data."""
    if raw.empty:
        print("❌ No data available to process.")
        return pd.DataFrame()

    # Remove duplicates and missing values
    raw.dropna(subset=["value"], inplace=True)
    raw.drop_duplicates(inplace=True)

    # If required columns are missing, abort gracefully
    required_cols = ["iso3", "country", "date", "indicator", "value"]
    missing = [col for col in required_cols if col not in raw.columns]
    if missing:
        print(f"⚠️ Missing columns in data: {missing}")
        return pd.DataFrame()

    # Safe pivot
    try:
        df = raw.pivot_table(
            index=["iso3", "country", "date"],
            columns="indicator",
            values="value",
            aggfunc="mean"
        ).reset_index()
    except Exception as e:
        print(f"⚠️ Pivot failed: {e}")
        return pd.DataFrame()

    return df

def plot_data(df):
    """Plots CO2 emissions and renewable energy trends."""
    if df.empty:
        print("⚠️ No data available to plot.")
        return

    plt.figure(figsize=(10, 6))
    for country in df["country"].unique():
        subset = df[df["country"] == country]
        plt.plot(subset["date"], subset["CO2 emissions (metric tons per capita)"], label=f"{country} - CO₂")

    plt.title("CO₂ Emissions per Capita (2000–2023)")
    plt.xlabel("Year")
    plt.ylabel("Metric Tons per Capita")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    for country in df["country"].unique():
        subset = df[df["country"] == country]
        plt.plot(subset["date"], subset["Renewable energy consumption (% of total final energy consumption)"], label=f"{country} - Renewables")

    plt.title("Renewable Energy Consumption (2000–2023)")
    plt.xlabel("Year")
    plt.ylabel("% of Total Energy Consumption")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    countries = ["KEN", "USA", "CHN", "DEU", "IND"]
    indicators = {
        "CO2 emissions (metric tons per capita)": "EN.ATM.CO2E.PC",
        "Renewable energy consumption (% of total final energy consumption)": "EG.FEC.RNEW.ZS"
    }

    raw = fetch_indicator_data(countries, indicators)
    if raw.empty:
        print("❌ No data returned — exiting.")
        return

    df = process_data(raw)
    if df.empty:
        print("❌ Could not process data — exiting.")
        return

    print(df.head())
    plot_data(df)

if __name__ == "__main__":
    main()

