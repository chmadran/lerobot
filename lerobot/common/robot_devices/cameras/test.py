from lerobot.common.robot_devices.cameras.opencv import OpenCVCamera

camera = OpenCVCamera(camera_index=0, fps=30, width=640, height=480)
camera.connect()
color_image = camera.read()

print(color_image.shape)
print(color_image.dtype)