import os
import glob
import re
import numpy as np
import pandas as pd
from mpi4py import MPI  # Requires: pip install mpi4py

def process_cutoff(root_folder, folder_name, output_dir):
    """
    Reads masks for a single cutoff folder, handles time gaps,
    strictly ignores 'selected_points.npy', and saves to Excel.
    """
    cutoff_id = folder_name
    # Since we are inside the root, we look directly into the numbered folder
    mask_folder = os.path.join(root_folder, folder_name, "mask")
    
    if not os.path.exists(mask_folder):
        return None

    # 1. Collect .npy files
    npy_files = glob.glob(os.path.join(mask_folder, "*.npy"))
    file_data = []
    
    for f_path in npy_files:
        f_name = os.path.basename(f_path)
        
        # --- PROTECTION 1: EXPLICITLY IGNORE 'selected_points.npy' ---
        if "selected_points" in f_name:
            continue
        
        # --- PROTECTION 2: REGEX VALIDATION ---
        # Matches "1990_anything.npy". 
        match = re.match(r"(\d{4})_.*\.npy", f_name)
        
        if match:
            year = int(match.group(1))
            file_data.append({'year': year, 'path': f_path})
    
    file_data.sort(key=lambda x: x['year'])
    
    if len(file_data) < 2:
        return None

    results = []

    # 2. Iterate through consecutive available files
    for i in range(len(file_data) - 1):
        t0_info = file_data[i]
        t1_info = file_data[i+1]
        
        year_start = t0_info['year']
        year_end = t1_info['year']
        
        # TIME DIFFERENCE CALCULATION (dt)
        dt = year_end - year_start
        
        # Safety check for duplicates
        if dt == 0:
            rank = MPI.COMM_WORLD.Get_rank()
            print(f"[Rank {rank}] Warning: Duplicate year {year_start} in folder {cutoff_id}. Skipping.")
            continue

        try:
            # Load Masks (Force binary 0 and 1)
            mask_t0 = (np.load(t0_info['path']) > 0).astype(int)
            mask_t1 = (np.load(t1_info['path']) > 0).astype(int)
            
            # --- CALCULATIONS ---
            diff_map = mask_t1 - mask_t0
            
            count_pos_1 = np.sum(diff_map == 1)
            count_neg_1 = np.sum(diff_map == -1)
            
            # Normalization (Total Water Pixels in Start Year)
            total_counts = np.sum(mask_t0 == 1)
            
            if total_counts == 0:
                raw_dim_pos = 0.0
                raw_dim_neg = 0.0
            else:
                raw_dim_pos = count_pos_1 / total_counts
                raw_dim_neg = count_neg_1 / total_counts
            
            # --- ANNUALIZED RATE CALCULATION (Divide by dt) ---
            yearly_erosion = raw_dim_pos / dt
            yearly_deposition = raw_dim_neg / dt
            
            migration_rate = min(yearly_erosion, yearly_deposition)
            widening_rate = yearly_erosion - yearly_deposition
            
            results.append({
                "Year Interval": f"{year_start}-{year_end}",
                "Start Year": year_start,
                "End Year": year_end,
                "Time Diff (dt)": dt,
                "Raw Dim Erosion (Total)": raw_dim_pos,
                "Raw Dim Deposition (Total)": raw_dim_neg,
                "Annualized Erosion": yearly_erosion,
                "Annualized Deposition": yearly_deposition,
                "Migration Speed (per year)": migration_rate,
                "Widening Rate (per year)": widening_rate
            })
            
        except Exception as e:
            rank = MPI.COMM_WORLD.Get_rank()
            print(f"[Rank {rank}] Error processing {cutoff_id} ({year_start}): {e}")
            continue

    if not results:
        return None

    # 3. Save to Individual Excel File
    df = pd.DataFrame(results)
    output_filename = f"Cutoff_{cutoff_id}.xlsx"
    output_path = os.path.join(output_dir, output_filename)
    
    df.to_excel(output_path, index=False)
    return f"Cutoff {cutoff_id}"


def main():
    # --- MPI INITIALIZATION ---
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # UPDATE: We use '.' to refer to the current directory
    root_folder = '.'  
    output_dir = "Analysis_Results"

    # 1. Setup (Rank 0 only checks folders)
    if rank == 0:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

    # Sync all cores
    comm.Barrier()

    # 2. Get Task List
    all_folders = []
    # We scan the current directory
    files_in_current_dir = os.listdir(root_folder)
    
    # FILTER: ONLY accept folders that are numbers (e.g. "11", "12")
    # This automatically ignores the script itself and other random files
    all_folders = [f for f in files_in_current_dir if f.isdigit()]
    all_folders.sort(key=int)

    # 3. Cyclic Distribution
    my_folders = all_folders[rank::size]

    if rank == 0:
        print(f"Starting analysis on {len(all_folders)} folders using {size} cores.")

    # 4. Processing
    count_done = 0
    for folder_name in my_folders:
        res = process_cutoff(root_folder, folder_name, output_dir)
        if res:
            count_done += 1

    # 5. Final Report
    print(f"[Rank {rank}] Finished. Processed {count_done} folders.")

if __name__ == '__main__':
    main()