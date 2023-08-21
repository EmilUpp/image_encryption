# Python code to read image
import math

import cv2
import numpy as np

# To read image from disk, we use
# cv2.imread function, in below method,
img = cv2.imread("pride.png", cv2.IMREAD_COLOR)
#img = cv2.resize(img, [200, 200])

img_2 = cv2.imread("pride.png", cv2.IMREAD_COLOR)
#img_2 = cv2.resize(img_2, [200, 200])


def encrypt_2(image, message, alphabet):
    total_pixel_count = 0
    for i, row in enumerate(image):
        if total_pixel_count >= len(message):
            break
        for j, col in enumerate(image[row]):
            if total_pixel_count >= len(message):
                break
            for k, pix in enumerate(image[col]):
                if total_pixel_count >= len(message):
                    break

                current_value = image[i][j][k]
                try:
                    letter_index = alphabet.index(message[total_pixel_count].lower())
                except ValueError:
                    print("Unkown char: " + message[total_pixel_count])
                    total_pixel_count += 1
                    continue

                current_value = add_to_value(current_value, letter_index)

                if total_pixel_count == 0:
                    image[0][0][0] = add_to_value(image[0][0][0], len(message))
                else:
                    image[i][j][k] = current_value

                total_pixel_count += 1

    return image


def encrypt(image, message, alphabet, spacing=1, number_of_digits=5):
    pixel_list = image.flatten()
    print(len(pixel_list))

    if len(message) * spacing > len(pixel_list):
        print("true")
        spacing = math.floor(len(pixel_list) - (number_of_digits + 1)/ len(message))

    #pixel_list[0] = add_to_value(pixel_list[0], len(message) + 1)
    pixel_list = encrypt_length(pixel_list, message, number_of_digits)

    pixel_list[number_of_digits] = add_to_value(pixel_list[number_of_digits], spacing)

    for i, current_value in enumerate(pixel_list[number_of_digits+1::spacing]):
        if i >= len(message):
            break

        try:
            letter_index = alphabet.index(message[i].lower())
        except ValueError:
            print("Unkown char: " + message[i])
            continue

        current_value = add_to_value(current_value, letter_index)

        pixel_list[i*spacing + number_of_digits + 1] = current_value

    pixel_list = np.reshape(pixel_list, image.shape)

    return pixel_list


def encrypt_length(pixel_list, message, number_of_digits):
    digits = str(len(message))
    digits = digits.zfill(number_of_digits)

    for i in range(number_of_digits):
        pixel_list[i] = add_to_value(pixel_list[i], int(digits[i]))

    return pixel_list


def add_to_value(current_value, letter_index):
    if current_value - letter_index < 0:
        current_value += letter_index
    elif current_value + letter_index > 255:
        current_value -= letter_index
    else:
        current_value += letter_index
    return current_value


def around_corner(value, threshold=124):
    if value > threshold:
        return 256 - value
    else:
        return value


def decrypt(key, encrypted, number_of_digits):
    combined = encrypted - key
    combined_flat = combined.flatten()

    message_length = int("".join([str(_) for _ in combined_flat[:number_of_digits]]))
    print(combined_flat[:number_of_digits])

    # end = (around_corner(message_length) - 1) * around_corner(combined_flat[5])
    end = (message_length) * around_corner(combined_flat[number_of_digits])

    if around_corner(combined_flat[number_of_digits]) <= number_of_digits+1:
        end += number_of_digits+1
    for each in combined_flat[number_of_digits+1:end:around_corner(combined_flat[number_of_digits])]:
        each = around_corner(each, len(alphabet))

        print(alphabet[each], end="")


def read_file(filename):
    with open(filename, "r") as file_handler:
        content = file_handler.read()

    return content


bible = read_file("bible.txt")

print(len(bible))
message = bible
alphabet = "abcdefghijklmnopqrstuvwxyzåäö ,.¬!?;\n:'1234567890\"()-"
print(len(message))

img_2 = encrypt(img_2, message, alphabet, 2, 8)

cv2.imwrite("encrypted.png", img_2)

decrypt(img, img_2, 8)

# concatenate image Horizontally
Hori = np.concatenate((img, img_2), axis=1)

cv2.imshow('HORIZONTAL', Hori)

cv2.waitKey(0)
cv2.destroyAllWindows()