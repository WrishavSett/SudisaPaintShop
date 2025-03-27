import cv2
import os
from tqdm import tqdm

def extract_frames(video_folder, output_folder, resize_dim=(1280, 720), jpeg_quality=80, frame_skip=4):
    """
    Extract frames from videos, resize them, and save with specified JPEG quality.
    
    Parameters:
    - video_folder: Path to the folder containing video files.
    - output_folder: Path to the folder to save extracted frames.
    - resize_dim: Tuple specifying the target width and height (default: 1280x720).
    - jpeg_quality: JPEG compression quality (1-100, default: 80).
    - frame_skip: Number of frames to skip (default: 5, saves every 5th frame).
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through all files in the video folder
    for video_file in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_file)
        
        # Check if the file is a video
        if os.path.isfile(video_path) and video_file.endswith(('.mp4', '.avi', '.mkv', '.mov')):
            # Create a subfolder for this video
            video_name = os.path.splitext(video_file)[0]
            video_output_folder = os.path.join(output_folder, video_name)
            os.makedirs(video_output_folder, exist_ok=True)

            # Read the video
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            saved_frame_count = 0

            # Get the total number of frames
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Adjust total frames for progress bar considering frame skipping
            frames_to_process = total_frames // frame_skip
            
            # Initialize progress bar
            with tqdm(total=frames_to_process, desc=f"Processing {video_file}", unit="frame") as pbar:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Skip frames
                    if frame_count % frame_skip == 0:
                        # Resize frame
                        resized_frame = cv2.resize(frame, resize_dim, interpolation=cv2.INTER_AREA)
                        
                        # Save frame to subfolder with specified JPEG quality
                        frame_filename = os.path.join(video_output_folder, f"{video_name}_{saved_frame_count:04d}.jpg")
                        cv2.imwrite(frame_filename, resized_frame, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])
                        
                        saved_frame_count += 1
                        pbar.update(1)  # Update progress bar
                    
                    frame_count += 1
            
            cap.release()
            print(f"Extracted {saved_frame_count} frames from {video_file}")

if __name__ == "__main__":
    video_folder = input("Enter input dir path: ")  # Replace with your video folder path
    output_folder = "D:/SUDISA/output_recordings"  # Replace with your output folder path
    frame_skip = 9  # Save every 5th frame
    extract_frames(video_folder, output_folder, resize_dim=(1280, 720), frame_skip=frame_skip)
