# Calculate accessibility change from new cycling projects

This code calculates the change in destination accessibility for each origin in Toronto as a result of an input list of cycling infrastructure projects. 

## Inputs:

- A list of projects -- a list of integer IDs for projects that correspond to the arterial road segments in `proj2artid`, i.e. project 0 is the 0th indexed element in `proj2artid`. Alternatively projects are listed as network edges in `args['projects']`.
- `args.pkl` -- object containing:
	- destination values for each DA (indexed by centroid node ID)
    	- graph object for full city network (G) and reachable with current infrastructure (G_curr)

## Returns:

- change in destination accessibility for each origin, mapped to DAid in a csv


