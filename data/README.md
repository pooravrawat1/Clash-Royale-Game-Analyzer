# Data Directory

This directory contains all data files for the project.

⚠️ **Note**: This directory is gitignored to avoid committing large files.

## Structure

- `raw_videos/` - Original game recordings (MP4, AVI, etc.)
- `frames/` - Extracted frames from videos
- `datasets/` - Annotated datasets for training (YOLO format)

## Getting Started

1. Place your game recordings in `raw_videos/`
2. Run frame extraction script
3. Upload frames to Roboflow for annotation
4. Download annotated dataset to `datasets/`

## Dataset Format

Datasets should follow YOLOv8 format:

```
datasets/troops_v1/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── data.yaml
```
