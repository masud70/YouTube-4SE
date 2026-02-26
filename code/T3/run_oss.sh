#!/bin/bash
#SBATCH --job-name=gptoss
#SBATCH --output=logs/gptoss.%j.out
#SBATCH --error=logs/gptoss.%j.err
#SBATCH --mail-user=mazumdmm@myumanitoba.ca
#SBATCH --mail-type=END,FAIL

#SBATCH --time=06:00:00
#SBATCH --gres=gpu:h100:2
#SBATCH --cpus-per-task=4
#SBATCH --mem=20G

set -euo pipefail
echo "Job started on $(hostname) at $(date)"

cd /home/mazumdmm/projects/def-shaiful/masud/YouTube/YouTube-4SE/code/T3
source .venv/bin/activate

srun python chat_llm.py

echo "Job finished at $(date)"