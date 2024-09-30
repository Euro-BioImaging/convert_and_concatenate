source /g/cba/miniconda3/etc/profile.d/conda.sh \
module load Mamba \
conda activate ome_zarr_pyramid_slurm \
pip install git+https://github.com/Euro-BioImaging/ome_zarr_pyramid.git@slurm

example: \
`convert_and_concatenate /g/ebioimage/oezdemir/data/yannick/F227_WT2wk_run3_5nm_aligned /g/ebioimage/oezdemir/data/yannick/results12`
