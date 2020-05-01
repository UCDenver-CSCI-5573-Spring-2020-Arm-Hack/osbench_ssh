# Import the scripts
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt

opti = pd.read_csv('./edge_log.txt', names=['Model', 'otime'])
rasp = pd.read_csv('./edge_log_arm.txt', names=['Model', 'rtime'])

def read_time(x):
    if x < 60 :
        return str(round(x, 3)) + " Seconds"
    else:
        return str(round(x/60, 1)) + " Minutes"



data = pd.merge(opti, rasp, on='Model')
data['Difference'] =  round(data['rtime'] / data['otime']).apply(int).apply(str) + " X longer"

data['RasPi Zero'] = data.rtime.apply(read_time)
data['Optiplex'] = data.otime.apply(read_time)

print(data[['Model', 'Optiplex', 'RasPi Zero', 'Difference']])
data[['Model', 'Optiplex', 'RasPi Zero', 'Difference']].to_csv('edge_tables.csv')

exit(0)

round(rasp.rtime, 3)
round(opti.otime, 3)
data = pd.concat([opti, rasp])
data.reset_index(inplace = True, drop=True)
data.time / 60

data['Iteration'] = data.index
data['Priority'] = data['nice'].apply(lambda x: 'Nice' if x == 'so nice' else 'Not Nice')
data['metric'] = data['metric'].apply(lambda x: 
        'Allocate/free 1000000 memory chunks' if x == 'Allocate/free 1000000 memory chunks (4-128 bytes)' else x)
data.columns
data.loc[1].T

sea.set_palette("Dark2")
for i, met in enumerate(data.metric.unique()):
    plt.clf()
    plt.figure(figsize=(4,3.5))
    plt.subplots_adjust(bottom=0.15, left=0.18)
    plot = sea.boxplot(y='measure', x='GPU Memory', hue = 'Priority', data=data[data.metric == met])
    plot.set_title(met)
    yl = data[data.metric == met]['units'].values[0] + "  <Lower is Better>"
    plot.set_ylabel(yl)
    plot.figure.savefig("osbench_" + str(i) + ".png", transparent=True)

plt.close('all')

plt.clf()
plt.figure(figsize=(8,5))
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
    plt.figure(figsize=(5,4))
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

