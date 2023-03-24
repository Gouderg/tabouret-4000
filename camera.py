import depthai as dai

class Camera:
    def __init__(self):
        self.setup()

    def setup(self):
        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Define source and output
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        self.xoutRgb = self.pipeline.create(dai.node.XLinkOut)

        self.xoutRgb.setStreamName("rgb")

        # Properties
        self.camRgb.setPreviewSize(640, 640)
        self.camRgb.setInterleaved(False)
        self.camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

        # Linking
        self.camRgb.preview.link(self.xoutRgb.input)
    
    def printInformation(self, deviceCamera):
        print('Connected cameras:', deviceCamera.getConnectedCameraFeatures())
        # Print out usb speed
        print('Usb speed:', deviceCamera.getUsbSpeed().name)
        # Bootloader version
        if deviceCamera.getBootloaderVersion() is not None:
            print('Bootloader version:', deviceCamera.getBootloaderVersion())
        # Device name
        print('Device name:', deviceCamera.getDeviceName())