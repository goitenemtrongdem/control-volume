import cv2
import mediapipe as mp
import time
import math
import hand as htm
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolumeâ
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import numpy as np
cam=cv2.VideoCapture(0)
pTime=0
detector=htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# print(f"Audio output: {devices.FriendlyName}")a
# print(f"- Muted: {bool(volume.GetMute())}")
# print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")     # min -65.25  max 0
current_volume_db = volume.GetMasterVolumeLevel()
# print(f"Âm lượng hiện tại: {current_volume_db:.2f} dB")
minVol= -65.25
maxVol= 0
while True:
    ret,frame=cam.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    if len(lmList)!=0:
    # giao dien
       x1,y1=lmList[4][1],lmList[4][2]
       x2, y2 = lmList[8][1], lmList[8][2]
       cv2.circle(frame,(x1,y1),15,(255,0,26),-1)
       cv2.circle(frame, (x2,y2),15,(255, 0, 26), -1)
       cv2.line(frame,(x1,y1),(x2,y2),(255, 0, 26),3)
       x=(x1+x2)//2
       y=(y1+y2)//2
       cv2.circle(frame, (x, y), 15, (255, 0, 26), -1)
       khoangcach=math.hypot(x2-x1,y2-y1)   # min 14   max 170
       # print(khoangcach)
       vol = np.interp(khoangcach, [14, 170], [minVol, maxVol])
       display=np.interp(khoangcach, [14, 170], [250, 70])
       von_type=np.interp(khoangcach, [14, 170], [0, 100])
       volume.SetMasterVolumeLevel(vol, None)
       if khoangcach<30:
           cv2.circle(frame, (x, y), 15, (0, 0, 0), -1)
       cv2.rectangle(frame, (30, 70), (90, 250), (23, 25, 78), 3)
       cv2.rectangle(frame, (30, int(display)), (90, 250), (23, 25, 78), -1)
       cv2.putText(frame, f"{int(von_type)}%", (31, 299), cv2.FONT_HERSHEY_PLAIN, 3, (25, 4, 100), 3)
    # dis = np.interp(current_volume_db, [-65.25, 0], [250, 70])
    # cv2.rectangle(frame, (30, 70), (90, 250), (23, 25, 78), 3)
    # cv2.rectangle(frame, (30, int(dis)), (90, 250), (23, 25, 78), -1)
    # hien thi fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f"FPS: {int(fps)}", (130, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("cua so cam",frame)
    if cv2.waitKey(1) & 0xFF == ord('a'):
           break
cam.release()
cv2.destroyAllWindows()

