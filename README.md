Installation: \
```bash
source /g/cba/miniconda3/etc/profile.d/conda.sh 
module load Mamba 
conda activate file-format-tools 
pip install git+https://github.com/Euro-BioImaging/ome_zarr_pyramid.git@slurm
pip install git+https://github.com/Euro-BioImaging/convert_and_concatenate.git
```
example: \
`convert_and_concatenate /g/ebioimage/oezdemir/data/yannick/F227_WT2wk_run3_5nm_aligned /g/ebioimage/oezdemir/data/yannick/results`
