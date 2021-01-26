import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd

fig= plt.figure()
ax = plt.gca()

# d = {'hello':5,'bar':10}

# df = pd.DataFrame(d.items(), columns=['Emotion', 'Count'])

def animate_frame(i):
    labels, values = zip(*counter.items())
    indexes = np.arange(len(labels))
    width = 1
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    # return df['Emotion'].value_counts().plot(ax=ax)

animation = FuncAnimation(fig, func=animate_frame, interval=1000)
plt.show()