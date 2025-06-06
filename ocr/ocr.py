import cv2
import pytesseract
from PIL import Image
import numpy as np

# --- Configuration ---
# Specify the path to the Tesseract executable (change this if Tesseract is not in your PATH)
# For Windows, it might look like: r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# For Linux/macOS, if installed via package manager, it's usually in PATH and not needed.
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' # Adjust this path if needed

def read_distorted_text(image_path):
    """
    Loads an image, applies pre-processing, and attempts to read text using Tesseract OCR.
    """
    try:
        # 1. Load the image using OpenCV
        img = cv2.imread(image_path)

        if img is None:
            print(f"Error: Could not load image from {image_path}")
            return None

        # 2. Convert to Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Apply Thresholding (Binarization)
        # Using Otsu's thresholding for better results on varying lighting/noise
        # You might need to experiment with different thresholding methods and values.
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Invert the image if text is black on white (Tesseract often prefers white text on black background)
        # This particular image seems to be dark text on light background, so THRESH_BINARY_INV is good.
        # If text was white on black, you might use THRESH_BINARY and then invert later if needed.

        # 4. Noise Reduction
        # Median blur is effective for salt-and-pepper noise (the scattered dots)
        denoised = cv2.medianBlur(thresh, 3) # Kernel size 3 or 5 usually works well

        # 5. Optional: Morphological Operations (to clean up text/noise further)
        # Dilate to make characters thicker and fill small gaps, then erode to thin them back
        # This can help connect broken characters and remove small artifacts.
        kernel = np.ones((2, 2), np.uint8) # Adjust kernel size based on character thickness
        dilated = cv2.dilate(denoised, kernel, iterations=1)
        eroded = cv2.erode(dilated, kernel, iterations=1)

        # You can save the pre-processed image to inspect it
        # cv2.imwrite("preprocessed_image.png", eroded)
        # print("Pre-processed image saved as preprocessed_image.png")

        # 6. Pass the pre-processed image to Tesseract
        # Convert OpenCV image (NumPy array) to PIL Image, as pytesseract sometimes prefers it
        pil_image = Image.fromarray(eroded)

        # Use Tesseract to do OCR on the image
        # config='--psm 6' means assuming a single uniform block of text.
        # You might experiment with different psm (page segmentation mode) values.
        # For a single line of text, --psm 7 is often good.
        # For general text, --psm 3 (default) or --psm 6.
        # For noisy characters like this, trying different PSMs is key.
        text = pytesseract.image_to_string(pil_image, config='--psm 6')

        print(text)
        return text.strip() # .strip() removes leading/trailing whitespace

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Main execution ---
image_file = 'test_captcha.png'  # Replace with your image file path

recognized_text = read_distorted_text(image_file)

if recognized_text:
    print(f"\nRecognized Text: '{recognized_text}'")
else:
    print("\nText recognition failed.")