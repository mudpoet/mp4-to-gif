#!/usr/bin/env python3
import argparse
from pathlib import Path
from ..converter import convert_mp4_to_gif, validate_conversion_params

def main():
    parser = argparse.ArgumentParser(
        description='MP4 to GIF Converter CLI',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('input', type=str, help='Input MP4 file path')
    parser.add_argument('output', type=str, help='Output GIF file path')
    parser.add_argument('--loop', type=int, default=0,
                       help='Loop count (0 = infinite)')
    parser.add_argument('--start-time', default='00:00:00.000',
                       help='Start time in HH:MM:SS.ms format')
    parser.add_argument('--end-time', 
                       help='End time in HH:MM:SS.ms format')
    parser.add_argument('--fps', default='source',
                       help='Output FPS ("source" to preserve original)')
    parser.add_argument('--width', type=int, default=320,
                       help='Output width in pixels')

    args = parser.parse_args()
    
    try:
        # Validate paths
        if not Path(args.input).exists():
            raise FileNotFoundError(f"Input file {args.input} not found")
        
        # Prepare parameters
        params = {
            'loop': args.loop,
            'start_time': args.start_time,
            'end_time': args.end_time,
            'fps': args.fps,
            'output_width': args.width
        }
        
        # Validate and convert
        validate_conversion_params(params)
        convert_mp4_to_gif(args.input, args.output, params)
        
        print(f"Successfully created {args.output}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()