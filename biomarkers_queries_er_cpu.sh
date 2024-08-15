#!/bin/sh

#SBATCH --job-name=biomarkers_prompts_er
#SBATCH --output=out/biomarkers_prompts_er_%j.out

#SBATCH --time=36:00:00     # walltime

#SBATCH -p gpu # partition
#SBATCH -c 20 # number of cores
#SBATCH --mem=200G # RAM needed

source /home/exacloud/gscratch/OCTRI_AI_NLP/haglers/env/lmql-env/bin/activate
module load gcc/13.2.0
export LD_LIBRARY_PATH="/home/exacloud/software/spack/opt/spack/linux-centos7-ivybridge/gcc-10.2.0/gcc-13.2.0-jniuawgyfwcighxcd6ityb3olkizzigw/lib64:$LD_LIBRARY_PATH"

#DATA="/home/exacloud/gscratch/OCTRI_AI_NLP/haglers/testing_data/source_data"
DATA="/home/exacloud/gscratch/OCTRI_AI_NLP/haglers/training_data/source_data"
KEYWORDS="/home/exacloud/gscratch/OCTRI_AI_NLP/haglers/testing_data/BreastCancerPathology.keywords.txt"
MODE_ER="ER"
MODEL="/home/exacloud/gscratch/OCTRI_AI_NLP/gguf/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
PICKLE_ER="/home/exacloud/gscratch/OCTRI_AI_NLP/haglers/pkl/breast_cancer_biomarkers_er.pkl"
PORT=8080
SCRIPT="/home/exacloud/gscratch/OCTRI_AI_NLP/haglers/biomarkers_prompts/biomarkers_prompts.py"
TOKENIZER="mistralai/Mistral-7B-Instruct-v0.1"

#readonly PORT=$(/usr/local/bin/get-open-port.py)
#echo "Using port ${PORT}"

srun -c 20 --mem-per-cpu=10G --exclusive python3 $SCRIPT --data $DATA --keywords $KEYWORDS --mode $MODE_ER --model $MODEL --pickle $PICKLE_ER --port $PORT --tokenizer $TOKENIZER
