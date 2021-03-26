# auto_cut
自动抠图，可选取感兴趣区域，一键扣取前景，可通过标记前景/后景进行迭代微调  
基于https://github.com/zihuaweng/Interactive-image-segmentation-opencv-qt 修改  
使用方法：  
0、安装requirements.txt文件中的依赖项  
1、运行app.py  
2、点击**导入图片**按钮，选择原图片  
3、点击**指定区域**按钮，框选包含目标内容的矩形区域  
4、点击**迭代一次**按钮，在输出结果窗口查看结果，如果看不到，请适当拖拽结果窗口  
5、点击**标记微调**按钮，鼠标会变成画笔，按住左键标记前景；按住右键标记背景  
6、每次标记后，可以点击**迭代一次**继续迭代  
7、效果满意后点击保存，选择保存路径保存提取结果  

**新增功能** 使用attnGAN根据描述生成图片，目前仅支持鸟类图片
使用方法：  
1、按照https://github.com/taoxugit/AttnGAN 下载数据集到AttnGAN项目中的指定文件夹中  
2、点击**生成图片**按钮  
3、选择类别为bird  
4、输入描述鸟类特征的句子，示例：this bird is red with white and has a very short beak  
5、等待图片生成  
