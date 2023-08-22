import cv2
import numpy as np
import glob
import os


def create_pencil_sketch_from_image(image, _path, _name):
    # convert an image from one color space to another
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    invert = cv2.bitwise_not(gray_img)  # helps in masking of the image
    # sharp edges in images are smoothed while minimizing too much blurring
    blur = cv2.GaussianBlur(invert, (21, 21), 0)

    inverted_blur = cv2.bitwise_not(blur)

    sketch = cv2.divide(gray_img, inverted_blur, scale=256.0)

    # cv2.imshow("New Image", sketch)
    # cv2.waitKey(0)
    cv2.imwrite(_path + "pencil2_" + _name,
                sketch)  # converted image is saved as mentioned name
    print("Pencil Sketch Created successfully.")
    return _path + "pencil2_" + _name


def from_image_to_another(src, dest, _path, _name, _extension):
    new_image = src.astype(int)
    for i in range(256):
        new_image = np.where(new_image == dest, new_image + 1, new_image)
        new_image = np.where(new_image >= dest, new_image - 1, new_image + 1)
        new_path = _path
        new_path += f"output/from_image_to_another_{_name}_{(256 - i):03}"+_extension
        cv2.imwrite(new_path, new_image)


def make_video(_path, _name, _extension):
    images = []
    general_photos_path = _path + 'output\\*'+_extension
    for filename in glob.glob(general_photos_path):
        images.append(cv2.imread(filename))
    frame = images[0]
    height, width, layers = frame.shape

    video = cv2.VideoWriter(_path + f'\\output\\{_name}.avi', 0, 60,
                            (width, height))
    for image in images:
        video.write(image)
    cv2.destroyAllWindows()
    video.release()  # releasing the video generated
    print("Video Created successfully.")


def check_if_output_folder_exists(_path):
    folder_path = _path+'\\output'

    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If it doesn't exist, create it
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def make_video_from_scratch(_path, _name):
    # ------ Init ------
    image_original = cv2.imread(_path + _name)  # Choose PathName

    # ------ Create Pencil Sketch ------
    sketch_path = create_pencil_sketch_from_image(image_original, _path, _name)
    image_final = cv2.imread(sketch_path)  # choose image to transfer to

    # ------ Create Frames ------
    root, extension = os.path.splitext(_path + _name)
    check_if_output_folder_exists(_path)
    from_image_to_another(image_original, image_final, _path, _name, extension)

    # ------ Create Video ------
    make_video(_path, _name, extension)


if __name__ == '__main__':
    path = "OurPhoto\\"
    name = "1.jpeg"
    make_video_from_scratch(path, name)
