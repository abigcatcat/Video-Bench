# Video-Bench: Human Preference Aligned Video Generation Benchmark

=======
*Video-Bench is a benchmark tool designed to systematically leverage MLLMs across all dimensions relevant to video generation assessment in generative models. By incorporating few-shot scoring and chain-of-query techniques, Video-Bench provides a structured, scalable approach to generated video evaluation.*
>>>>>>> f5a97cb267f2dbec3cad56b786871ac4aec9866d

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
[📝Literature](#Literature) |
[📒Leaderboard](#Leaderboard) |
[🤗HumanAlignment](#HumanAlignment) |
[🛠️Installation](#Installation) |
[🗃️Preparation](#Preparation) |
[⚡Instructions](#Instructions) |
[🚀Usage](#Usage) |
[📭Citation](#Citation)

# Overview

<div align=center><img src="https://github.com/Video-Bench/Video-Bench/blob/main/figures/videobench.png"/></div>

# Literature

## Video Generation Models

(A Table to be filled, providing name, year, paper link, github link, accepted conference)

## Video Generation Evaluation Methods

(A Table to be filled, providing name, year, paper link, github link, accepted conference)

# Leaderboard

| Model            | Imaging Quality | Aesthetic Quality | Temporal Consist. | Motion Effects | Avg Rank | Video-text Consist. | Object-class Consist. | Color Consist. | Action Consist. | Scene Consist. | Avg Rank | Overall Avg Rank |
|------------------|-----------------|-------------------|--------------------|----------------|----------|----------------------|-----------------------|----------------|-----------------|----------------|----------|------------------|
| Cogvideox [57]   | 3.87            | 3.84              | 4.14               | 3.55           | 3.00     | **4.62**             | 2.81                 | **2.92**        | 2.81            | **2.93**       | **1.60**  | 2.22             |
| Gen3 [42]        | **4.66**        | **4.44**          | **4.74**           | **3.99**       | **1.00** | 4.38                 | 2.81                 | 2.87            | 2.59            | **2.93**       | 2.40      | **1.78**         |
| Kling [24]       | 4.26            | 3.82              | 4.38               | 3.11           | 2.75     | 4.07                 | 2.70                 | 2.81            | 2.50            | 2.82           | 4.60      | 3.78             |
| VideoCrafter2 [5] | 4.08            | 3.85              | 3.69               | 2.81           | 3.75     | 4.18                 | **2.85**             | 2.90            | 2.53            | 2.78           | 2.80      | 3.22             |
| LaVie [52]       | 3.00            | 2.94              | 3.00               | 2.43           | 7.00     | 3.71                 | 2.82                 | 2.81            | 2.45            | 2.63           | 5.00      | 5.88             |
| PiKa-Beta [38]   | 3.78            | 3.76              | 3.40               | 2.59           | 5.50     | 3.78                 | 2.51                 | 2.52            | 2.25            | 2.60           | 6.80      | 6.22             |
| Show-1 [60]      | 3.30            | 3.28              | 3.90               | 2.90           | 5.00     | 4.21                 | 2.82                 | 2.79            | 2.53            | 2.72           | 3.80      | 4.33             |

**Notes**:
- Higher scores indicate better performance.
- The best score in each dimension is highlighted in **bold**.

# HumanAlignment

| Metrics     | Benchmark      | Imaging Quality | Aesthetic Quality | Temporal Consist. | Motion Effects | Video-text Consist. | Object-class Consist. | Color Consist. | Action Consist. | Scene Consist. |
|-------------|----------------|------------------|--------------------|--------------------|----------------|----------------------|-----------------------|----------------|-----------------|----------------|
| MUSIQ [21]  | VBench [19]    | 0.363           | -                  | -                  | -              | -                    | -                     | -              | -               | -              |
| LAION       | VBench [19]    | -               | 0.446              | -                  | -              | -                    | -                     | -              | -               | -              |
| CLIP [40]   | VBench [19]    | -               | -                  | 0.260              | -              | -                    | -                     | -              | -               | -              |
| RAFT [48]   | VBench [19]    | -               | -                  | -                  | 0.329          | -                    | -                     | -              | -               | -              |
| Amt [28]    | VBench [19]    | -               | -                  | -                  | 0.329          | -                    | -                     | -              | -               | -              |
| ViCLIP [53] | VBench [19]    | -               | -                  | -                  | -              | -                    | 0.445                 | -              | -               | -              |
| UMT [27]    | VBench [19]    | -               | -                  | -                  | -              | -                    | -                     | -              | 0.411           | -              |
| GRiT [54]   | VBench [19]    | -               | -                  | -                  | -              | -                    | -                     | -              | -               | -              |
| Tag2Text [16]| VBench [19]   | -               | -                  | -                  | -              | 0.469                | 0.545                 | -              | -               | 0.422          |
| ComBench [46]| ComBench [46] | -               | -                  | -                  | -              | 0.611                | 0.696                 | 0.633          | 0.633           | 0.631          |
| **Ours**    | **Ours**       | **0.733**       | **0.702**          | **0.402**          | **0.514**      | **0.735**            | **0.750**             | **0.718**      | **0.733**       | **0.733**      |

**Notes**:
- Higher scores indicate better performance.
- The best score in each dimension is highlighted in **bold**.


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

- Install with pip
   ````bash
   pip install HAbench
   ````
- Install with conda
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

# Preparation

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

# Instructions

**Video-Bench enables video generation assessment from multiple dimensions (add description and scale to the below table)**:
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
