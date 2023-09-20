import cv2
import os
import sys

def create_video_from_images(image_folder, output_path, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Change the codec as needed
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for _ in range(10):
        for image in images:
            img_path = os.path.join(image_folder, image)
            frame = cv2.imread(img_path)
            video.write(frame)

    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    image_folder = sys.argv[1]
    output_path = "output_video.avi"
    fps = 60  # Frames per second

    create_video_from_images(image_folder, output_path, fps)
