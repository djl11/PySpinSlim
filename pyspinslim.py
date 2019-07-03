import PySpin

class PySpinSlim():

    def __init__(self):

        # Retrieve singleton reference to system object
        self._system = PySpin.System.GetInstance()

        # Retrieve list of cameras from the system
        self._cams = self._system.GetCameras()
        for cam in self._cams:
            cam.Init()

        # Retrieve TL device nodemap and print device information
        self._nodemaps_tldevice = [cam.GetTLDeviceNodeMap() for cam in self._cams]

        # Retrieve GenICam nodemaps
        self._nodemaps = [cam.GetNodeMap() for cam in self._cams]


    # Pixel Format #
    #--------------#

    def _set_pixel_format(self, format, cam_idx=0):

        node_pixel_format = PySpin.CEnumerationPtr(self._nodemaps[cam_idx].GetNode('PixelFormat'))
        if not PySpin.IsAvailable(node_pixel_format) or not PySpin.IsWritable(node_pixel_format):
            raise Exception('Unable to set Pixel Format. Aborting...')

        else:
            # Retrieve entry node from enumeration node
            entry_pixel_format = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName(format))
            if not PySpin.IsAvailable(entry_pixel_format) or not PySpin.IsReadable(entry_pixel_format):
                raise Exception('Unable to set Pixel Format to' + format + '. Aborting...')

            # Retrieve integer value from entry node
            pixel_format = entry_pixel_format.GetValue()

            # Set integer value from entry node as new value of enumeration node
            node_pixel_format.SetIntValue(pixel_format)

    def set_rgb(self, cam_idx=0):
        self._set_pixel_format('RGB8',cam_idx)

    def set_mono(self, cam_idx=0):
        self._set_pixel_format('Mono8',cam_idx)

    # Buffer Handling #
    #-----------------#

    def _set_buffer_handling(self, format, cam_idx=0):

        # Retrieve Stream Parameters device nodemap
        s_node_map = self._cams[cam_idx].GetTLStreamNodeMap()

        handling_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferHandlingMode'))
        if not PySpin.IsAvailable(handling_mode) or not PySpin.IsWritable(handling_mode):
            raise Exception('Unable to set Buffer Handling mode (node retrieval). Aborting...\n')

        handling_mode_entry = handling_mode.GetEntryByName(format)
        handling_mode.SetIntValue(handling_mode_entry.GetValue())


    def set_newest_first(self, cam_idx=0):
        self._set_buffer_handling('NewestFirst', cam_idx)


    def set_newest_only(self, cam_idx=0):
        self._set_buffer_handling('NewestOnly', cam_idx)


    def set_oldest_first(self, cam_idx=0):
        self._set_buffer_handling('OldestFirst', cam_idx)


    def set_oldest_first_overwrite(self, cam_idx=0):
        self._set_buffer_handling('OldestFirstOverwrite', cam_idx)



    # Image Acquisition #
    #-------------------#

    def begin_camera_acquisition(self, cam_idx=0):
        self._cams[cam_idx].BeginAcquisition()

    def stop_camera_acquisition(self, cam_idx=0):
        self._cams[cam_idx].EndAcquisition()

    def get_next_image(self, cam_idx=0):
        image_frame = self._cams[cam_idx].GetNextImage()
        time_stamp = image_frame.GetTimeStamp()
        image = image_frame.GetData()
        image_frame.Release()
        return image, time_stamp

    def get_image_dims(self, cam_idx=0):
        width = self._cams[cam_idx].Width.GetValue()
        height = self._cams[cam_idx].Height.GetValue()
        return (height, width)

    def shutdown(self):
        """
        shutdown PySpinSlim, to be called at end of program
        """

        # clear cameras
        for cam in self._cams:
            cam.DeInit()
            del cam
        self._cams.Clear()

        # release system instance
        self._system.ReleaseInstance()