"""
authors: Kadir O. Altunel, Ronny Toribio
project: Covid and Air Travel
"""
import csv
import math

import matplotlib.pyplot as plt
import seaborn as sns


def predict(alpha, beta, x_i):
    return beta * x_i + alpha


def error(alpha, beta, x_i, y_i):
    return predict(alpha, beta, x_i) - y_i


def sum_of_sqerrors(alpha, beta, x, y):
    return sum(error(alpha, beta, x_i, y_i) ** 2
               for x_i, y_i in zip(x, y))

def mean(x):
    return sum(x) / len(x)


def de_mean(x):
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

 
def dot(v, w):
    return sum(v_i * w_i
               for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    return dot(v, v)


def variance(x):
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)

 
def standard_deviation(x):
    return math.sqrt(variance(x))

 
def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)


def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
      return 0


def least_squares_fit(x, y):
    beta = correlation(x, y) * standard_deviation(y) / standard_deviation(x)
    alpha = mean(y) - beta * mean(x)
    return alpha, beta


def total_sum_of_squares(y):
    return sum(v ** 2 for v in de_mean(y))


def r_squared(alpha, beta, x, y):
    return 1.0 - (sum_of_sqerrors(alpha, beta, x, y) / total_sum_of_squares(y))


def load_data(filename = "data/covidandairtravel.csv"):
    year = []
    fuel = []
    enplanements = []
    revenue = []
    with open(filename, "r") as f:
        file = csv.DictReader(f)
        for row in file:
            year.append(int(row['Years']))
            fuel.append(float(row['Fuel Consumption']))
            enplanements.append(float(row['Enplanements']))
            revenue.append(float(row['Revenue Streams']))
    return year, fuel, enplanements, revenue
    

def plot_data(year, ydata, yname, color):
    plt.figure(figsize=(10, 10))
    plt.plot(year, ydata, color=color, marker='o')
    plt.title('Year vs {}'.format(yname), fontsize=14)
    plt.xticks(year)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel(yname, fontsize=14)
    plt.grid(True)
    plt.show()


def plot_regression_data(xdata, ydata, xname, yname, year):
    plot = sns.jointplot(x = xdata, y = ydata, kind = "reg");
    plot.ax_joint.set_xticks(year)
    plot.ax_joint.set_xlabel(xname, fontweight='bold')
    plot.ax_joint.set_ylabel(yname, fontweight='bold')
    alpha, beta = least_squares_fit(xdata, ydata)
    print("Pearson correlation coefficient for {} vs {} is: {}".format(xname, yname, r_squared(alpha, beta, xdata, ydata)))


if __name__ == "__main__":
    year, fuel, enplanements, revenue = load_data("data/covidandairtravel.csv")
    plot_data(year, fuel, "Fuel Consumption", "r")
    plot_data(year, enplanements, "Enplanements", "g")
    plot_data(year, revenue, "Revenue Streams", "b")
    print("The fit for year vs fuel consumption is: ",  least_squares_fit(year, fuel))
    print("The fit for year vs enplanements is: ",  least_squares_fit(year, enplanements))
    print("The fit for year vs revenue stream is: ",  least_squares_fit(year, revenue))
    print("The fit for enplanements vs fuel consumption is: ",  least_squares_fit(enplanements, fuel))
    print("The fit for enplanements vs revenue stream is: ",  least_squares_fit(enplanements, revenue))
    print("The fit for fuel consumption vs revenue stream is: ",  least_squares_fit(fuel, revenue))
    plot_regression_data(year, fuel, "Year", "Fuel Consumption", year)
    plot_regression_data(year, enplanements, "Year", "Enplanements", year)
    plot_regression_data(year, revenue, "Year", "Revenue Streams", year)
    plot_regression_data(enplanements, fuel, "Enplanements", "Fuel Consumption", year)
    plot_regression_data(enplanements, revenue, "Enplanements", "Revenue Streams", year)
    plot_regression_data(fuel, revenue, "Fuel Consumption", "Revenue Streams", year)
