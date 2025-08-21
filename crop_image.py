import  cv2

img=cv2.imread(r"C:\Users\Arun\OneDrive\Pictures\Screenshots 1\Screenshot 2025-08-01 020521.png")
img=cv2.resize(img,(500,500))

drawing = False
ix,iy=-1,-1

def draw(event,x,y,flags,params):
    global ix,iy,drawing,img
    if event==1:
        drawing = True
        ix=x
        iy=y
    elif event ==4:
        drawing=False
        cv2.rectangle(img,(ix,iy),(x,y),color=(0,0,255),thickness=1)
        x1,x2=min(ix,x),max(ix,x)
        y1,y2=min(iy,y),max(iy,y)

        cropped_img=img[y1:y2,x1:x2]

        cv2.imshow("new_window",cropped_img)
        cv2.waitKey(0)


cv2.namedWindow("window")
cv2.setMouseCallback("window",draw)

while True:
    cv2.imshow("window",img)
    if cv2.waitKey(1) & 0xFF == ord("y"):
        break

cv2.destroyAllWindows()