from os.path import join, sep
from DigiCam.Camera import Camera


def setup_and_capture(save_loc, img_idx):

    # Update with the path to your CameraControlCmd.exe file.  This is likely found within digiCamControl which is likely within one of your program directories.
    # Replace the below path with the absolute or relative path to your CameraControlCmd executable.
    camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'

    test_camera = Camera(control_cmd_location=camera_control_cmd_path, save_folder=save_loc, image_index=img_idx)

    test_setting: Camera.Settings = Camera.Settings(aperture='2.8', exposure_control='1',
                                                        shutter_speed='10', iso='AUTO')


    test_camera.setup(test_setting)

    test_camera.capture_single_image(autofocus=True)


if __name__ == '__main__':

    SAVE_FOLDER_PATH = join('C:' + sep, 'Users', 'egand', 'Documents', 'GitHub', 'DigiCam', 'test')
    IMAGE_IDX = 2
    setup_and_capture(SAVE_FOLDER_PATH, IMAGE_IDX)
