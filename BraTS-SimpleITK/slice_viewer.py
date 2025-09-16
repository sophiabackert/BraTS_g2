import numpy as np
import SimpleITK as sitk
import ipywidgets as ipyw
import matplotlib.pyplot as plt


class ImageSliceViewer3D:
    """ 
    ImageSliceViewer3D is for viewing volumetric image slices in jupyter or
    ipython notebooks. 
    
    User can interactively change the slice plane selection for the image and 
    the slice plane being viewed. 

    Argumentss:
    Volume = 3D input image as numpy array or SimpleITK image.
    figsize = default(8,8), to set the size of the figure
    cmap = default('plasma'), string for the matplotlib colormap. You can find 
    more matplotlib colormaps on the following link:
    https://matplotlib.org/users/colormaps.html
    
    """
    
    def __init__(self, volume, mask=None, figsize=(5,5), cmap='gray'):
        if isinstance(volume, sitk.Image):
            self.volume = sitk.GetArrayFromImage(volume)
        else:
            self.volume = volume.copy() 
        if isinstance(mask, sitk.Image):
            self.mask_orig = sitk.GetArrayFromImage(mask)
        elif mask is not None:
            self.mask_orig = mask.copy()
        else:
            self.mask_orig = None
        self.figsize = figsize
        self.cmap = cmap
        self.v = [np.min(volume), np.max(volume)]
        
        # Call to select slice plane
        ipyw.interact(self.view_selection, view=ipyw.ToggleButtons(
            options=['axial','coronal', 'sagittal'], value='axial', 
            description='Slice plane selection:', disabled=False,
            style={'description_width': 'initial'}))
        
    def view_selection(self, view):
        # Transpose the volume to orient according to the slice plane selection
        orient = {"coronal": [0,2,1], "sagittal": [0,1,2],"axial": [1,2,0]}
        self.vol = np.transpose(self.volume, orient[view])
        self.mask = np.transpose(self.mask_orig, orient[view]) if self.mask_orig is not None else None
        maxZ = self.vol.shape[2] - 1        
        # Call to view a slice within the selected slice plane
        ipyw.interact(self.plot_slice, 
            z=ipyw.IntSlider(value=maxZ//2, min=0, max=maxZ, step=1, continuous_update=False, 
            description='Image Slice:'))
        
    def plot_slice(self, z):
        # Plot slice for the given plane and slice
        self.fig = plt.figure(figsize=self.figsize)
        plt.imshow(self.vol[:,:,z], cmap=plt.get_cmap(self.cmap), 
            vmin=self.v[0], vmax=self.v[1], origin='lower')
        if self.mask is not None:
            mask_slice = self.mask[:,:,z]
            alphas = np.ones(mask_slice.shape) * 0.7
            alphas[mask_slice < 1] = 0
            plt.imshow(self.mask[:,:,z], cmap='jet', alpha=alphas, origin='lower')
        plt.show()
