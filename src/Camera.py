import os

class Camera(object):
    """
    Class Description:
    Camera Object used to communicate with cameras connected to the computer.

    Author(s):
    Jacob Taylor Cassady

    Dates: 
    Created - 6/5/18
    Updated - 6/5/18
    """
    def __init__(self, control_cmd_location = None, save_folder_path=None, script_path = None, image_type=None, image_name=None,
				 aperture=None, exposure_control=None, shutter_speed=None, iso=None):
        # Initialize variables
        self.control_cmd_location = self.set_control_cmd_location(control_cmd_location)
        self.save_folder = self.set_save_folder(save_folder_path)
        self.script_location = self.set_script_path(script_path)
        self.setup(aperture=aperture, exposure_control=exposure_control, shutter_speed=shutter_speed, iso=iso)
        self.image_type = self.set_image_type(image_type)
        self.image_name = image_name
        self.image_index = 0		

    def setup(self, aperture=None, exposure_control=None, shutter_speed=None, iso=None, setup_script_name="setup.dccscript"):
        """
        Function Desciption:
        Drives the setup of the camera given a set of settings.  Autocodes the setup script and runs it.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/6/18
        Updated - 6/6/18
        """
        self.generate_setup_script(setup_script_name=setup_script_name, aperture=aperture, exposure_control=exposure_control, shutter_speed=shutter_speed, iso=iso)
        self.run_script(script_name=setup_script_name)

    def generate_setup_script(self, setup_script_name, aperture=None, exposure_control=None, shutter_speed=None, iso=None):
        """
        Function Description:
        Generates the setup script to set the aperture, exposure_control, shutter_speed,, and iso of the camera if any of these values are passed.

		Author(s):
		Jacob Taylor Cassady

		Dates:
		Created - 6/6/18
		Updated - 6/6/18
		"""
        settings = {"aperture" : aperture,
                       "ec" : exposure_control,
                       "shutter" : shutter_speed,
                       "iso" : iso}

        with open(self.script_location + setup_script_name, "w") as file:
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file.write("<dccscript>\n")
            file.write(" "*2 + "<commands>\n")
            self.write_settings(file, settings)
            file.write(" "*2 + "</commands>\n")
            file.write("</dccscript>")

    def write_settings(self, file, settings):
        """
        Function Description:
        Writes the passed dictionary of settings to the passed file.  If a setting has a value of None, it is passed over.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/6/18
        Updated - 6/6/18
        """
        for setting in settings:
            if settings[setting] is not None:
                file.write(" "*3 + "<setcamera property=\"" + str(setting) + "\" value=\"" + settings[setting] + "\"/>\n")
                
    def set_control_cmd_location(self, control_cmd_location=None):
        """
        Function Description:
        Sets the location of CameraControlCmd.exe which is used to command a camera from the command line using the program DigiCamControl.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if control_cmd_location is None:
            control_cmd_location = "\"C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe\""

        return control_cmd_location

    def command_camera(self, command):
        """
        Function Description:
        Creates a call to the camera using DigiCamControl

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        os.system(self.control_cmd_location + " /filename "  + self.save_folder + self.image_name + str(self.image_index) + self.image_type +  " " + command)

    def run_script(self, script_name):
        """
        Function Description:
        Runs the passed script within the script location.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/6/18
        Updated - 6/6/18
        """
        os.system(self.control_cmd_location + " " + self.script_location + script_name)

    def set_save_folder(self, folder_path=None):
        """
        Function Description:
        Sets the folder path for saving images taken using this class.  If no folder path is given, a preset relative path is used.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if folder_path is None:
            folder_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep +".." + os.path.sep + "Camera" + os.path.sep + "Images" + os.path.sep

        return folder_path

    def set_script_path(self, script_path=None):
        """
        Function Description:
        Sets the path for CameraScripts used to control the camera.  If no path is given, a preset relative path is used.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if script_path is None:
            script_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + ".." + os.path.sep + "Camera" + os.path.sep + "CameraScripts" + os.path.sep

        print(script_path)

        return script_path

    def set_image_type(self, image_type=None):
        """
        Function Description:
        Sets the image type.  If none is given, the default CannonRaw2 image type is used.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if image_type == "jpeg" or image_type == "jpg":
            return ".jpg"
        else:
            return ".CR2"

    def capture_single_image(self, autofocus=False):
        """
        Function Description:
        Captures a single image.  Iterates the image index to ensure a unique name for each image taken.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        if autofocus:
            self.command_camera("/capture")
        else:
            self.command_camera("/capturenoaf")
        self.image_index += 1

    def capture_multiple_images(self, image_count):
        """
        Function Description:
        Captures an n number of images by repeatedly calling the capture_single_image function n times where n is the parameter image_count.

        Author(s):
        Jacob Taylor Cassady

        Dates:
        Created - 6/5/18
        Updated - 6/5/18
        """
        for capture in range(image_count):
            self.capture_single_image()

if __name__ == "__main__":
    # Aperture sizes: 2.8, 3.2, 3.5, 4.0, 4.5, 5.0, 5.6, 6.3, 7.1, 8.0, 9.0, 10, 11, 13, 14, 16, 18, 20, 22
    # Shutter speeds: 1/4, 1/5, 1/6, 1/8, 1/10, 1/13, 1/15, 1/20, 1/25, 1/30, 1/40, 1/50, 1/60, 1/80, 1/100, 1/125, 1/160, 1/200, 1/250, 1/320, 1/400, 1/500, 1/640, 1/800, 1/1000, 1/1250, 1/1600, 1/2000, 1/2500, 1/3200, 1/4000  
    # ISO: 100, 200, 400, 800, 1600, 3200, 6400, 12800

    test_cam = Camera(image_type="jpg", image_name="test_image", shutter_speed="1/1600", iso="12800", aperture="6.3")

    test_cam.capture_multiple_images(10)
