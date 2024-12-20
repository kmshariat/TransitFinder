import numpy as np
import matplotlib.pyplot as plt
import math
import lightkurve as lk
from tqdm import tqdm  

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
        axes[i].set_title(f"{i + 1}")

    # Hide unused axes 
    for j in range(num_datasets, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

    return fig, num_datasets

TransitOverview('TIC 399860444')
