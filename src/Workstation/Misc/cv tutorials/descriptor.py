import numpy as np
import cv2

# Load the image


img = cv2.imread('img1.jpg')

# Convert it to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect the SURF key points
surf = cv2.xfeatures2d.SURF_create(hessianThreshold=50000, upright=True, extended=True)
keyPoints, descriptors = surf.detectAndCompute(gray, None)

# Paint the key points over the original image
result = cv2.drawKeypoints(img, keyPoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Display the results
cv2.imshow('Key points', result)
cv2.waitKey(0)
cv2.destroyAllWindows()