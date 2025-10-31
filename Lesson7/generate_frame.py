# -----------------------------------------------------------------
# All necessary imports for the function
# -----------------------------------------------------------------
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cmocean
import numpy as np
import os

# -----------------------------------------------------------------
# The function
# -----------------------------------------------------------------
def generate_frame(i, input_file, output_dir):
    """
    Generates and saves a plot for a specific timestep from a NetCDF file.
    
    Args:
        i (int): The timestep index to plot.
        input_file (str): The path to the input NetCDF file.
        output_dir (str): The directory to save the image to.
    """
    
    # 1. Prevent figures from displaying
    plt.ioff()
    
    # 2. Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # 3. Open the dataset and prepare data
    try:
        with xr.open_dataset(input_file) as ds:
            # Select the 'TCW' variable and the single timestep 'i'
            tcw = ds['TCW'].isel(time=i)
            
            # Extract coordinates
            lons = tcw['longitude']
            lats = tcw['latitude']
            
            # Get the time value for the plot title
            time_val = tcw['time'].values
            time_str = np.datetime_as_string(time_val, unit='s')
            
    except FileNotFoundError:
        print(f"Error: Input file not found at: {input_file}")
        return
    except KeyError:
        print(f"Error: Variable 'TCW' not found in the file.")
        return
    except IndexError:
        print(f"Error: Timestep index {i} is out of bounds for the file.")
        return
    except Exception as e:
        print(f"An error occurred during data loading: {e}")
        return

    # 4. Create the plot
    Bloomington_lat = 39.1653
    Bloomington_lon = -86.5264
    
    fig = plt.figure(figsize=(10, 10))
    projection = ccrs.Orthographic(central_longitude=Bloomington_lon,
                                    central_latitude=Bloomington_lat)
    ax = plt.axes(projection=projection)
    
    plot = ax.pcolormesh(lons, lats, tcw,
                         transform=ccrs.PlateCarree(),
                         cmap=cmocean.cm.rain)
    
    ax.coastlines()
    ax.gridlines()
    plt.colorbar(plot, ax=ax, orientation='vertical', label='Total Column Water (TCW)', shrink=0.8)
    ax.set_title(f'Total Column Water (TCW)\n{time_str}')
    
    # 5. Save and close the figure
    filename = f"frame_{i:03d}.png"
    output_path = os.path.join(output_dir, filename)
    
    try:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Successfully saved frame: {output_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")
    finally:
        # Close the figure to prevent memory issues
        plt.close(fig)