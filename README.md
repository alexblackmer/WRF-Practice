# WRF-Practice
This is a partial codebase for the WRF practice I produced during my Numerical Weather Prediction class at the University of Utah.
Only the driving namelist and batch files are included due to storage restraints.
## Case

## Workflow
Here is a step-by-step guide for running the WRF model with my code.
Start with WRF Preprocessing System (WPS), run WRF model, and post-process with wrf-python.
### WPS:
1. Edit namelist.wps to preferred domain configuration
2. Link initial conditions data to WPS
  > ./link_grib.csh /path/to/your/data/*
3. Run WPS script
  * In this case, run batch script
  > sbatch run_wps
4. Use ncl to view domains
  > module load ncl \
  > ncl util/plotgrids_new.ncl
5. Check SLURM error and output files to ensure model 
6. Move to ../run directory
### WRF Run:
7. Change namelist.input to reflect the following
  * Domain info from namelist.wps
  * Physics schemes
8. Link WPS files to WRF run
  > ln –s ../WPS/met_em* .
9. Run WRF real batch script
  > sbatch run_real
  * Check SLURM output files for errors
10. Run WRF final batch script
  > sbatch run_wrf
  * Check SLURM  output file for errors
### Post-Processing:
11. Use ncview to view WRF output
  > 'module load ncview'
12. Develop wrf-python scripts for better visualizations
