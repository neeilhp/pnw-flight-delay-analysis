"""
PNW Flight Delay & Cancellation Analysis
----------------------------------------
This script analyzes flight delays and cancellations
using the pnwflights2022 dataset.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def main():
    # -------------------------------
    # Load the data
    # -------------------------------
    flights2022 = pd.read_csv("C:/Users/neelp/Portfolio/pnw-flight-delay-analysis/data/flights2022.csv")
    flights_weather2022 = pd.read_csv("C:/Users/neelp/Portfolio/pnw-flight-delay-analysis/data/flights_weather2022.csv")

    # Create folder for plots
    os.makedirs("plots", exist_ok=True)

    # -------------------------------
    # Route Analysis
    # -------------------------------
    flights2022["route"] = flights2022["origin"] + "-" + flights2022["dest"]

    routes_delays_cancels = flights2022.groupby("route").agg(
        mean_dep_delay=("dep_delay", "mean"),
        total_cancellations=("dep_time", lambda x: x.isna().sum())
    ).reset_index()

    # Top 9 by delay & cancellations
    top_routes_by_delay = routes_delays_cancels.sort_values(
        "mean_dep_delay", ascending=False
    ).head(9)

    top_routes_by_cancellations = routes_delays_cancels.sort_values(
        "total_cancellations", ascending=False
    ).head(9)

    # Plot cancellations
    fig, ax = plt.subplots()
    ax.bar(
        top_routes_by_cancellations["route"],
        top_routes_by_cancellations["total_cancellations"]
    )
    ax.set_xlabel("Route")
    ax.set_ylabel("Total Cancellations")
    ax.set_title("Routes with Highest Number of Cancellations")
    ax.set_xticklabels(top_routes_by_cancellations["route"], rotation=90)
    plt.tight_layout()
    plt.savefig("plots/top_routes_cancellations.png", dpi=300)
    plt.close()

    # -------------------------------
    # Airline Analysis
    # -------------------------------
    airlines_delays_cancels = flights2022.groupby("airline").agg(
        mean_dep_delay=("dep_delay", "mean"),
        total_cancellations=("dep_time", lambda x: x.isna().sum())
    ).reset_index()

    top_airlines_by_delay = airlines_delays_cancels.sort_values(
        "mean_dep_delay", ascending=False
    ).head(9)

    top_airlines_by_cancellations = airlines_delays_cancels.sort_values(
        "total_cancellations", ascending=False
    ).head(9)

    # Plot delays
    fig, ax = plt.subplots()
    ax.bar(
        top_airlines_by_delay["airline"],
        top_airlines_by_delay["mean_dep_delay"]
    )
    ax.set_xlabel("Airline")
    ax.set_ylabel("Mean Departure Delay")
    ax.set_title("Airlines with Highest Mean Departure Delays")
    ax.set_xticklabels(top_airlines_by_delay["airline"], rotation=90)
    plt.tight_layout()
    plt.savefig("plots/top_airlines_delays.png", dpi=300)
    plt.close()

    # -------------------------------
    # Weather Impact Analysis
    # -------------------------------
    flights_weather2022["group"] = flights_weather2022["wind_gust"].apply(
        lambda x: ">= 10mph" if x >= 10 else "< 10 mph"
    )

    wind_grouped_data = flights_weather2022.groupby(
        ["group", "origin"]
    ).agg(mean_dep_delay=("dep_delay", "mean"))

    print("\nImpact of Wind Gusts on Departure Delays:")
    print(wind_grouped_data)


if __name__ == "__main__":
    main()
