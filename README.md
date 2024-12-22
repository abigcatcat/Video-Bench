# Video-Bench: Human Preference Aligned Video Generation Benchmark

*Video-Bench is a benchmark tool designed to systematically leverage MLLMs across all dimensions relevant to video generation assessment in generative models. By incorporating few-shot scoring and chain-of-query techniques, Video-Bench provides a structured, scalable approach to generated video evaluation.*

<a href="https://arxiv.org/pdf/xxx.pdf" alt="paper"><img src="https://img.shields.io/badge/ArXiv-xxx-FAA41F.svg?style=flat" /></a>
<a href="https://videobench.github.io/VideoBench-project/" alt="demo"><img src="https://img.shields.io/badge/Demo-VideoBench-orange" /></a> 
<a href="https://medium.com/xxx" alt="blog"><img src="https://img.shields.io/badge/Medium-Blog-green" /></a> 
<a href="https://zhuanlan.zhihu.com/p/xxx" alt="zhihu"><img src="https://img.shields.io/badge/Zhihu-知乎-blue" /></a> 
<a href="https://www.youtube.com/watch?v=xxx" alt="video"><img src="https://img.shields.io/badge/Video-YouTube-purple" /></a>
<a href="https://xxx" alt="twitter"><img src="https://img.shields.io/badge/Post-Twitter-1DA1F2" /></a>

 
![Multi-Modal](https://img.shields.io/badge/Task-Vision--Perception-red) 
![Foundation-Model](https://img.shields.io/badge/Task-Video--Understanding-red) 
![Foundation-Model](https://img.shields.io/badge/Task-Video--Generation-red) 
![Video-Understanding](https://img.shields.io/badge/Task-Video--Evaluation-red) 
![Video-Generation](https://img.shields.io/badge/Task-Video--Benchmark-red) 
![Video-Recommendation](https://img.shields.io/badge/Task-MLLM--Application-red) 
![Video-Recommendation](https://img.shields.io/badge/Task-Human--Preference--Learning-red) 
![Video-Recommendation](https://img.shields.io/badge/Dataset-Human--Annotation-red) 

[⭐Overview](#Overview) |
[📒Benchmark](#Benchmark) |
[🗃️Evaluation](#Evaluation) |
[🛠️Installation](#Installation) |
[🚀Usage](#Usage) |
[🤗Video Understanding Meets Recommender Systems](#Video_Understanding_Meets_Recommender_Systems) |
[📭Citation](#Citation) |)

# Overview

<div align=center><img src="https://github.com/Video-Bench/Video-Bench/blob/main/figures/videobench.png"/></div>

# Benchmark

(A Table to be filled)

# Evaluation

**Multi-Dimensional Assessment (add description and scale to the below table)**:
| Dimension  |  Code Path |
|---|---|
| Image Quality  |  `Video-Bench/staticquality.py` |
| Aesthetic Quality  | `Video-Bench/staticquality.py`  |
| Temporal Consistency | `Video-Bench/dynamicquality.py`  |
| Motion Effects | `Video-Bench/dynamicquality.py` |
| Object-Class Consistency | `Video-Bench/VideoTextConsistency.py` |
| Video-Text Consistency | `Video-Bench/VideoTextConsistency.py` |
| Color Consistency | `Video-Bench/VideoTextConsistency.py` |
| Action Consistency | `Video-Bench/VideoTextConsistency.py` |
| Scene Consistency |`Video-Bench/VideoTextConsistency.py` |


**Tested Models (a table with name, year, paper link, github link, accepted paper)**:
  - Lavie
  - Pika
  - Show-1
  - VideocrAfter2
  - CogVideoX5B
  - Kling
  - Gen3


# Installation

## Installation Requirements
- Python >= 3.8
- OpenAI API access
   Update your OpenAI API keys in `config.json`:
   ````json
   {
       "GPT4o_API_KEY": "your-api-key",
       "GPT4o_BASE_URL": "your-base-url",
       "GPT4o_mini_API_KEY": "your-mini-api-key",
       "GPT4o_mini_BASE_URL": "your-mini-base-url"
   }
   ````

## Pip Installation

   ````bash
   pip install xxx
   ````

## Git Clone

   ````bash
   git clone https://github.com/yourusername/Video-Bench.git
   cd Video-Bench
   conda env create -f environment.yml
   conda activate Video-Bench
   ````

## Download From Huggingface

   ````bash
   wget https://huggingface.co/xxx/resolve/main/pytorch_model.bin -O ./pytorch_model.bin
   ````
   or
   ````bash
   curl -L https://huggingface.co/xxx/resolve/main/pytorch_model.bin -o ./pytorch_model.bin
   ````

## Data Preparation

Please organize your data according to the following structure:
```bash
/Video-Bench/data/
├── color/                           # 'color' dimension videos
│   ├── cogvideox5b/
│   │   ├── A red bird_0.mp4
│   │   ├── A red bird_1.mp4
│   │   └── ...
│   ├── lavie/
│   │   ├── A red bird_0.mp4
│   │   ├── A red bird_1.mp4
│   │   └── ...
│   ├── pika/
│   │   └── ...
│   └── ...
│
├── object_class/                    # 'object_class' dimension videos
│   ├── cogvideox5b/
│   │   ├── A train_0.mp4
│   │   ├── A train_1.mp4
│   │   └── ...
│   ├── lavie/
│   │   └── ...
│   └── ...
│
├── scene/                           # 'scene' dimension videos
│   ├── cogvideox5b/
│   │   ├── Botanical garden_0.mp4
│   │   ├── Botanical garden_1.mp4
│   │   └── ...
│   └── ...
│
├── action/                          # 'action' 'temporal_consistency' 'motion_effects' dimension videos
│   ├── cogvideox5b/
│   │   ├── A person is marching_0.mp4
│   │   ├── A person is marching_1.mp4
│   │   └── ...
│   └── ...
│
└── overall_consistency/             # 'overall consistency' 'imaging_quality' 'aesthetic_quality' dimension videos
    ├── cogvideox5b/
    │   ├── Close up of grapes on a rotating table._0.mp4
    │   └── ...
    ├── lavie/
    │   └── ...
    ├── pika/
    │   └── ...
    └── ...
```
# Usage
Run the following command to evaluate the dimension you want to evaluate:
   ````bash
   python evaluate.py \
    --dimension $DIMENSION \
    --videos_path ./data/{dimension} \
    --config_path ./config.json/
   ````

# Citation
If you use our dataset, code or find Video-Bench useful, please cite our paper in your work as:

```bib
@article{ni2023content,
  title={Video-Bench: Human Preference Aligned Video Generation Benchmark},
  author={Han, Hui and Li, Siyuan and Chen, Jiaqi and Yuan, Yiwen and Wu, Yuling and Leong, Chak Tou and Du, Hanwen and Fu, Junchen and Li, Youhua and Zhang, Jie and Zhang, Chi and Li, Li-jia and Ni, Yongxin},
  journal={arXiv preprint arXiv:xxx},
  year={2024}
}
```
