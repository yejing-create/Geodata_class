import numpy as np
import simplempi

smpi = simplempi.simpleMPI()
# get the rank
comm = smpi.comm
rank = smpi.comm.rank

# initialize pi to 0
pi_part = 0

# set the number of terms in the sum
N = int(3200)


# loop from 1 to N, adding terms to pi
# such that pi ~= 4*(1 - 1/3 + 1/5 - 1/7 + 1/9 ... -(-1)**n / (2n - 1))
smpi.pprint("Starting loop")
for n in smpi.parfor(range(1,N)):
    if n == 1:
        term = 1
    else:
        term = -((-1)**n) / (2*n - 1)
    pi_part = pi_part + term
smpi.pprint("Ending loop")
    
# use gather to collect all the parts
pi_parts = comm.gather(pi_part, root = 0)



# print the answer
if rank == 0:
    # sum the result
    pi = sum(pi_parts)

    # multiply pi by four to get the final answer
    pi = 4 * pi
    
    print(f"pi = {pi:2.7f}")
    print(f"np.pi = {np.pi:2.7f}")