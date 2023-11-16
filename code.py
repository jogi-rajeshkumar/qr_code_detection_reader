import cv2
import time
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from datetime import datetime
import os
import csv


# Specify the parent directory path
parent_dir = "Admit_card"  # Change this to the path of your input frames folder
dest = "output_frames/"  # Change this to the path where you want to save frames with QR codes
csv_file = "completed_videos.csv"  # CSV file to store information about completed videos

# Read existing completed videos from CSV
completed_videos = set()
if os.path.exists(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            completed_videos.add(row[0])

# Find all video files in the parent directory and its subdirectories
video_files = []
for root, dirs, files in os.walk(parent_dir):
    for file in files:
        if file.lower().endswith(('.jpg','.avi', '.mp4', '.mov', '.mkv', '.mts', '.flv', '.ts', '.webm')):
            video_files.append(os.path.join(root, file))

start_time = time.time()

for video_path in video_files:
    if video_path in completed_videos:
        print(f"Video {video_path} already completed. Skipping...")
        continue

    print(f"Current Running video ||||||||||||||| {video_path}")

    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    video_completed = False

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % 1 == 0:
            # Your frame processing code here

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_resized = cv2.resize(frame, (1920, 1080))
            cv2.imshow("Window", gray_resized)
            cv2.waitKey(2)

            # Detect ArUco markers
            # decoded_objects = decode(gray)

            decoded_objects = decode(gray, symbols=[ZBarSymbol.QRCODE])



            # Check if any QR code is detected
            if decoded_objects:
                qr_data = decoded_objects[0].data.decode('utf-8')
                output_path = os.path.join(dest, f"{qr_data}_1.jpg")
                counter = 0
                while os.path.exists(output_path):
                    counter += 1
                    output_path = os.path.join(dest, f"{qr_data}_{counter}.jpg")

                cv2.imwrite(output_path, frame)
                print(f"QR code detected in {file}. Saved to {output_path}")
                video_completed = True
                
                if video_completed:
                    # Update the CSV file with the completed video
                    with open(csv_file, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([video_path])
                break

        frame_count += 1

    # if video_completed:
    #     # Update the CSV file with the completed video
    #     with open(csv_file, 'a', newline='') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow([video_path])

    print(f"Completed video {video_path}")
    # move to the next video by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

end_time = time.time()
print("------ %.2f seconds -------" % (end_time - start_time))
