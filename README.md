# Clash Royale Game Analyzer

🎮 An AI-powered computer vision system that analyzes Clash Royale gameplay recordings and generates detailed transcripts of game events.

## Features

- 🔍 **Troop Detection**: Identifies and tracks troops, spells, and buildings
- 📍 **Coordinate Mapping**: Converts pixel coordinates to arena grid positions
- 📝 **Event Transcription**: Logs deployments, damage, and other game events
- 📊 **Game Analysis**: Generates statistics and visualizations

## Project Status

🚧 **In Development** - Currently working on MVP with basic troop detection

### Current Progress

- [x] Project setup
- [x] Frame extraction
- [ ] Data annotation (in progress)
- [ ] Model training
- [ ] Basic detection
- [ ] Event analysis
- [ ] Transcript generation

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/clash-royale-analyzer.git
cd clash-royale-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Extract Frames from Video

```bash
python scripts/extract_frames.py --video data/raw_videos/game1.mp4 --output data/frames/game1
```

### 2. Train Detection Model

```bash
python scripts/train_model.py --data data/datasets/troops_v1/data.yaml --epochs 100
```

### 3. Analyze a Game

```bash
python scripts/analyze_game.py --video data/raw_videos/game1.mp4 --output outputs/transcripts/game1.txt
```

## Tech Stack

- **Python 3.10+**
- **YOLOv8** - Object detection
- **OpenCV** - Video processing
- **PyTorch** - Deep learning backend
- **Roboflow** - Dataset management

## Documentation

- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [Annotation Guide](docs/annotation_guide.md)
- [Troop Classes](docs/troop_classes.md)

## Contributing

This is currently a personal project, but suggestions and feedback are welcome!
