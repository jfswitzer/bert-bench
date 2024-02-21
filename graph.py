import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
df=pd.read_csv(sys.argv[1])
latencies=df["latency"]
x = np.sort(latencies)
y = 1. * np.arange(len(latencies)) / (len(latencies) - 1)
plt.plot(x, y)
plt.show()
