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
    fobj = open(filename)
    file = csv.DictReader(fobj)
    year = []
    fuel = []
    enplanements = []
    revenue = []
    for row in file:
        year.append(int(row['Years']))
        fuel.append(float(row['Fuel Consumption']))
        enplanements.append(float(row['Enplanements']))
        revenue.append(float(row['Revenue Streams']))
    return year, fuel, enplanements, revenue
    

def plot_data(year, fuel, enplanements, revenue):
    plt.figure(figsize=(10, 10))
    plt.plot(year, fuel, color='red', marker='o')
    plt.title('Year vs Fuel Consumption', fontsize=14)
    plt.xticks([2004, 2006, 2008 ,2010, 2012, 2014, 2016, 2018, 2020])
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Fuel Consumption', fontsize=14)
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 10))
    plt.plot(year, enplanements, color='red', marker='o')
    plt.title('Year vs Enplanements', fontsize=14)
    plt.xticks([2004, 2006, 2008 ,2010, 2012, 2014, 2016, 2018, 2020])
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Enplanements', fontsize=14)
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 10))
    plt.plot(year, revenue, color='red', marker='o')
    plt.title('Year vs Revenue Streams', fontsize=14)
    plt.xticks([2004, 2006, 2008 ,2010, 2012, 2014, 2016, 2018, 2020])
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Revenue Streams', fontsize=14)
    plt.grid(True)
    plt.show()


def plot_regression_data(year, fuel, enplanements, revenue):
    plot1 = sns.jointplot(x = year, y = fuel, data = row, kind = "reg");
    plot1.ax_joint.set_xticks([2004, 2006, 2008 ,2010, 2012, 2014, 2016, 2018, 2020])
    plot1.ax_joint.set_xlabel('Year', fontweight='bold')
    plot1.ax_joint.set_ylabel('Fuel Consumption', fontweight='bold')
    alpha, beta = least_squares_fit(year, fuel)
    print("Pearson correlation coefficient for year vs fuel consumption is: ", 
          r_squared(alpha, beta, year, fuel))

    plot2 = sns.jointplot(x = year, y = enplanements, data = row, kind = "reg");
    plot2.ax_joint.set_xticks([2004, 2006, 2008 ,2010, 2012, 2014, 2016, 2018, 2020])
    plot2.ax_joint.set_xlabel('Year', fontweight='bold')
    plot2.ax_joint.set_ylabel('Enplanements', fontweight='bold')
    alpha, beta = least_squares_fit(year, enplanements)
    print("Pearson correlation coefficient for year vs enplanements is: ", 
          r_squared(alpha, beta, year, enplanements))

    plot3 = sns.jointplot(x = year, y = revenue, data = row, kind = "reg");
    plot3.ax_joint.set_xticks([2004, 2006, 2008 ,2010, 2012, 2014, 2016, 2018, 2020])
    plot3.ax_joint.set_xlabel('Year', fontweight='bold')
    plot3.ax_joint.set_ylabel('Revenue Stream', fontweight='bold')
    alpha, beta = least_squares_fit(year, revenue)
    print("Pearson correlation coefficient for year vs revenue stream is: ", 
          r_squared(alpha, beta, year, revenue))

    plot4 = sns.jointplot(x = enplanements, y = fuel, data = row, kind = "reg");
    plot4.ax_joint.set_xlabel('Enplanements', fontweight='bold')
    plot4.ax_joint.set_ylabel('Fuel Consumption', fontweight='bold')
    alpha, beta = least_squares_fit(enplanements, fuel)
    print("Pearson correlation coefficient for enplanements vs fuel consumption is: ", 
          r_squared(alpha, beta, enplanements, fuel))

    plot5 = sns.jointplot(x = enplanements, y = revenue, data = row, kind = "reg");
    plot5.ax_joint.set_xlabel('Enplanements', fontweight='bold')
    plot5.ax_joint.set_ylabel('Revenue Stream', fontweight='bold')
    alpha, beta = least_squares_fit(enplanements, revenue)
    print("Pearson correlation coefficient for enplanements vs revenue stream is: ", 
          r_squared(alpha, beta, enplanements, revenue))

    plot6 = sns.jointplot(x = fuel, y = revenue, data = row, kind = "reg");
    plot6.ax_joint.set_xlabel('Fuel Consumption', fontweight='bold')
    plot6.ax_joint.set_ylabel('Revenue Stream', fontweight='bold')
    alpha, beta = least_squares_fit(fuel, revenue)
    print("Pearson correlation coefficient for fuel consumption vs revenue stream is: ", 
          r_squared(alpha, beta, fuel, revenue))
    print(year)

if __name__ == "__main__":
    year, fuel, enplanements, revenue = load_data("data/covidandairtravel.csv")
    plot_data(year, fuel, enplanements, revenue)
    print("The fit for year vs fuel consumption is: ",  least_squares_fit(year, fuel))
    print("The fit for year vs enplanements is: ",  least_squares_fit(year, enplanements))
    print("The fit for year vs revenue stream is: ",  least_squares_fit(year, revenue))
    print("The fit for enplanements vs fuel consumption is: ",  least_squares_fit(enplanements, fuel))
    print("The fit for enplanements vs revenue stream is: ",  least_squares_fit(enplanements, revenue))
    print("The fit for fuel consumption vs revenue stream is: ",  least_squares_fit(fuel, revenue))
    plot_regression_data(year, fuel, enplanements, revenue)




