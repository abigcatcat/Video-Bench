import os
from openai import OpenAI
import openai
from .utils import Video_Dataset
import json
import logging
from tenacity import retry, stop_after_attempt, wait_random_exponential

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def call_api(client, messages, model):
    """调用 OpenAI API 的函数，包含重试机制"""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def eval(config, prompt, dimension, cur_full_info_path):
    """
    Evaluate videos using OpenAI API
    Args:
        config: configuration dictionary
        prompt: prompt template
        dimension: evaluation dimension name
    Returns:
        dict: containing evaluation scores
    """
    # 设置日志
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(config[f'log_path_{dimension}'])
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    client = OpenAI(
        api_key = config['GPT4o_API_KEY'],
        base_url = config['GPT4o_BASE_URL']
    )
    MODEL = "gpt-4o-2024-08-06"

    results = {}
    dataset = Video_Dataset(cur_full_info_path)
    
    l1 = list(range(0, len(dataset)))
    for i in l1:
        try:
            logger.info(f'Processing video {i}...')
            data = dataset[i]
            frames = data['frames']
            prompten = data['prompt']
            
            # 构建包含所有模型帧的消息
            model_frames_content = []
            for model_name, model_frames in frames.items():
                model_frames_content.extend([
                    f"\n{len(model_frames)} frames from {model_name}\n",
                    *map(lambda x: {"type": "image_url", 
                                  "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, 
                         model_frames)
                ])

            messages = [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user", 
                    "content": [
                        f"These are the frames from the video. The prompt is '{prompten}'.",
                        *model_frames_content
                    ]
                }
            ]

            response = call_api(client, messages, MODEL)
            results[str(i)] = response
            
            logger.info(f'Successfully evaluated video {i}')
            logger.debug(f'Response for video {i}: {response}')
            
        except Exception as e:
            logger.error(f'Error processing video {i}: {str(e)}')
            results[str(i)] = f'Error: {str(e)}'

    return {
        'score': results
    }