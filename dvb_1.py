import cv2
import time


def image_proc():
    img = cv2.imread('img_test.jpg')
    w,h = img.shape[:2]
    (cX,cY) = (w//2,h//2)
    M = cv2.getRotationMatrix2D((cX,cY),45,1.0)
    rotated = cv2.warpAffine(img,M,(w,h))
    cat = img[250:580,20:280]
    # cv2.imshow('image',cat)

    cv2.line(img,(0,0),(580,600),(255,0,0),5)
    cv2.rectangle(img,(384,10),(510,128),(0,255,0),2)
    cv2.putText(img,'DVB-2',(10,500),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),2,cv2.LINE_AA)

    cv2.imshow('image',img)


def video_proc():
    cap = cv2.VideoCapture('sample.mp4')
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(21,21),0)

        ret, thresh = cv2.threshold(gray,105,255,cv2.THRESH_BINARY_INV)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours)>0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            Fr_w,Fr_h = frame.shape[:2]
            cv2.line(frame,(x+w//2,0),(x+w//2,Fr_w),(0,0,255),2)
            cv2.line(frame,(0,y+h//2),(Fr_h,y+h//2),(0,0,255),2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        cv2.imshow('vid',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)

    cap.release()

# image_proc()
video_proc()

# cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()