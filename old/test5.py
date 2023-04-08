import cv2
theImage = cv2.imread(r'C:\Users\Administrator\Pictures\10-full.jpg', cv2.IMREAD_UNCHANGED)
theImage[0][0] = 255, 0, 0
print(theImage[0][1])
cv2.imwrite(r'C:\Users\Administrator\Pictures\10-full-modified.bmp', theImage)
#cv2.imshow('With watermark', theImage)
#cv2.waitKey(0)
#cv2.imwrite(r'C:\Users\Administrator\Pictures\10-full-modified.jpg', theImage);
#[148 166 165]