import numpy as np
import matplotlib.pyplot as plt
import math
import lightkurve as lk
from astropy.timeseries import LombScargle
import astropy.units as u
from tqdm import tqdm  
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

def TransitOverview(id):
    datasets = lk.search_lightcurve(id)
    num_datasets = len(datasets)

    if num_datasets == 0:
        print(f"No datasets found for TIC ID {id}.")
        return None

    # Grid 
    cols = 5
    rows = math.ceil(num_datasets / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(20, rows * 2))
    axes = axes.flatten()

    # progress bar
    for i in tqdm(range(num_datasets), desc="Processing datasets", unit="dataset"):
        data_raw = datasets[i].download()
        time_raw = data_raw.time.value
        flux_raw = data_raw.flux.value

        axes[i].scatter(time_raw, flux_raw, color='#363636', marker='.')
        axes[i].set_xticks([])
        axes[i].set_yticks([])
        axes[i].set_title(f"Set # {i + 1}")

    # Hide unused axes 
    for j in range(num_datasets, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

    return fig, num_datasets

def TransitParticular(id, set_no):
    data = lk.search_lightcurve(id)[set_no-1].download()

    real_time = data.time.value
    real_flux = np.array(data.flux.value)
    real_flux_err = np.array(data.flux_err.value)

    fig = plt.figure(figsize=(10, 6))

    plt.errorbar(real_time, real_flux, real_flux_err, ecolor='gray', color='black', fmt = '.')
    plt.xlabel('Time (in days)')
    plt.ylabel('Normalized Flux')
    plt.show()

def PeriodogramOverview(id):
    
    datasets = lk.search_lightcurve(id)
    num_datasets = len(datasets)

    # Grid
    cols = 5  
    rows = math.ceil(num_datasets / cols)

    # progress bar
    with tqdm(total=num_datasets, desc="Processing datasets") as pbar:
        
        fig, axes = plt.subplots(rows, cols, figsize=(20, 2 * rows)) 
        axes = axes.flatten() 

        for i, result in enumerate(datasets):
            
            data = result.download()
            if data is None:
                print(f"Skipping dataset {i+1} due to download issues.")
                pbar.update(1)
                continue

            # periodogram
            pdg = data.to_periodogram()

            # Plot the periodogram 
            ax = axes[i]
            pdg.plot(ax=ax, color="#363636")  
            ax.legend().remove()  
            ax.set_title(f"Set # {i+1}")

            # Update the progress bar
            pbar.update(1)

        # Hide unused axes
        for j in range(num_datasets, len(axes)):
            axes[j].axis('off')

        plt.tight_layout()
        plt.show()

def PeriodogramParticular(id, set_no):
    data = lk.search_lightcurve(id)[set_no-1].download()

    # Periodogram
    pdg = data.to_periodogram()
    period = pdg.period_at_max_power.value

    # Plot the periodogram with the title inside the plot
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    pdg.plot(ax=ax)
    ax.set_title(f"Period: {period:.4f} days", fontsize=12, color="#363636") 
    plt.show()

