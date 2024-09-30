source /g/cba/miniconda3/etc/profile.d/conda.sh
module load Mamba
conda activate ome_zarr_pyramid_slurm
pip install git+https://github.com/Euro-BioImaging/ome_zarr_pyramid.git@slurm
