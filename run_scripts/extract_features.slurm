#!/bin/bash
#SBATCH --job-name=extract_features
##SBATCH --job-name=resample_demos_tw
#SBATCH -A imi@cpu
#SBATCH --qos=qos_cpu-dev
##SBATCH --qos=qos_cpu-t3 
##SBATCH --partition=gpu_p2
#SBATCH --ntasks=32
##SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
##SBATCH --hint=nomultithread
#SBATCH --time=2:00:00
##SBATCH --qos=qos_cpu-dev
##SBATCH --output=out.out
##SBATCH --error=err.err


module purge
#module load pytorch-gpu/py3/1.10.0
module load pytorch-cpu/py3/1.7.1

export ROOT_FOLDER=/gpfswork/rech/imi/usc19dv/captionRLenv/
export DATA_FOLDER=/gpfsscratch/rech/imi/usc19dv/data/UR5/
export PROCESSED_DATA_FOLDER=/gpfsscratch/rech/imi/usc19dv/data/UR5_processed/
export ROOT_DIR_MODEL=/gpfswork/rech/imi/usc19dv/mt-lightning/
export PRETRAINED_FOLDER=/gpfswork/rech/imi/usc19dv/mt-lightning/training/experiments/


#srun --wait=0 -n 32 --chdir=/gpfswork/rech/imi/usc19dv/mt-lightning feature_extraction/process_tw_data.sh /gpfsscratch/rech/imi/usc19dv/data/generated_data_processed/ --replace_existing
srun --wait=0 -n 32 --chdir=/gpfswork/rech/imi/usc19dv/mt-lightning feature_extraction/process_tw_data.sh /gpfsscratch/rech/imi/usc19dv/data/UR5_processed/ --replace_existing
#srun --wait=0 -n 16 python3 inference_mpi_owo.py 
#srun -n 320 python3 inference_mpi.py --using_model --experiment_name train_transflower_zp5_single_obj_nocol_trim_tw_single_filtered_restore_objs --pretrained_name transflower_zp5_single_obj_nocol_trim_tw_single_filtered --base_filenames_file ${PROCESSED_DATA_FOLDER}base_filenames_single_objs_filtered.txt --save_eval_results --save_sampled_traj --num_repeats 20 --restore_objects
