"""
### First do this in bash:

source /g/cba/miniconda3/etc/profile.d/conda.sh
module load Mamba
conda activate ome_zarr_pyramid_slurm
pip install git+https://github.com/Euro-BioImaging/ome_zarr_pyramid.git@slurm

"""
import os, shutil, glob, fire
from pathlib import Path
from ome_zarr_pyramid.process.converters import Converter
from ome_zarr_pyramid import Aggregative
from ome_zarr_pyramid.utils import metadata_utils as metautils
from ome_zarr_pyramid.core.pyramid import Pyramid

def convert_and_concatenate(source_dir,
                            dest_dir,
                            ### func params
                            axis='z',
                            ### Metadata for the new dimension
                            new_unit = 'nm',
                            new_scale = 10,
                            ### conversion params
                            resolutions=3,
                            chunk_z=1,
                            chunk_y=1024,
                            chunk_x=1024,
                            scale_factor = None,
                            ### slurm params
                            cores = 4,
                            memory = "2GB",
                            n_jobs = 128,
                            processes = 1,
                            nanny = True,
                            overwrite = False
                            ):
    ### func params
    cvt = Converter(n_jobs = n_jobs).set_slurm_params(cores = cores, memory = memory, processes = processes)
    if overwrite:
        if (dest_dir).exists():
            if (dest_dir).is_dir():
                shutil.rmtree(dest_dir)
            elif (dest_dir).is_file():
                os.remove(dest_dir)
    ###
    cvt.to_omezarrs(source_dir,
    dest_dir/"unary",
    resolutions = resolutions,
    chunk_z = chunk_z,
    chunk_y = chunk_y,
    chunk_x = chunk_x
    )
    ###
    print("Conversions complete.")
    agg = Aggregative(n_jobs = n_jobs,
                      output_chunks = (1,1,chunk_z,chunk_y,chunk_x),
                      overwrite = overwrite,
                      rescale_output = False,
                      ).set(parallel_backend = 'loky',
                            verbose = True,
                            cores = cores,
                            memory = memory,
                            processes = processes,
                            scale_factor=scale_factor,
                            nanny = nanny,
                            syncdir=dest_dir / '.syncdir'
                            )
    output = agg.concatenate(dest_dir/"unary",
                            axis = axis,
                            out = dest_dir/"concatenated.zarr"
                            )
    print("Concatenation complete.")
    meta = metautils.MetadataUpdater()
    newunit = {"z_unit": new_unit,
               "y_unit": new_unit,
               "x_unit": new_unit
               }
    output = meta.update_units(dest_dir/"concatenated.zarr", **newunit)
    newscale = {"z_scale": new_scale,
                "y_scale": new_scale,
                "x_scale": new_scale,
                }
    output = meta.update_scales(dest_dir/"concatenated.zarr", **newscale)
    return output

# source_dir=Path("/g/ebioimage/oezdemir/data/yannick/F227_WT2wk_run3_5nm_aligned")
# dest_dir=Path("/g/ebioimage/oezdemir/data/yannick/results11")
#
# convert_and_concatenate(
#                         source_dir,
#                         dest_dir,
#                         ### func params
#                         axis='z',
#                         ### conversion params
#                         resolutions=3,
#                         chunk_z=1,
#                         chunk_y=1024,
#                         chunk_x=1024,
#                         scale_factor = None,
#                         ### slurm params
#                         cores = 16,
#                         memory = "64GB",
#                         n_jobs = 16,
#                         processes = 4,
#                         nanny = True,
#                         overwrite = False
#                         )

def convert_and_concatenate_cmd():
    _ = fire.Fire(convert_and_concatenate)
    return
