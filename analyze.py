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
            except:
                dataset_row["fuel"] = None
            try:
                enplanements = float(cols[2])
                dataset_row["enplanements"] = enplanements
            except:
                dataset_row["enplanements"] = None
            try:
                revenue = float(cols[3])
                dataset_row["revenue"] = revenue
            except:
                dataset_row["revenue"] = None
            dataset.append(dataset_row)
    return dataset


def impute_dataset_with_mean(dataset):
    fuel_mean = statistics.mean([x["fuel"] for x in dataset if isinstance(x["fuel"], float)])
    enplanements_mean = statistics.mean([x["enplanements"] for x in dataset if isinstance(x["enplanements"], float)])
    revenue_mean = statistics.mean([x["revenue"] for x in dataset if isinstance(x["revenue"], float)])
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
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.plot(years, fuel, "y-", label="fuel consumption")
    ax.plot(years, enplanements, "b-", label="enplanements")
    ax.plot(years, revenue, "g-", label="revenue")
    ax.axvline("2020", color="r", linestyle=":")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    dataset = load_dataset()
    if dataset is not None:
        dataset = impute_dataset_with_mean(dataset)
        dataset = expand_dataset_values(dataset)
        print_dataset(dataset)
        plot_dataset(dataset)
        
