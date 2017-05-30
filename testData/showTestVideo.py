import numpy as np
import cv2
import json


def drawRect(frame, rect, zoomfactor=1):
  p1 = (int(rect[0]["x"] * zoomfactor), int(rect[0]["y"] * zoomfactor))
  p2 = (int(rect[1]["x"] * zoomfactor), int(rect[1]["y"] * zoomfactor))
  p4 = (int(rect[2]["x"] * zoomfactor), int(rect[2]["y"] * zoomfactor))
  p3 = (int(rect[3]["x"] * zoomfactor), int(rect[3]["y"] * zoomfactor))
  strokeColor = (0, 255, 0)
  cv2.line(frame, p1, p2, strokeColor, 2)
  cv2.line(frame, p2, p3, strokeColor, 2)
  cv2.line(frame, p3, p4, strokeColor, 2)
  cv2.line(frame, p4, p1, strokeColor, 2)

def main():
  # load json data
  with open("./testData/video_rects.json", "r") as fin:
    rects = json.load(fin)

  cap = cv2.VideoCapture("./testData/video.mp4")

  frameNum = 0
  while(cap.isOpened()):
    frameRect, frame = cap.read()

    # visibleNodes = [ii for ii in rects["rects"] \
    #   if ii["startFrame"] <= frameNum and \
    #   ii["startFrame"] + len(ii["frames"]) >= frameNum ]
    for node in rects["rects"]:
      start = int(node["startFrame"])
      offset = frameNum - start
      if offset < 0 or offset >= len(node["frames"]):
        continue
      # draw rect
      drawRect(frame, node["frames"][offset])

    # show frame number
    frameNumCoord = (20, 40)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(frameNum), frameNumCoord, font, 1, (0, 0, 255))
    cv2.imshow("frame", frame)

    frameNum += 1
    key = cv2.waitKey(40)
    if key == 27 or key & 0xFF == ord("q"):
      break

  cap.release()
  cv2.destroyAllWindows()

if __name__ == "__main__": main()