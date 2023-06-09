import copy
import datetime as dt
import json
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


def make_plots(data, outdir, ylim=[0, 4000]):
    """
    Make plots for each channel
    """
    # channel 1
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    x = [ dt.datetime.fromtimestamp(i) for i in np.array(data["1"]["DP"]["time"])]
    y = np.array(data["1"]["lidar_range"])
    Z = np.array(data["1"]["DP"]["data"]).T
    p = ax.pcolormesh(
        x,
        y,
        Z,
        vmin=1e5,
        vmax=1e7,
        norm="log",
        cmap="viridis",
    )
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    cbar = plt.colorbar(p)
    cbar.set_label("calibrated range corrected backscatter")
    plt.ylim(ylim)
    plt.ylabel("Altitude (m)")
    plt.xlabel(f"Time (UTC {x[1].strftime('%Y-%m-%d')})")
    plt.savefig(f"{outdir}/channel1.png")
    plt.close()
    
    # channel 2
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    x = [ dt.datetime.fromtimestamp(i) for i in np.array(data["2"]["DP"]["time"])]
    y = np.array(data["2"]["lidar_range"])
    Z = np.array(data["2"]["DP"]["data"]).T
    p = ax.pcolormesh(
        x,
        y,
        Z,
        vmin=1e4,
        vmax=1e7,
        norm="log",
        cmap="viridis",
    )
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    cbar = plt.colorbar(p)
    cbar.set_label("calibrated range corrected backscatter")
    plt.ylim(ylim)
    plt.ylabel("Altitude (m)")
    plt.xlabel(f"Time (UTC {x[1].strftime('%Y-%m-%d')})")
    plt.savefig(f"{outdir}/channel2.png")
    plt.close()
    
    # channel 11
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    x = [ dt.datetime.fromtimestamp(i) for i in np.array(data["11"]["DP"]["time"])]
    y = np.array(data["11"]["lidar_range"])
    Z = np.array(data["11"]["DP"]["data"]).T
    p = ax.pcolormesh(
        x,
        y,
        Z,
        vmin=1e5,
        vmax=1e8,
        norm="log",
        cmap="viridis",
    )
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    cbar = plt.colorbar(p)
    cbar.set_label("calibrated range corrected backscatter")
    plt.ylim(ylim)
    plt.ylabel("Altitude (m)")
    plt.xlabel(f"Time (UTC) {x[1].strftime('%Y-%m-%d')}")
    plt.savefig(f"{outdir}/channel11.png")
    plt.close()


def read_json(json_file):
    """
    Read json file, as written by ncas-lidar-aerosol-1-software.read_data.save_to_json
    """
    with open(json_file,"r") as f:
        d = json.load(f)
    return d["data_dict"], d["metadata_dict"]


def join_data(all_data):
    """
    Take all_data with separate entries by time, return all_data_joined with one entry
    """
    all_data_joined = {}
    for id_channel in all_data[0].keys():
        all_data_joined[id_channel] = {}
        for key, value in all_data[0][id_channel].items():
            all_data_joined[id_channel][key] = copy.deepcopy(value)
            
    for i in range(1,len(all_data)):
        for id_channel in all_data[i].keys():
            for key, value in all_data[i][id_channel].items():
                if isinstance(value,str):
                    if not all_data_joined[id_channel][key] == value:
                        print('oops')
                elif isinstance(value, dict):
                    for k2,v2 in all_data[i][id_channel][key].items():
                        if isinstance(all_data_joined[id_channel][key][k2],(list,np.ndarray)):
                            all_data_joined[id_channel][key][k2].extend(v2)
                            
    return all_data_joined


def main_from_json(input_files, outdir):
    """
    Create plots from json data
    input_files - str or list of str of json files
    outdir - where to save images
    """
    if isinstance(input_files, str):
        input_files = [input_files]

    all_data = []
    all_metadata = []
    for input_file in input_files:
        data, metadata = read_json(input_file)
        all_data.append(data)
        all_metadata.append(data)

    data = join_data(all_data)

    if not os.path.exists(f"{outdir}/4km"):
        os.mkdir(f"{outdir}/4km")
    if not os.path.exists(f"{outdir}/15km"):
        os.mkdir(f"{outdir}/15km")
        
    make_plots(data, f"{outdir}/4km", ylim=[0, 4000])
    make_plots(data, f"{outdir}/15km", ylim=[0, 15000])

    
def main_from_netcdf(input_file, outdir):
    """
    Create plots from netcdf data
    """
    pass


if __name__ == "__main__":
    outdir = sys.argv[1]
    infiles = sys.argv[2:]
    main_from_json(infiles, outdir)
