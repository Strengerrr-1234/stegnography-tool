from PIL import Image

def encode_image(input_image_path, output_image_path, secret_message):
    # Open the input image
    image = Image.open(input_image_path)
    if image.mode != 'RGB':
        raise ValueError("Image mode must be RGB.")
    
    encoded_image = image.copy()
    width, height = image.size
    pixels = encoded_image.load()
    
    # Convert secret message to binary and add a delimiter
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '1111111111111110'
    
    # Check if the image has enough pixels to store the message
    if len(binary_message) > width * height * 3:
        raise ValueError("Image is too small to hold the message.")
    
    # Embed the binary message into the image's pixels
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
    
    # Save the encoded image
    encoded_image.save(output_image_path)
    print("Message encoded and saved to", output_image_path)

def decode_image(encoded_image_path):
    # Open the encoded image
    image = Image.open(encoded_image_path)
    if image.mode != 'RGB':
        raise ValueError("Image mode must be RGB.")
    
    pixels = image.load()
    width, height = image.size
    binary_message = ""
    
    # Extract binary data from the image's pixels
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for i in range(3):  # Extract from R, G, and B channels
                binary_message += str(pixel[i] & 1)
    
    # Split binary data into bytes and decode characters until the delimiter is found
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '11111110':  # Delimiter
            break
        message += chr(int(byte, 2))
    
    print("Decoded message:", message)

# Example usage
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
