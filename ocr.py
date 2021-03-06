import os
from urllib import request

class Ocr():

    """ 页面切割模式
    Page segmentation modes:
    0    Orientation and script detection (OSD) only.
    1    Automatic page segmentation with OSD.
    2    Automatic page segmentation, but no OSD, or OCR.
    3    Fully automatic page segmentation, but no OSD. (Default)
    4    Assume a single column of text of variable sizes.
    5    Assume a single uniform block of vertically aligned text.
    6    Assume a single uniform block of text.
    7    Treat the image as a single text line.
    8    Treat the image as a single word.
    9    Treat the image as a single word in a circle.
    10   Treat the image as a single character.
    """

    def __init__(self, ocr_path, *, out_path=None, mode=3, delete=True):
        """
        :param ocr_path: tesseract 引擎的安装路径
        :param out_path: 输出文件路径
        :param mode: 图片的切割模式
        :param delete: 是否保留生成的文本文件
        """
        self._ocrpath = ocr_path
        self._outpath = out_path
        self._mode = mode
        self._delete = delete

    def exec(self, *, img_path="", img_url=None):
        """ 执行命令
        :param img_path: 本地图片路径
        :param img_url: 网络图片地址
        """
        img = r"D:\img.jpg"
        if os.path.exists(img_path):
            img = img_path
        else:
            try:
                request.urlretrieve(img_url, img)
            except Exception as e:
                print(e)
        if self._outpath is None:
            self._outpath = r"D:\result"
        elif self._outpath.endswith(".txt"):
            self._outpath = self._outpath[:-4]
        if self._mode > 10 or self._mode < 0:
            self._mode = 3
        os.chdir(self._ocrpath)
        cmd = r'tesseract.exe {img} {out} -psm {mode}'.\
            format(img=img, out=self._outpath, mode=self._mode)
        os.system(cmd)
        try:
            with open(self._outpath + ".txt", "r") as f:
                result = f.read().strip()
            if self._delete:
                os.remove(self._outpath + ".txt")
                os.remove(r"D:\img.jpg")
            return result
        except IOError:
            print("无法找到该文件!")
        return None

if __name__ == "__main__":
    ocr = Ocr(r'C:\Program Files\Tesseract-OCR')
    result = ocr.exec(img_path=r"e:\python\pyocr\images\1.png")
    print(result)