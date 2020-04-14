# Import the scripts
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt

data1 = pd.read_csv('./baseline_run_3-13.csv')
data1["GPU Memory"] = "64 MB"
data1.columns
data2 = pd.read_csv('./gpu_mem_16_run_3-22.csv')
data2["GPU Memory"] = "16 MB"

data = pd.concat([data1, data2])
data.reset_index(inplace = True, drop=True)
data['Iteration'] = data.index
data['Priority'] = data['nice'].apply(lambda x: 'Nice' if x == 'so nice' else 'Not Nice')
data.columns
data.loc[1].T

sea.set_palette("Dark2")
for i, met in enumerate(data.metric.unique()):
    plt.clf()
    plot = sea.boxplot(y='measure', x='GPU Memory', hue = 'Priority', data=data[data.metric == met])
    plot.set_title(met)
    yl = data[data.metric == met]['units'].values[0] + "  <Lower is Better>"
    plot.set_ylabel(yl)
    plot.figure.savefig("osbench_" + str(i) + ".png", transparent=True)

plt.clf()
#plt.figure(figsize=(20,9))
plot = sea.lineplot(
        y='heat', 
        x='Iteration', 
        hue="Priority",  
        style='GPU Memory', 
        data=data
        )
plot.set_title("Temperature Over Testing Cycle")
plt.savefig("heat_vs_time.png", transparent=True)

for i, met in enumerate(data.metric.unique()):
    plt.clf()
    #plt.figure(figsize=(20,9))
    plot = sea.scatterplot(
            y='heat', 
            x='measure', 
            style='GPU Memory', 
            hue='Priority',  
            data=data[data["metric"] == met]
            )
    plot.set_title(met+" (Speed vs Temperature)")
    xl = data[data.metric == met]['units'].values[0] + "  <Lower is Better>"
    plot.set_xlabel(xl)
    plot.set_ylabel("Temperature (Celsius)")
    plt.savefig("heat_vs_speed_" + str(i) + ".png", transparent=True)

plt.clf()
plot = sea.scatterplot(
       y='heat', 
       x='volt', 
       data=data
       )
plt.savefig("heat_vs_volt.png", transparent=True)

