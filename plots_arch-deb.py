# Import the scripts
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt

data1 = pd.read_csv('./gpu_mem_16_run_4-29_arch.csv')
data1["OS"] = "Arch"
data2 = pd.read_csv('./gpu_mem_16_run_4-29_deb.csv')
data2["OS"] = "Raspbian"

data = pd.concat([data1, data2])
data.reset_index(inplace = True, drop=True)
data['Iteration'] = data.index
data['Priority'] = data['nice'].apply(lambda x: 'Nice' if x == 'so nice' else 'Not Nice')
data['metric'] = data['metric'].apply(lambda x: 
        'Allocate/free 1000000 memory chunks' if x == 'Allocate/free 1000000 memory chunks (4-128 bytes)' else x)
data.columns
data.loc[1].T

sea.set_palette("Dark2")
sea.set_palette(sea.color_palette()[4:])
for i, met in enumerate(data.metric.unique()):
    plt.clf()
    plt.figure(figsize=(4,3.5))
    plt.subplots_adjust(bottom=0.15, left=0.18)
    plot = sea.boxplot(y='measure', x='OS', hue = 'Priority', data=data[data.metric == met])
    plot.set_title(met)
    yl = data[data.metric == met]['units'].values[0] + "  <Lower is Better>"
    plot.set_ylabel(yl)
    plot.figure.savefig("osbench_" + str(i) + "_OS.png", transparent=True)

plt.close('all')

plt.clf()
plt.figure(figsize=(8,5))
plot = sea.lineplot(
        y='heat', 
        x='Iteration', 
        hue="Priority",  
        style='OS', 
        data=data
        )
plot.set_title("Temperature Over Testing Cycle")
plt.savefig("heat_vs_time_OS.png", transparent=True)

for i, met in enumerate(data.metric.unique()):
    plt.clf()
    plt.figure(figsize=(5,4))
    plot = sea.scatterplot(
            y='heat', 
            x='measure', 
            style='OS', 
            hue='Priority',  
            data=data[data["metric"] == met]
            )
    plot.set_title(met+" (Speed vs Temperature)")
    xl = data[data.metric == met]['units'].values[0] + "  <Lower is Better>"
    plot.set_xlabel(xl)
    plot.set_ylabel("Temperature (Celsius)")
    plt.savefig("heat_vs_speed_" + str(i) + "_OS.png", transparent=True)

plt.clf()
plot = sea.scatterplot(
       y='heat', 
       x='volt', 
       data=data
       )
plt.savefig("heat_vs_volt_OS.png", transparent=True)

