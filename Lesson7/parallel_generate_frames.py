# Import the MPI-related library
from mpi4py import MPI

# Import our custom function from the other file
import generate_frame

# --- Define Static Parameters ---
# All processes need to know this information.
# This is the file you provided.
input_file_path = ('/N/project/easg690_fall2025/data/ERA5/ds633.0/e5.oper.an.sfc/'
                   '202106/e5.oper.an.sfc.128_136_tcw.ll025sc.2021060100_2021063023.nc')

# We'll save the parallel output to a new directory
output_directory = 'parallel_frames_output'

# --- MPI Setup ---
# Initialize MPI, get the "Communicator", the rank, and the total size
try:
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank() # The ID number of this specific processor
    size = comm.Get_size() # The total number of processors we are using
except Exception as e:
    print(f"Failed to initialize MPI. Is mpi4py installed? Error: {e}")
    # We can't continue if MPI fails, so exit.
    # We use sys.exit(1) to indicate an error.
    import sys
    sys.exit(1)

# --- Task Assignment ---
# This is the core logic:
# Rank 0 will process timestep 0
# Rank 1 will process timestep 1
# ...
# Rank 19 will process timestep 19
i = rank

# --- Run the Function ---
# Each processor runs this code on its own assigned timestep 'i'
print(f"MPI Rank {rank} (of {size}) starting to process timestep {i}...")

# Call the imported function
generate_frame.generate_frame(i=i, 
                              input_file=input_file_path, 
                              output_dir=output_directory)

print(f"MPI Rank {rank} FINISHED processing timestep {i}.")