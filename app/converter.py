import subprocess
import os
import logging
from typing import Dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_conversion_params(params: Dict) -> None:
    """Validate common conversion parameters"""
    if not isinstance(params['loop'], int) or params['loop'] < 0:
        raise ValueError("Loop count must be a non-negative integer")
    
    if params['output_width'] < 1:
        raise ValueError("Output width must be at least 1 pixel")
    
    if params['fps'] != 'source' and float(params['fps']) <= 0:
        raise ValueError("FPS must be 'source' or a positive number")

def convert_mp4_to_gif(input_path: str, output_path: str, params: Dict) -> None:
    """
    Shared conversion function for both CLI and web interfaces
    
    Args:
        input_path: Path to source MP4 file
        output_path: Path to output GIF file
        params: Dictionary containing:
            - loop: int (0 = infinite)
            - start_time: str (HH:MM:SS.ms)
            - end_time: str (HH:MM:SS.ms)
            - fps: str/number ('source' or value)
            - output_width: int
    """
    # Validate parameters first
    validate_conversion_params(params)
    
    # Build base FFmpeg command
    command = [
        'ffmpeg',
        '-y',  # Overwrite output without asking
        '-ss', params['start_time'],
        '-i', input_path
    ]

    # Add end time if specified
    if params.get('end_time'):
        command += ['-to', params['end_time']]

    # Video filters
    filters = [
        f"scale={params['output_width']}:-1:flags=lanczos"
    ]

    # Frame rate handling
    if params['fps'] != 'source':
        filters.append(f"fps={params['fps']}")

    # Add filters to command
    if filters:
        command += ['-vf', ','.join(filters)]

    # Loop control
    command += [
        '-loop', str(params['loop']),
        '-f', 'gif',
        output_path
    ]

    # Run conversion
    logger.info(f"Starting conversion with command: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        logger.debug("FFmpeg output:\n%s", result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Conversion failed with error:\n%s", e.stdout)
        raise RuntimeError(f"FFmpeg conversion failed: {e.stdout}") from e

    logger.info("Conversion completed successfully")