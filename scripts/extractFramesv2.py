import cv2
import os
from tqdm import tqdm

def extract_frames(video_folder, output_folder, jpeg_quality=80):
    """
    Extract frames from videos and save with specified JPEG quality.
    
    Parameters:
    - video_folder: Path to the folder containing video files.
    - output_folder: Path to the folder to save extracted frames.
    - jpeg_quality: JPEG compression quality (1-100, default: 80).
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

            # Get the total number of frames
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Initialize progress bar
            with tqdm(total=total_frames, desc=f"Processing {video_file}", unit="frame") as pbar:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Save frame to subfolder with specified JPEG quality
                    frame_filename = os.path.join(video_output_folder, f"{video_name}_{frame_count:04d}.jpg")
                    cv2.imwrite(frame_filename, frame, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])
                    
                    frame_count += 1
                    pbar.update(1)  # Update progress bar
            
            cap.release()
            print(f"Extracted {frame_count} frames from {video_file}")

if __name__ == "__main__":
    video_folder = input("Enter input dir path: ")  # Replace with your video folder path
    output_folder = "D:/SUDISA/output_recordings"  # Replace with your output folder path
    extract_frames(video_folder, output_folder)
