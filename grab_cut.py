import cv2
import numpy as np

src = cv2.imread("input/test4.jpg")
src = cv2.resize(src, (0, 0), fx=0.5, fy=0.5)#缩放，宽高缩短到原来的一半

# 交互式，返回 (x_min, y_min, w, h)
r = cv2.selectROI('input', src, True)

# roi区域
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
#result转为四通道
b_channel,g_channel,r_channel=cv2.split(result)
alpha_channel=np.ones(b_channel.shape,dtype=b_channel.dtype)*255
result_BGAR=cv2.merge((b_channel,g_channel,r_channel,alpha_channel))
#result[np.all(result==[0,0,0,255],axis=2)]=[0,0,0,0]
result_BGAR[np.all(result_BGAR == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]

#输出剔除前景之后的后景
# back=src
# for i in range(src.shape[0]):
#     for j in range(src.shape[1]):
#         if(back[i,j,0]==result[i,j,0] and back[i,j,1]==result[i,j,1] and back[i,j,2]==result[i,j,2]):
#             back[i,j]=[255,255,255]




#cv2.imshow('back',back)
#cv2.imshow('mask', mask2)
cv2.imshow('roi', roi) 
cv2.imshow("result", result)
#保存前景和提取后的图片
cv2.imwrite('result/test4_re.png',result_BGAR)
#cv2.imwrite('testorigin_back.png',back)
cv2.waitKey(0)
cv2.destroyAllWindows()
