# Import the parfor function (which also initializes MPI) and pprint
from simplempi.parfor import parfor, pprint 

# Import our custom function from the other file
import generate_frame

# --- Define Static Parameters ---
input_file_path = ('/N/project/easg690_fall2025/data/ERA5/ds633.0/e5.oper.an.sfc/'
                   '202106/e5.oper.an.sfc.128_136_tcw.ll025sc.2021060100_2021063023.nc')

# We'll save the parallel output to a new directory
output_directory = 'parallel_frames_output'

# --- Define the Timestep Range ---
# Assuming you want to loop over 100 timesteps (0 to 99). Adjust this range as needed.
total_timesteps = 100
timesteps_to_process = range(total_timesteps)

# --- Parallel Loop with simplempi.parfor ---
# The parfor function transparently distributes the iterations (timesteps)
# in the 'timesteps_to_process' range across all MPI processes.
# Each process will only execute the loop body for the timesteps assigned to it.

for i in parfor(timesteps_to_process):
    # 'i' will be the timestep assigned to this processor in this iteration
    
    # Use pprint for a parallel-friendly print with rank and size information
    pprint(f"Starting to process timestep {i}...")

    # Call the imported function
    generate_frame.generate_frame(i=i, 
                                  input_file=input_file_path, 
                                  output_dir=output_directory)

    pprint(f"FINISHED processing timestep {i}.")

# The program will automatically finalize MPI after the loop completes.