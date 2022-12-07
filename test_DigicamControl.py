#!/usr/bin/env python
"""unit_tests.py:"""

__author__ = 'Jacob Taylor Cassady'
__email__ = 'jacobtaylorcassady@outlook.com'

from unittest import TestCase, main, skip
from os.path import join, sep
from DigiCam.Camera import Camera

# Update with the path to your CameraControlCmd.exe file.  This is likely found within digiCamControl which is likely within one of your program directories.
CAMERA_CONTROL_CMD_PATH = join('C:' + sep, 'Program Files (x86)', 'digiCamControl', 'CameraControlCmd.exe')
SAVE_FOLDER_PATH = join('C:' + sep, 'Users', 'egand', 'Documents', 'GitHub', 'DigiCam', 'test')
IMAGE_IDX = 2

class TestDigiCamControl(TestCase):
    """[summary]"""
    def test_camera_initialization(self) -> None:
        """[summary]"""
        Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH, save_folder=SAVE_FOLDER_PATH, image_index=IMAGE_IDX)

    @skip # Skipped by default because a camera must be connected for this test to pass.
    def test_setup(self) -> None:
        """[summary]"""
        test_camera = Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH, save_folder=SAVE_FOLDER_PATH, image_index=IMAGE_IDX)
        test_setting: Camera.Settings = Camera.Settings(aperture='2.8', exposure_control='1',
                                                        shutter_speed='10', iso='AUTO')


        test_camera.setup(test_setting)

    def test_capture(self) -> None:
        """[summary]"""
        test_camera = Camera(control_cmd_location=CAMERA_CONTROL_CMD_PATH, save_folder=SAVE_FOLDER_PATH, image_index=IMAGE_IDX)

        test_camera.capture_single_image(autofocus=True)




if __name__ == '__main__':
    main()
    
    