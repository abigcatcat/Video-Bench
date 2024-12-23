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
        
        # 定义维度映射关系
        dimension_mapping = {
            'aesthetic_quality': 'overall_consistency',
            'imaging_quality': 'overall_consistency',
            'temporal_consistency': 'action',
            'motion_effects': 'action',
            'overall_consistency': 'overall_consistency',
            'action': 'action',
            'color': 'color',
            'object_class': 'object_class',
            'scene': 'scene'
        }
        
        if mode == 'custom_input_consistency':
            self.check_dimension_requires_extra_info(dimension_list)
            
            # 获取实际的数据目录
            actual_dimensions = set(dimension_mapping[dim] for dim in dimension_list)
            
            # if os.path.isfile(videos_path):
            if os.path.isdir(videos_path) and len([f for f in os.listdir(videos_path) if os.path.isdir(os.path.join(videos_path, f))]) == 1:
                # Single video file
                model_name = os.path.basename(os.path.dirname(videos_path))
                full_name = f"{model_name}/{os.path.basename(videos_path)}"
                prompt = get_prompt_from_filename(full_name) if not prompt_list else prompt_list.get(full_name, get_prompt_from_filename(full_name))
                videos_dict = {model_name: os.path.abspath(videos_path)}
                cur_full_info_list = [{
                    "prompt_en": prompt,
                    "dimension": dimension_list,
                    "videos": videos_dict
                }]
            else:
                # Directory containing videos
                videos_by_prompt = {}

                # 遍历每个实际维度目录
                for actual_dim in actual_dimensions:
                    dimension_path = os.path.join(videos_path, actual_dim)
                    if os.path.exists(dimension_path):
                        for model_name in os.listdir(dimension_path):
                            model_path = os.path.join(dimension_path, model_name)
                            if os.path.isdir(model_path):
                                for video_name in os.listdir(model_path):
                                    if Path(video_name).suffix.lower() in ['.mp4', '.gif', '.jpg', '.png']:
                                        video_path = os.path.join(dimension_path, model_name, video_name)
                                        extracted_prompt = get_prompt_from_filename(video_name)
                                        
                                        # 在prompt_list中查找匹配的prompt
                                        matched_prompt = None
                                        if prompt_list:
                                            for prompt_key, prompt_value in prompt_list.items():
                                                if extracted_prompt in prompt_key or prompt_key in extracted_prompt:
                                                    matched_prompt = prompt_value
                                                    break
                                        
                                        prompt = matched_prompt if matched_prompt else extracted_prompt
                                        
                                        if prompt not in videos_by_prompt:
                                            videos_by_prompt[prompt] = {}
                                        videos_by_prompt[prompt][model_name] = video_path.replace("\\", "/")
                # Create info list entries
                for prompt, videos in videos_by_prompt.items():
                    cur_full_info_list.append({
                        "prompt_en": prompt,
                        "dimension": dimension_list,
                        "videos": videos
                    })
        
        elif mode == 'custom_input_nonconsistency':

            print('custom_input_nonconsistency')

        else:
            # Standard mode using benchmark data
            full_info_list = load_json(self.full_info_dir)
            
            for prompt_dict in full_info_list:
                # 检查是否有任何请求的维度在这个提示词的维度列表中
                if any(dim in dimension_list for dim in prompt_dict["dimension"]):
                    prompt = prompt_dict['prompt']
                    videos_dict = {}
                    
                    # 获取实际的数据目录
                    actual_dimensions = set(dimension_mapping[dim] for dim in dimension_list 
                                         if dim in prompt_dict["dimension"])
                    
                    # 遍历每个实际维度目录
                    for actual_dim in actual_dimensions:
                        dimension_path = os.path.join(videos_path, actual_dim)
                        if os.path.exists(dimension_path):
                            # 获取该维度下的所有模型目录
                            for model_name in os.listdir(dimension_path):
                                model_path = os.path.join(dimension_path, model_name)
                                if os.path.isdir(model_path):
                                    # 检查三个索引的视频
                                    for idx in range(3):
                                        video_name = f"{prompt}_{idx}.mp4"
                                        video_path = os.path.join(dimension_path, model_name, video_name)
                                        if os.path.exists(video_path):
                                            videos_dict[model_name] = video_path.replace("\\", "/")
                                            if verbose:
                                                print(f'Successfully found video: {video_path}')
                                        elif verbose:
                                            print(f'WARNING!!! Required video not found: {video_path}')
                    
                    if videos_dict:  # 只有当找到视频时才添加到列表中
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
