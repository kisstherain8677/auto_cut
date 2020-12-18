import cv2
import numpy as np
from tools.FormatCvt import FormatCvt
#接收图像进行操作
class PicProcess:

    def __init__(self,pixmap):
        self.pixmap=pixmap


    def grab_cut(self,r):#r是rect
        src=FormatCvt.qtpixmap_to_cvimg(self.pixmap)
        roi = src[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        # 原图mask，与原图等大小
        mask = np.zeros(src.shape[:2], dtype=np.uint8)

        # 矩形roi
        rect = (int(r[0]), int(r[1]), int(r[2]), int(r[3]))  # 包括前景的矩形，格式为(x,y,w,h)

        # bg模型的临时数组
        bgdmodel = np.zeros((1, 65), np.float64)
        # fg模型的临时数组
        fgdmodel = np.zeros((1, 65), np.float64)

        cv2.grabCut(src, mask, rect, bgdmodel, fgdmodel, 11, mode=cv2.GC_INIT_WITH_RECT)

        print(np.unique(mask))
        # 提取前景和可能的前景区域
        mask2 = np.where((mask == 1) | (mask == 3), 255, 0).astype('uint8')

        print(mask2.shape)

        # 按位与 src & src == 0，得到的是二进制
        result = cv2.bitwise_and(src, src, mask=mask2)
        # cv2.imwrite('result.jpg', result)
        # cv2.imwrite('roi.jpg', roi)
        # result转为四通道
        b_channel, g_channel, r_channel = cv2.split(result)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        result_BGAR = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        # result[np.all(result==[0,0,0,255],axis=2)]=[0,0,0,0]
        result_BGAR[np.all(result_BGAR == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
        return result_BGAR

