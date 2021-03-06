import cv2

from random import randint

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
# Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()

    elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()

    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()

    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()

    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()

    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()

    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()

    elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None

    print('Incorrect tracker name')
    print('Available trackers are:')


    for t in trackerTypes:
        print(t)

    return tracker

bboxes = []

colors = []


cap = cv2.VideoCapture(0)

# tracker = cv2.TrackerMOSSE_create()
# tracker = cv2.TrackerCSRT_create()
# tracker = createTrackerByName('CSRT')
# success, img = cap.read()
# bbox = cv2.selectROI("Tracking",img,False)
# tracker.init(img,bbox)

while True:
    success, frame = cap.read()

    bbox = cv2.selectROI('MultiTracker', frame,False,False)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))

    print("Press q to quit selecting boxes and start tracking")
    print("Press any other key to select next object")

    k = cv2.waitKey(0) & 0xFF
    if(k == 113):
        break
print('Selected bounding boxes {}'.format(bboxes))

# Specify the tracker type
trackerType = "CSRT"

# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()

# Initialize MultiTracker
for bbox in bboxes:
    multiTracker.add(createTrackerByName(trackerType), frame, bbox)

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        break

   # get updated location of objects in subsequent frames
    success, boxes = multiTracker.update(frame)

# draw tracked objects

    for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

# show frame

    cv2.imshow('MultiTracker', frame)

# quit on ESC button

    if cv2.waitKey(1) & 0xFF== 27: # Esc pressed
        break