#!/usr/bin/env python
import os
import sys
import json
import argparse
from datetime import datetime
from HAbench import HABench

def parse_args():
    parser = argparse.ArgumentParser(
        description='HABench - Human Preference Aligned Video Generation Benchmark',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "--output_path",
        type=str,
        default='./evaluation_results/',
        help="output path to save the evaluation results"
    )
    
    parser.add_argument(
        "--config_path",
        type=str,
        default='./config.json',
        help="path to the config file"
    )
    
    parser.add_argument(
        "--videos_path",
        type=str,
        required=True,
        help="folder that contains the videos to evaluate"
    )
    
    parser.add_argument(
        "--dimension",
        nargs='+',
        choices=[
            'color',
            'object_class',
            'scene',
            'action',
            'overall_consistency',
            'imaging_quality',
            'aesthetic_quality',
            'temporal_consistency',
            'motion_effects'
        ],
        required=True,
        help="evaluation dimensions to use"
    )
    
    parser.add_argument(
        "--full_json_dir",
        type=str,
        default=None,
        help="path to save the full evaluation information json file"
    )

    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_path, exist_ok=True)

    HAVBench = HABench(args.full_json_dir, args.output_path, args.config_path)

    current_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    kwargs = {}

    dimension_str = args.dimension[0]

    try:
        # Run evaluation
        HAVBench.evaluate(
            videos_path = args.videos_path,
            #name = f'results_{current_time}',
            name = f'results_{dimension_str}',
            dimension_list = args.dimension,
            **kwargs
        )
        
        print(f"\nEvaluation completed successfully!")
        
    except Exception as e:
        print(f"\nError during evaluation: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 