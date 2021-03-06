#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matplotlib as mpl

mpl.rcParams['svg.hashsalt'] = 42


# Convert Cases to numpy array for easier manipulation

def derivative(data):

    # Add an extra zero up front
    data = np.append([0],data)

    # Calculate Day or Day Change
    return data[1:] - data[0:-1]

def smooth(data,N=14):
    output = np.convolve(data, np.ones(N)/N, mode='valid')
    return np.append(np.zeros(N-1),output)

def running_percentile(data,pct=50,N=14):
    output = []
    for i in range(len(data)-N+1):
        chunk = data[i:i+N]
        output.append(np.percentile(chunk,pct))


    return np.append(np.zeros(N-1),output)

def clean_dates(df):
    df["Date"] = pd.to_datetime(df["date"])
    df = df.drop(["date"],axis=1)
    df.set_index("Date")
    return df

def calc_stats(df):
    df["New Cases"] = derivative(df["cases"].to_numpy())
    df  = df.drop(["cases"],axis=1)

    df["New Deaths"] = derivative(df["deaths"].to_numpy())
    df  = df.drop(["deaths"],axis=1)

    #df["Avg Cases"] = smooth(df["New Cases"])
    #df["Avg Deaths"] = smooth(df["New Deaths"])

    df["Avg Cases"] = running_percentile(df["New Cases"])
    df["Avg Deaths"] = running_percentile(df["New Deaths"])

    df["90%ile Cases"] = running_percentile(df["New Cases"],90)
    df["90%ile Deaths"] = running_percentile(df["New Deaths"],90)

    df["30%ile Cases"] = running_percentile(df["New Cases"],30)
    df["30%ile Deaths"] = running_percentile(df["New Deaths"],30)


    df  = df.drop(["New Cases"],axis=1)
    df  = df.drop(["New Deaths"],axis=1)

    return df

def list_states():
    df = pd.read_csv("covid-19-data/us-states.csv")
    return sorted(df["state"].unique())

def get_us_data():
    df = pd.read_csv("covid-19-data/us.csv")
    df = clean_dates(df)


    return calc_stats(df)

def get_state_data(state):
    df = pd.read_csv("covid-19-data/us-states.csv")
    df = clean_dates(df)

    df = df[df["state"].isin([state])]
    df  = df.drop(["state"],axis=1)
    df  = df.drop(["fips"],axis=1)

    return calc_stats(df)

def get_county_data(county,state):
    df = pd.read_csv("covid-19-data/us-counties.csv")
    df = clean_dates(df)

    #date,county,state,fips,cases,deaths

    df = df[df["county"].isin([county])]
    df = df[df["state"].isin([state])]

    df  = df.drop(["state"],axis=1)
    df  = df.drop(["county"],axis=1)
    df  = df.drop(["fips"],axis=1)

    return calc_stats(df)

def plot_data(df,name):

    print("Plotting",name)

    df.plot(x="Date", y=["Avg Cases", "Avg Deaths"], logy=True, grid=True, figsize=(11,8.5))

    plt.fill_between(df["Date"].to_numpy(),df["90%ile Cases"],df["30%ile Cases"],color=[(0.5,0.5,1,0.5)])
    plt.fill_between(df["Date"].to_numpy(),df["90%ile Deaths"],df["30%ile Deaths"],color=[(1,0.5,0.5,0.5)])

    plt.grid(True,"both","y")


    plt.savefig("graphs/"+name+".svg",metadata={'Date': None})

    plt.clf()
    plt.close()



plot_data(get_us_data(),"USA")

for state in list_states():
    plot_data(get_state_data(state),state)

plot_data(get_county_data("Clark","Nevada"),"Vegas")
plot_data(get_county_data("New York City","New York"),"NYC")
plot_data(get_county_data("Los Angeles","California"),"LA")

