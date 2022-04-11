#!/usr/bin/python3
"""
@authors: Ronny Toribio, Kadir O. Altunel
@project: Covid and air travel
"""
import os.path
import statistics
import matplotlib.pyplot as plt


MILLION = 1000000
BILLION = 1000000000


def load_dataset(data_path="data/covidandairtravel.csv"):
    if not os.path.exists(data_path):
        return None
    dataset = []
    with open(data_path, "r") as f:
        data_str = f.read()
        for row in data_str.split("\n"):
            if "Years" in row:
                continue
            cols = row.split(",")
            dataset_row = {}
            if len(cols) != 4:
                continue
            year, fuel, enplanments, revenue = (None, None, None, None)
            if not cols[0]:
                continue
            dataset_row["year"] = cols[0]
            try:
                fuel = float(cols[1])
                dataset_row["fuel"] = fuel
            except ValueError:
                dataset_row["fuel"] = None
            try:
                enplanements = float(cols[2])
                dataset_row["enplanements"] = enplanements
            except ValueError:
                dataset_row["enplanements"] = None
            try:
                revenue = float(cols[3])
                dataset_row["revenue"] = revenue
            except ValueError:
                dataset_row["revenue"] = None
            dataset.append(dataset_row)
    return dataset


def impute_dataset_with_mean(dataset):
    # attempt to get means for fuel, enplanements and revenue
    try:
        fuel_mean = statistics.mean([x["fuel"] for x in dataset if isinstance(x["fuel"], float)])
        enplanements_mean = statistics.mean([x["enplanements"] for x in dataset if isinstance(x["enplanements"], float)])
        revenue_mean = statistics.mean([x["revenue"] for x in dataset if isinstance(x["revenue"], float)])
    except statistics.StatisticsError:
        return dataset
    
    # impute missing values with means
    for row in dataset:
        if len(row) != 4:
            continue
        if row["fuel"] is None:
            row["fuel"] = fuel_mean
        if row["enplanements"] is None:
            row["enplanements"] = enplanements_mean
        if row["revenue"] is None:
            row["revenue"] = revenue_mean
    return dataset


def expand_dataset_values(dataset):
    for row in dataset:
        if len(row) != 4:
            continue
        row["fuel"] *= BILLION
        row["enplanements"] *= MILLION
        row["revenue"] *= BILLION
    return dataset


def dataset_to_lists(dataset):
    return (
        [x["year"] for x in dataset],
        [x["fuel"] for x in dataset],
        [x["enplanements"] for x in dataset],
        [x["revenue"] for x in dataset]
    )


def print_dataset(dataset):
    print("{:<10} {:<20} {:<20} {:<20}".format("Years", "Fuel Consumption", "Enplanements", "Revenue Streams"))
    for row in dataset:
        print("{:<10} {:<20,.2f} {:<20,.2f} ${:<20,.2f}".format(row["year"], row["fuel"], row["enplanements"], row["revenue"]))


def plot_dataset(dataset):
    years, fuel, enplanements, revenue = dataset_to_lists(dataset)
    fig, ax1 = plt.subplots(1, 1, figsize=(12, 8))
    ax2 = ax1.twinx()
    ax1.set_xlabel("Year", color="r")
    ax1.tick_params(axis="x", labelcolor="r")
    ax1.set_ylabel("Billions", color="g")
    ax1.tick_params(axis="y", labelcolor="g")
    ax2.set_ylabel("Millions", color="b")
    ax2.tick_params(axis="y", labelcolor="b")
    ax1.plot(years, fuel, "y-", label="fuel consumption")
    ax2.plot(years, enplanements, "b-", label="enplanements")
    ax1.plot(years, revenue, "g-", label="revenue")
    ax1.axvline("2019", color="r", linestyle=":")
    ax1.axvline("2020", color="r", linestyle=":")
    ax1.axvline("2021", color="r", linestyle=":")
    ax1.legend()
    plt.show()


if __name__ == "__main__":
    dataset = load_dataset()
    if dataset is not None:
        dataset = impute_dataset_with_mean(dataset)
        dataset = expand_dataset_values(dataset)
        print_dataset(dataset)
        plot_dataset(dataset)
        
