import numpy as np
from PIL import Image
import os
import shutil

images_alpha_dir = 'images_alpha'
images_rgb_dir = 'images_rgb'

def clear_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)

def write_slices(axis, grid, write_alpha=False, write_rgb=False):
    axes = ['X', 'Y', 'Z']
    if(not axis in axes):
        print(f'Invalid axis \'{axis}\'. Valid are X,Y or Z')
        return

    clear_dir(images_alpha_dir)
    clear_dir(images_rgb_dir)
    for i in range(grid.shape[1 + axes.index(axis)]):
        indices = [i if axis == axes[0] else slice(None),
                   i if axis == axes[1] else slice(None),
                   i if axis == axes[2] else slice(None)]
        if write_alpha:
            alpha = 255*grid[(3,          *indices)]
            Image.fromarray(alpha.astype(np.uint8), 'L').save(f'{images_alpha_dir}/{i}.png')
        if write_rgb:
            rgb   = 255*grid[(slice(0,3), *indices)].transpose()
            Image.fromarray(rgb.astype(np.uint8), 'RGB').save(f'{images_rgb_dir}/{i}.png')


grid = np.load('grid.npy')
alpha = grid[3,:,:,:]

# Set values to 0 if alpha (transparency) equal to, or less than 0
grid[:, alpha <= 0.0] = 0.0
# Also clamp them to [0,1] just to be sure
np.clip(grid, 0.0, 1.0)

print(f'grid shape: {grid.shape}')
write_slices('Y', grid, write_alpha=True, write_rgb=True)

