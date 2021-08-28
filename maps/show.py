import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

grid = np.zeros([4,5])
grid[1:-1, 1:-1] = 1

plt.imshow(grid, cmap = "gray")
plt.show()

