import cv2
import os
import argparse
from pathlib import Path

def extract_frames(video_path, output_dir, fps=10, max_frames=None):
    """
    Extract frames from video at specified FPS
    
    Args:
        video_path: Path to input video file
        output_dir: Directory to save extracted frames
        fps: Frames per second to extract (lower = fewer frames)
        max_frames: Maximum number of frames to extract (None = all)
    """
    # Check if video exists
    if not os.path.exists(video_path):
        print(f"❌ Error: Video not found at {video_path}")
        return
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Open video
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print(f"❌ Error: Could not open video {video_path}")
        return
    
    video_fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / video_fps if video_fps > 0 else 0
    
    print(f"\n📹 Video Info:")
    print(f"   File: {os.path.basename(video_path)}")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {video_fps:.1f}")
    print(f"   Total Frames: {total_frames}")
    print(f"   Duration: {duration:.2f} seconds")
    
    # Calculate frame interval
    if video_fps == 0:
        print(f"❌ Error: Invalid video FPS")
        video.release()
        return
    
    frame_interval = int(video_fps / fps)
    estimated_frames = total_frames // frame_interval
    
    print(f"\n⚙️  Extraction Settings:")
    print(f"   Target FPS: {fps}")
    print(f"   Frame Interval: Every {frame_interval} frames")
    print(f"   Estimated Output: {estimated_frames} frames")
    if max_frames:
        print(f"   Max Frames Limit: {max_frames}")
    
    frame_count = 0
    saved_count = 0
    
    print(f"\n🔄 Extracting frames...")
    
    while True:
        success, frame = video.read()
        if not success:
            break
        
        # Extract frame at interval
        if frame_count % frame_interval == 0:
            frame_filename = f"frame_{saved_count:06d}.jpg"
            frame_path = os.path.join(output_dir, frame_filename)
            cv2.imwrite(frame_path, frame)
            saved_count += 1
            
            # Progress update every 50 frames
            if saved_count % 50 == 0:
                print(f"   Extracted {saved_count} frames...")
            
            # Stop if max_frames reached
            if max_frames and saved_count >= max_frames:
                print(f"   Reached maximum of {max_frames} frames")
                break
        
        frame_count += 1
    
    video.release()
    
    print(f"\n✅ Complete!")
    print(f"   Total frames extracted: {saved_count}")
    print(f"   Output directory: {output_dir}")
    print(f"   Average extraction rate: {saved_count / duration:.1f} frames/second")

def preview_frames(frame_dir, num_preview=5):
    """
    Display a few extracted frames to verify quality
    
    Args:
        frame_dir: Directory containing extracted frames
        num_preview: Number of frames to display
    """
    frames = sorted([f for f in os.listdir(frame_dir) if f.endswith('.jpg')])
    
    if not frames:
        print(f"❌ No frames found in {frame_dir}")
        return
    
    print(f"\n👁️  Previewing {min(num_preview, len(frames))} frames...")
    print("   Press any key to see next frame, 'q' to quit preview")
    
    for i in range(min(num_preview, len(frames))):
        frame_path = os.path.join(frame_dir, frames[i])
        img = cv2.imread(frame_path)
        
        if img is None:
            print(f"   ⚠️  Could not read {frames[i]}")
            continue
        
        # Resize for display if too large
        height, width = img.shape[:2]
        if width > 1280:
            scale = 1280 / width
            img = cv2.resize(img, (1280, int(height * scale)))
        
        cv2.imshow(f'Frame Preview - {frames[i]}', img)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        if key == ord('q'):
            print("   Preview cancelled")
            break

def main():
    parser = argparse.ArgumentParser(
        description='Extract frames from Clash Royale gameplay videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic extraction (10 FPS)
  python scripts/extract_frames.py --video data/raw_videos/game1.mp4
  
  # Extract at 15 FPS
  python scripts/extract_frames.py --video data/raw_videos/game1.mp4 --fps 15
  
  # Extract only 100 frames
  python scripts/extract_frames.py --video data/raw_videos/game1.mp4 --max-frames 100
  
  # Custom output directory
  python scripts/extract_frames.py --video game1.mp4 --output data/frames/match1
        """
    )
    
    parser.add_argument(
        '--video',
        type=str,
        default='data/raw_videos/game1.mp4',
        help='Path to video file (default: data/raw_videos/game1.mp4)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output directory for frames (default: data/frames/[video_name])'
    )
    
    parser.add_argument(
        '--fps',
        type=int,
        default=10,
        help='Frames per second to extract (default: 10)'
    )
    
    parser.add_argument(
        '--max-frames',
        type=int,
        default=None,
        help='Maximum number of frames to extract (default: all)'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview extracted frames after completion'
    )
    
    parser.add_argument(
        '--preview-count',
        type=int,
        default=5,
        help='Number of frames to preview (default: 5)'
    )
    
    args = parser.parse_args()
    
    # Auto-generate output directory if not specified
    if args.output is None:
        video_name = Path(args.video).stem
        args.output = f"data/frames/{video_name}"
    
    # Extract frames
    print("=" * 60)
    print("🎮 CLASH ROYALE FRAME EXTRACTOR")
    print("=" * 60)
    
    extract_frames(args.video, args.output, args.fps, args.max_frames)
    
    # Preview if requested
    if args.preview:
        preview_frames(args.output, args.preview_count)
    
    print("\n" + "=" * 60)
    print("✨ Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()