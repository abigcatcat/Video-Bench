import os
import importlib
from pathlib import Path
from itertools import chain
from .utils import save_json, load_json, get_prompt_from_filename

class HABench(object):
    def __init__(self, full_info_dir, output_path, config_path):
        """
        Initialize VBench evaluator
        
        Args:
            full_info_dir (str): Path to the full info JSON file
            output_path (str): Directory to save evaluation results
            config_path (str): Path to configuration file
        """
        self.full_info_dir = full_info_dir  
        self.output_path = output_path
        self.config_path = config_path
        self.config = load_json(config_path)
        os.makedirs(self.output_path, exist_ok=True)

    def build_full_dimension_list(self):
        """Return list of all available evaluation dimensions"""
        return [
           "aesthetic_quality", "imaging_quality", "temporal_consistency", "motion_effects", 
           "color", "object_class", "scene", "action", "overall_consistency"
        ]
    
    def check_dimension_requires_extra_info(self, dimension_list):
        """Check if any dimension requires extra information"""
        VideoTextConsistency_dimensions = ['color', 'object_class', 'scene', 'action', 'overall_consistency']
        for dim in dimension_list:
            if dim in VideoTextConsistency_dimensions:
                return True
        return False
    
    def build_full_info_json(self, videos_path, name, dimension_list, prompt_list=[], special_str='', verbose=False, mode='vbench_standard', **kwargs):
        """Build full info JSON file containing video paths and prompts"""
        cur_full_info_list = []
        
        if mode == 'custom_input':
            self.check_dimension_requires_extra_info(dimension_list)
            if os.path.isfile(videos_path):
                # Single video file
                model_name = os.path.basename(os.path.dirname(videos_path))
                prompt = get_prompt_from_filename(videos_path) if not prompt_list else prompt_list[videos_path]
                videos_dict = {model_name: os.path.abspath(videos_path)}
                cur_full_info_list = [{
                    "prompt_en": prompt,
                    "dimension": dimension_list,
                    "videos": videos_dict
                }]
            else:
                # Directory containing videos
                video_names = os.listdir(videos_path)
                videos_by_prompt = {}

                # Group videos by prompt
                for filename in video_names:
                    if Path(filename).suffix.lower() not in ['.mp4', '.gif', '.jpg', '.png']:
                        continue
                        
                    video_path = os.path.abspath(os.path.join(videos_path, filename))
                    model_name = os.path.basename(os.path.dirname(video_path))
                    prompt = get_prompt_from_filename(filename)
                    if prompt_list:
                        prompt = prompt_list.get(video_path, prompt)
                    
                    if prompt not in videos_by_prompt:
                        videos_by_prompt[prompt] = {}
                    videos_by_prompt[prompt][model_name] = video_path

                # Create info list entries
                for prompt, videos in videos_by_prompt.items():
                    cur_full_info_list.append({
                        "prompt_en": prompt,
                        "dimension": dimension_list,
                        "videos": videos
                    })

        else:
            # Standard mode using benchmark data
            full_info_list = load_json(self.full_info_dir)
            
            for prompt_dict in full_info_list:
                if set(dimension_list) & set([prompt_dict["dimension"]]):
                    prompt = prompt_dict['prompt']
                    # 为每个提示词创建3个视频的条目
                    for idx in range(3):  # 0, 1, 2
                        videos_dict = {}
                        for model in ['cogvideox5b', 'kling', 'gen3', 'videocrafter2', 'pika', 'show1', 'lavie']:
                            video_path = os.path.join(
                                prompt_dict['dimension'],
                                model,
                                f"{prompt}_{idx}.mp4"
                            )
                            videos_dict[model] = os.path.join(videos_path, video_path)
                        
                        cur_full_info_list.append({
                            "prompt_en": prompt,
                            "dimension": dimension_list,
                            "videos": videos_dict
                        })

        cur_full_info_path = os.path.join(self.output_path, name+'_full_info.json')
        save_json(cur_full_info_list, cur_full_info_path)
        print(f'Evaluation meta data saved to {cur_full_info_path}')
        return cur_full_info_path

    def evaluate_dimension(self, dimension, videos_path, name, dimension_list, prompt_list, mode, **kwargs):
        """Evaluate a single dimension by importing and running its module"""
        # 只传入当前维度
        cur_dimension_list = [dimension]
        
        cur_full_info_path = self.build_full_info_json(
            videos_path=videos_path,
            name=name,
            dimension_list=cur_dimension_list,
            prompt_list=prompt_list,
            mode=mode,
            **kwargs
        )

        try:
            VideoTextConsistency_dimensions = ['color', 'object_class', 'scene', 'action', 'overall_consistency']
            static_dimensions = ['aesthetic_quality', 'imaging_quality']
            dynamic_dimensions = ['temporal_consistency', 'motion_effects']

            if dimension in VideoTextConsistency_dimensions:
                from .VideoTextConsistency import eval
                from .prompt_dict import prompt
                results = eval(self.config, prompt[dimension], dimension, cur_full_info_path)
            elif dimension in static_dimensions:
                from .staticquality import eval
                from .prompt_dict import prompt
                results = eval(self.config, prompt[dimension], dimension, cur_full_info_path)
            elif dimension in dynamic_dimensions:
                from .dynamicquality import eval
                from .prompt_dict import prompt
                results = eval(self.config, prompt[dimension], dimension, cur_full_info_path)
            else:
                raise ValueError(f"Unknown dimension: {dimension}")
            
            return results
            
        except Exception as e:
            print(f"Error evaluating {dimension}: {e}")
            return {'error': str(e)}

    def evaluate(self, videos_path, name, dimension_list=None, prompt_list=[], mode='vbench_standard', **kwargs):
        """
        Run evaluation on specified dimensions
        
        Args:
            videos_path (str): Path to video files
            name (str): Name for this evaluation run
            dimension_list (list): List of dimensions to evaluate
            prompt_list (dict): Dictionary mapping video paths to prompts
            mode (str): Evaluation mode ('vbench_standard' or 'custom_input')
            **kwargs: Additional arguments
        """
        # Use default dimension list if none provided
        if dimension_list is None:
            dimension_list = self.build_full_dimension_list()
            print(f'Using default dimension list: {dimension_list}')
        
        # Evaluate each dimension
        results = {}
        for dimension in dimension_list:
            print(f"Evaluating {dimension}...")
            dimension_results = self.evaluate_dimension(
                dimension=dimension,
                videos_path=videos_path,
                name=name,
                dimension_list=dimension_list,
                prompt_list=prompt_list,
                mode=mode,
                **kwargs
            )

            # 为每个维度创建输出目录
            dimension_output_dir = os.path.join(self.output_path, dimension)
            os.makedirs(dimension_output_dir, exist_ok=True)
            
            # 保存结果
            VideoTextConsistency_dimensions = ['color', 'object_class', 'scene', 'action', 'overall_consistency']
            if dimension in VideoTextConsistency_dimensions:
                save_json(dimension_results['history'], os.path.join(dimension_output_dir, f'{name}_history_results.json'))
                save_json(dimension_results['updated_description'], os.path.join(dimension_output_dir, f'{name}_updated_description_results.json'))
                save_json(dimension_results['score'], os.path.join(dimension_output_dir, f'{name}_score_results.json'))
            else:
                save_json(dimension_results['score'], os.path.join(dimension_output_dir, f'{name}_score_results.json'))
            
            results[dimension] = dimension_results
        
        return results
