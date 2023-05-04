import cv2
import numpy as np


def adjust_value_in_range(img, gray_img, value_range, amount):
    # Mask image to only select browns
    mask = cv2.inRange(gray_img, value_range[0], value_range[1])

    # define the alpha and beta
    alpha = 1 # Contrast control
    beta = amount # Brightness control

    # call convertScaleAbs function
    img[mask > 0] = cv2.convertScaleAbs(img[mask > 0], alpha=alpha, beta=beta)

    return img

def adjust_value(hsv_img, value, adjustment):
    h, s, v = cv2.split(hsv_img)

    v = v + (255 - abs(value - v)) * adjustment / 255

    v = np.minimum(np.maximum(v, 0), 255)
    final_hsv = cv2.merge((h, s, v.astype(np.uint8)))
    return final_hsv


# Open the video file
cap = cv2.VideoCapture('C:\\Programming\\test_ffmpeg\\constantInput.mp4')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Create a VideoWriter object to write the adjusted frames
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('C:\\Programming\\test_ffmpeg\\constant_handbrake_input_darker_light_fix_sat_too.mp4', fourcc, fps, (width, height))

target_hue = 0
target_saturation = 0
target_value = 100
# target_value_list = []

frame_count = 0
while True:
    grabbed, frame = cap.read()

    if grabbed == False:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # mean_hue = cv2.mean(hsv[:, :, 0])[0]
    mean_saturation = cv2.mean(hsv[:, :, 1])[0]
    mean_value = cv2.mean(hsv[:, :, 2])[0]

    # print(mean_value)
    
    # if target_hue == 0:
    #     target_hue = mean_hue
    
    if target_saturation == 0:
        target_saturation = mean_saturation
    
    if target_value == 0:
        target_value = mean_value

    # hue_difference = int(target_hue) - int(mean_hue)
    saturation_difference = int(target_saturation) - int(mean_saturation)
    value_difference = int(target_value) - int(mean_value)

    # # define the alpha and beta
    # alpha = 1 # Contrast control
    # beta = value_difference # Brightness control

    h, s, v = cv2.split(hsv)
    
    # h = h.astype(np.int16)
    # h += hue_difference
    # h[h > 255] = 255
    # h[h < 0] = 0

    s = s.astype(np.int16)
    s += saturation_difference
    s[s > 255] = 255
    s[s < 0] = 0

    v = v.astype(np.int16)
    v += value_difference
    v[v > 255] = 255
    v[v < 0] = 0

    hsv = cv2.merge((h.astype(np.uint8), s.astype(np.uint8), v.astype(np.uint8)))

    # print(frame_count)
    frame_count += 1
    if frame_count % 50 == 0:
        print("   " + str(frame_count / total_frame_count * 100) + "%", end="\r")
        # frame

    # area = ((0, 300), (0, 300))
    
    # value_list = [hsv[300, 450, 2], hsv[100, 700, 2], hsv[400, 100, 2]]

    # for y in range(*area[1], 20):
    #     for x in range(*area[0], 20):
    #         value = hsv[x, y, 2]
    #         if value not in value_list:
    #             value_list.append(value)
    # value_list.sort()
    # print(value_list)
    # input()

    # if target_value_list == []:
    #     # target_value_list = [hsv[300, 450, 2], hsv[100, 700, 2], hsv[400, 100, 2]]
    #     target_value_list = [hsv[500, 100, 2], hsv[800, 470, 2]]
    # else:
    #     for target_value, value_xy in zip(target_value_list, [(500, 100), (800, 470)]):
    #         value = hsv[value_xy[0], value_xy[1], 2]
    #         difference = int(target_value) - int(value)
    #         if difference == 0:
    #             continue
    #         # print(difference)
    #         hsv = adjust_value(hsv, value, difference)
    #         # frame = adjust_value_in_range(frame, gray, sorted([int(previous_value), int(value)]), difference)
    #         print(target_value)
    #         print(value)
    #         print(hsv[value_xy[0], value_xy[1], 2])
    #     print()

    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    out.write(bgr)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # mean_value = cv2.mean(gray)[0]
    
    # if target_brightness == 0:
    #     target_brightness = mean_value

    # print(target_brightness, mean_value)

    # color_difference = int(target_brightness) - int(mean_value)

    # # define the alpha and beta
    # alpha = 1 # Contrast control
    # beta = color_difference # Brightness control

    # # call convertScaleAbs function
    # adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # area = ((0, 200), (0, 1080))
        
    # if target_value_list == []:
    #     position_list = []
    #     for y in range(*area[1], 10):
    #         for x in range(*area[0], 10):
    #             value = gray[x, y]
    #             # if value not in position_list:
    #             position_list.append((value, x, y))
    #     unique_dict = {item[0]: item for item in position_list}
    #     position_list = list(unique_dict.values())
    #     position_list.sort(key=lambda x: x[0])
    #     value_list = [gray[i[1], i[2]] for i in position_list]
    #     target_value_list = value_list
    # else:
    #     value_list = [gray[i[1], i[2]] for i in position_list]
    

    # previous_value = None
    # for target_value, value in zip(target_value_list, value_list):
    #     if previous_value == None:
    #         previous_value = value
    #         continue
    #     difference = int(target_value) - int(value)
    #     if difference == 0:
    #         previous_value = value
    #         continue
    #     # print(difference)
    #     frame = adjust_value_in_range(frame, gray, sorted([int(previous_value), int(value)]), difference)
    #     previous_value = value

    # write the adjusted frame
    # out.write(frame)

    # print(frame_count)
    # frame_count += 1

cap.release()
out.release()
cv2.destroyAllWindows()