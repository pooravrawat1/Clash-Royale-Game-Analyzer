import os
from ultralytics import YOLO
import argparse
from pathlib import Path

def train_model(data_yaml, epochs=100, imgsz=640, batch=16, model_size='n', project='models', name='troop_detector'):
    """
    Train YOLO model on Clash Royale dataset
    
    Args:
        data_yaml: Path to data.yaml file
        epochs: Number of training epochs
        imgsz: Image size for training
        batch: Batch size (reduce if out of memory)
        model_size: YOLO model size (n/s/m/l/x - n is smallest/fastest)
        project: Project directory to save results
        name: Name of this training run
    """
    
    # Check if data.yaml exists
    if not os.path.exists(data_yaml):
        print(f"❌ Error: data.yaml not found at {data_yaml}")
        return
    
    print("=" * 60)
    print("🎮 CLASH ROYALE TROOP DETECTOR TRAINING")
    print("=" * 60)
    
    # Load pretrained YOLO model
    model_name = f'yolov8{model_size}.pt'
    print(f"\n📦 Loading pretrained model: {model_name}")
    
    try:
        model = YOLO(model_name)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    print(f"✅ Model loaded successfully")
    
    # Print training configuration
    print(f"\n⚙️  Training Configuration:")
    print(f"   Dataset: {data_yaml}")
    print(f"   Epochs: {epochs}")
    print(f"   Image Size: {imgsz}")
    print(f"   Batch Size: {batch}")
    print(f"   Model: YOLOv8{model_size}")
    print(f"   Output: {project}/{name}")
    
    # Train the model
    print(f"\n🚀 Starting training...")
    print("=" * 60)
    
    try:
        results = model.train(
            data=data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            name=name,
            project=project,
            patience=20,  # Early stopping if no improvement for 20 epochs
            save=True,
            plots=True,
            device='cuda' if os.system('nvidia-smi') == 0 else 'cpu',  # Auto-detect GPU
            verbose=True
        )
        
        print("\n" + "=" * 60)
        print("✅ Training Complete!")
        print("=" * 60)
        
        # Print results location
        save_dir = Path(project) / name
        print(f"\n📊 Results saved to: {save_dir}")
        print(f"\n📈 Training plots:")
        print(f"   - {save_dir}/results.png")
        print(f"   - {save_dir}/confusion_matrix.png")
        print(f"\n🏆 Best model: {save_dir}/weights/best.pt")
        print(f"📦 Last model: {save_dir}/weights/last.pt")
        
        # Validate the model
        print(f"\n🧪 Running validation...")
        metrics = model.val()
        
        print(f"\n📊 Validation Metrics:")
        print(f"   mAP50: {metrics.box.map50:.3f}")
        print(f"   mAP50-95: {metrics.box.map:.3f}")
        
        print("\n" + "=" * 60)
        print("✨ All Done!")
        print("=" * 60)
        print(f"\nNext steps:")
        print(f"1. Check training plots in {save_dir}/")
        print(f"2. Test your model with: python scripts/test_model.py")
        print(f"3. If accuracy is low, annotate more images and retrain")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        print(f"\nCommon issues:")
        print(f"- Out of memory: Try --batch 8 or --batch 4")
        print(f"- Path errors: Check data.yaml paths are correct")
        print(f"- CUDA errors: Try --device cpu")

def main():
    parser = argparse.ArgumentParser(
        description='Train YOLO model for Clash Royale troop detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic training (recommended for first run)
  python scripts/train_model.py
  
  # Train for more epochs
  python scripts/train_model.py --epochs 150
  
  # Smaller batch size (if running out of memory)
  python scripts/train_model.py --batch 8
  
  # Use larger model for better accuracy
  python scripts/train_model.py --model-size s
  
  # Custom dataset
  python scripts/train_model.py --data path/to/data.yaml
        """
    )
    
    parser.add_argument(
        '--data',
        type=str,
        default='data/datasets/troops_v1/data.yaml',
        help='Path to data.yaml file'
    )
    
    parser.add_argument(
        '--epochs',
        type=int,
        default=100,
        help='Number of training epochs (default: 100)'
    )
    
    parser.add_argument(
        '--imgsz',
        type=int,
        default=640,
        help='Image size for training (default: 640)'
    )
    
    parser.add_argument(
        '--batch',
        type=int,
        default=16,
        help='Batch size (default: 16, reduce if out of memory)'
    )
    
    parser.add_argument(
        '--model-size',
        type=str,
        default='n',
        choices=['n', 's', 'm', 'l', 'x'],
        help='Model size: n(ano), s(mall), m(edium), l(arge), x(large) - default: n'
    )
    
    parser.add_argument(
        '--project',
        type=str,
        default='models',
        help='Project directory (default: models)'
    )
    
    parser.add_argument(
        '--name',
        type=str,
        default='troop_detector',
        help='Training run name (default: troop_detector)'
    )
    
    args = parser.parse_args()
    
    train_model(
        data_yaml=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        model_size=args.model_size,
        project=args.project,
        name=args.name
    )

if __name__ == "__main__":
    main()