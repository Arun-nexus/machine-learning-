import cv2

cap = cv2.VideoCapture(0)
cropping = False
ix, iy = -1, -1
ex, ey = -1, -1
rectangles = []
frame = None

def crop(event, x, y, flags, params):
    global cropping, ix, iy,ex,ey, frame, rectangles

    if event == cv2.EVENT_LBUTTONDOWN:
        cropping = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            temp = frame.copy()
            cv2.rectangle(temp, (ix, iy), (x, y), (0, 0, 255), 2)
            cv2.imshow("windows", temp)

    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        ex=x
        ey=y
        rectangles.append([ix, iy, ex, ey])
        cv2.rectangle(frame, (ix, iy), (ex, ey), (0, 0, 255), 2)

        for i in rectangles:
            if i[2] > -1 and i[3] > -1:
                cropped_image = frame[min(i[1], i[3]):max(i[1], i[3]), min(i[0], i[2]):max(i[0], i[2])]
                cv2.imshow(f"rectangle{i}",mat=cropped_image)

cv2.namedWindow("windows")
cv2.setMouseCallback("windows", crop)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("windows", frame)



    if cv2.waitKey(1) & 0xFF == ord("x"):
        break

cap.release()
cv2.destroyAllWindows()
