# stegnography-tool
A code that uses the Pillow library to implement a basic steganography tool. The tool can hide text data within an image file by modifying the least significant bits of pixel values.

This Python script performs image-based steganography using the Pillow library. It can encode a secret message into an image or decode a message hidden in an image.

## 1. Import Required Library
```
from PIL import Image
```
* `Pillow`: A library for image processing in Python.
* The script uses `Image` to open, manipulate, and save images.


## 2. Encode Function
### 2.1 Input Parameters
```
def encode_image(input_image_path, output_image_path, secret_message):
```
* `input_image_path`: Path to the original image where the message will be hidden.
* `output_image_path`: Path to save the encoded image.
* `secret_message`: The message to hide in the image.
  
### 2.2 Open the Image
```
image = Image.open(input_image_path)
if image.mode != 'RGB':
    raise ValueError("Image mode must be RGB.")
```
* Opens the image using `Pillow`.
* Ensures the image mode is **RGB** (3 color channels: Red, Green, and Blue).

### 2.3 Prepare for Encoding
```
encoded_image = image.copy()
width, height = image.size
pixels = encoded_image.load()
```
* Creates a copy of the input image.
* Retrieves image dimensions (`width`, `height`) and pixel data (`pixels`).

### 2.4 Convert Message to Binary
```
binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '1111111111111110'
```
* Converts each character of the secret message to an 8-bit binary representation using `format(ord(char), '08b')`.
* Appends a delimiter `1111111111111110` to indicate the end of the message.

### 2.5 Check Image Capacity
```
if len(binary_message) > width * height * 3:
    raise ValueError("Image is too small to hold the message.")
```
* Ensures the image has enough pixels to hold the binary message.
* Each pixel can store 3 bits (one in each RGB channel).

### 2.6 Embed Binary Message
```
data_index = 0
for y in range(height):
    for x in range(width):
        pixel = list(pixels[x, y])
        for i in range(3):  # Modify R, G, and B channels
            if data_index < len(binary_message):
                pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index])
                data_index += 1
        pixels[x, y] = tuple(pixel)
        if data_index >= len(binary_message):
            break
    if data_index >= len(binary_message):
        break
```
* Iterates through each pixel and modifies the least significant bit (LSB) of its RGB channels to store bits of the binary message.
* Uses `pixel[i] & ~1` to clear the LSB and `| int(binary_message[data_index])` to set it.

2.7 Save the Encoded Image
```
encoded_image.save(output_image_path)
print("Message encoded and saved to", output_image_path)
```
* Saves the modified image with the secret message embedded.


## 3. Decode Function
### 3.1 Input Parameters
```
def decode_image(encoded_image_path):
```
* `encoded_image_path`: Path to the image containing the hidden message.

3.2 Open the Image
```
image = Image.open(encoded_image_path)
if image.mode != 'RGB':
    raise ValueError("Image mode must be RGB.")
```
* Opens the encoded image and ensures it is in RGB mode.

3.3 Extract Binary Data
```
pixels = image.load()
width, height = image.size
binary_message = ""

for y in range(height):
    for x in range(width):
        pixel = pixels[x, y]
        for i in range(3):  # Extract from R, G, and B channels
            binary_message += str(pixel[i] & 1)
```
* Iterates through the pixels, extracting the LSBs of the RGB channels to reconstruct the binary message.

3.4 Convert Binary to Text
```
message = ""
for i in range(0, len(binary_message), 8):
    byte = binary_message[i:i+8]
    if byte == '11111110':  # Delimiter
        break
    message += chr(int(byte, 2))
```
* Divides the binary message into 8-bit chunks.
* Converts each chunk from binary to a character using `chr(int(byte, 2))`.
* Stops decoding when the delimiter `11111110` is found.

3.5 Print the Decoded Message
```
print("Decoded message:", message)
```
* Prints the hidden message retrieved from the image.


## 4. Main Program
```
if __name__ == "__main__":
    option = input("Choose an option: 1 (Encode) or 2 (Decode): ").strip()
    if option == "1":
        input_image = input("Enter the path of the image to encode: ").strip()
        output_image = input("Enter the path to save the encoded image: ").strip()
        secret_message = input("Enter the secret message: ").strip()
        encode_image(input_image, output_image, secret_message)
    elif option == "2":
        encoded_image = input("Enter the path of the encoded image: ").strip()
        decode_image(encoded_image)
    else:
        print("Invalid option!")
```
* Asks the user whether to encode or decode a message.
* Collects inputs for file paths and the message.
* Calls the appropriate function based on the user's choice.


## Summary

### 1. Encoding:
  * Converts a message into binary and embeds it in an image's LSBs.
  * Saves the modified image.
### 2. Decoding:
  * Extracts LSBs from the image to reconstruct the binary message.
  * Converts binary back into text and displays the hidden message.

This script is a simple and effective implementation of **LSB steganography**.
