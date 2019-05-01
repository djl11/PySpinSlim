import PySpin

def configure_trigger(nodemap):
    """
    This function configures the camera to use a trigger. First, trigger mode is
    set to off in order to select the trigger source. Once the trigger source
    has been selected, trigger mode is then enabled, which has the camera
    capture only a single image upon the execution of the trigger.

    :param nodemap: Device nodemap to retrieve images from.
    :type nodemap: INodeMap
    :return: True if successful, False otherwise
    :rtype: bool
    """
    try:
        result = True
        print('\n*** CONFIGURING TRIGGER ***\n')

        # Ensure trigger mode off
        #
        # *** NOTES ***
        # The trigger must be disabled in order to configure the
        # trigger source.
        trigger_mode = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
        if not PySpin.IsAvailable(trigger_mode) or not PySpin.IsWritable(trigger_mode):
            print('Unable to disable trigger mode (node retrieval). Aborting...\n')
            return False

        trigger_mode_off = PySpin.CEnumEntryPtr(trigger_mode.GetEntryByName('Off'))
        if not PySpin.IsAvailable(trigger_mode_off) or not PySpin.IsReadable(trigger_mode_off):
            print('Unable to disable trigger mode (enum entry retrieval). Aborting...\n')
            return False

        trigger_mode.SetIntValue(trigger_mode_off.GetValue())
        print('Trigger mode disabled...')

        # Set trigger source to software
        trigger_source = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerSource'))
        if not PySpin.IsAvailable(trigger_source) or not PySpin.IsWritable(trigger_source):
            print('Unable to set trigger mode (node retrieval). Aborting...')
            return False

        trigger_source_software = PySpin.CEnumEntryPtr(trigger_source.GetEntryByName('Software'))
        if not PySpin.IsAvailable(trigger_source_software) or not PySpin.IsReadable(trigger_source_software):
            print('Unable to set trigger mode (enum entry retrieval). Aborting...')
            return False

        trigger_source.SetIntValue(trigger_source_software.GetValue())
        print('Trigger source set to software...')

        # Turn trigger mode on
        trigger_mode_on = PySpin.CEnumEntryPtr(trigger_mode.GetEntryByName('On'))
        if not PySpin.IsAvailable(trigger_mode_on) or not PySpin.IsReadable(trigger_mode_on):
            print('Unable to enable trigger mode (enum entry retrieval). Aborting...\n')
            return False

        trigger_mode.SetIntValue(trigger_mode_on.GetValue())
        print('Trigger mode turned back on...')

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False

    return result

def grab_next_image_by_trigger(nodemap):
    """
    This function retrieves a single image using the trigger. In this example,
    only a single image is captured and made available for acquisition - as such,
    attempting to acquire two images for a single trigger execution would cause
    the example to hang. This is different from other examples, whereby a
    constant stream of images are being captured and made available for image
    acquisition.

    :param nodemap: Device nodemap to retrieve images from.
    :type nodemap: INodeMap
    :return: True if successful, False otherwise
    :rtype: bool
    """
    try:
        result = True

        # Execute software trigger
        software_trigger_command = PySpin.CCommandPtr(nodemap.GetNode('TriggerSoftware'))
        if not PySpin.IsAvailable(software_trigger_command) or not PySpin.IsWritable(software_trigger_command):
            print('Unable to execute trigger. Aborting...\n')
            return False

        software_trigger_command.Execute()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False

    return result

def reset_trigger(nodemap):
    """
    This function returns the camera to a normal state by turning off trigger mode.

    :param nodemap: Device nodemap to retrieve images from.
    :type nodemap: INodeMap
    :return: True if successful, False otherwise
    :rtype: bool
    """
    try:
        result = True

        # Turn trigger mode back off
        #
        # *** NOTES ***
        # Once all images have been captured, turn trigger mode back off to
        # restore the camera to a clean state.
        trigger_mode = PySpin.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
        if not PySpin.IsAvailable(trigger_mode) or not PySpin.IsWritable(trigger_mode):
            print('Unable to disable trigger mode (node retrieval). Non-fatal error...\n')
            return False

        trigger_mode_off = PySpin.CEnumEntryPtr(trigger_mode.GetEntryByName('Off'))
        if not PySpin.IsAvailable(trigger_mode_off) or not PySpin.IsReadable(trigger_mode_off):
            print('Unable to disable trigger mode (enum entry retrieval). Non-fatal error...\n')
            return False

        trigger_mode.SetIntValue(trigger_mode_off.GetValue())
        print('Trigger mode disabled...\n')

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False

    return result
