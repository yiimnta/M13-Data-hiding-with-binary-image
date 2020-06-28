import cv2
import numpy as np
import io

class Util:

    def convertImageToBinaryImage(self, path):
        np_img = self.convertImageToBlackWhiteImage(path)
        return  np.where(np_img == 255, 1, 0)

    def convertImageToBlackWhiteImage(self, path):
        img = cv2.imread(path, 0)
        mat, bw = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)
        return np.array(bw)#black and white

    def convertBinaryMatrixToBinaryImage(self, matrix):
        matrix = np.where(matrix == 1, 255, 0)
        return matrix

    def convertMatrixToImage(self, matrix, path):
        cv2.imwrite(path, matrix)

    def convertTextToBinary(self, s):
        st = ' '.join(format(ord(x), '08b') for x in s)
        return st
    def matrixMul(self, m1, m2):
        rs = []
        for i in range(len(m1)):
            ar = []
            for j in range(len(m1)):
                if m1[i][j] == 0:
                    ar.append(0)
                else:
                    ar.append(m2[i][j])
            rs.append(ar)
        return rs

    def maxTrixChangeBit(self, m, pos):
        m = np.array(m)
        for i in range(len(pos)):
            x = pos[i][0]
            y = pos[i][1]

            val = 0
            if m[x][y] == 0:
                val = 1
            m[x][y] = val

        return np.matrix(m)

    def encode(self, f, k, w, bit):
        t = np.array(np.bitwise_xor(f, k))
        #convert matrix to array
        f = np.array(f)
        k = np.array(k)
        #sum * w
        s = self.matrixMul(t, w)

        #sum s
        su = np.sum(s)

        #get d
        d = (int(bit, 2) - su) % pow(2, len(bit))
        posBitwise = []
        r = len(bit)

        if d != 0:
            jk = self.calcS(w,t,d,r)
            if jk is not None:
                posBitwise.append(jk)
            else:
                #tim so tu nhien h in {1,2,3,..2r-1} nho nhat sao cho Shd != null va Sd-hd != null
                for h in range(1,pow(2,r) - 1):
                    jk = self.calcS(w,t,h,r)
                    if jk is not None:
                        h2 = pow(2,r) + (d-h)
                        uv = self.calcS(w,t,h2,r)
                        if uv is not None:
                            posBitwise.append(jk)
                            posBitwise.append(uv)
                            break

        return self.maxTrixChangeBit(f,posBitwise)

    def calcS(self, w, t, d, r):
        for i in range(len(t)):
            if d in w[i]:
                pos = w[i].index(d)
                if t[i][pos] == 0:
                    return [i, pos]
            elif (pow(2, r) - d) in w[i]:
                pos = w[i].index((pow(2, r) - d))
                if t[i][pos] == 1:
                    return [i, pos]
        return None

    def decode(self, f, k, w, r):

        t = np.array(np.bitwise_xor(f, k))
        # convert matrix to array
        f = np.array(f)
        k = np.array(k)
        w = np.array(w)

        # sum
        t = np.array(t)

        # sum * w
        s = self.matrixMul(t, w)

        # sum s
        su = np.sum(s)

        # print(su % (pow(2,)))
        result = (su % (pow(2, r)))
        return format(result, '08b')

    def runEncode(self, pathImg, pathText ):
        fo = io.open(pathText, "r", encoding="utf8")
        text = fo.read()
        fo.close()
        text = text + codeToEndDecode
        st = self.convertTextToBinary(text).split(" ")
        f_matrix = self.convertImageToBinaryImage(pathImg)
        x = 0
        y = 0
        i = 0
        ele = 16
        max_size_h = np.size(f_matrix, 1)
        max_size_v = np.size(f_matrix, 0)
        sss = ""
        for bit in st:

            f = f_matrix[y * ele:y * ele + ele, x * ele: x * ele + ele]
            r = 8
            f = self.encode(f, k, w, bit)
            f_matrix[y * ele:y * ele + ele, x * ele: x * ele + ele] = np.matrix(f)
            f = f_matrix[y * ele:y * ele + ele, x * ele: x * ele + ele]
            x += 1
            if (x * ele + ele > max_size_h):
                y += 1
                x = 0
            if (y * ele + ele > max_size_v):
                break
        return self.convertBinaryMatrixToBinaryImage(f_matrix)

    def runDecode(self, pathImg):
        f_matrix = self.convertImageToBinaryImage(pathImg)
        x = 0
        y = 0
        i = 0
        ele = 16
        max_size_h = np.size(f_matrix, 1)
        max_size_v = np.size(f_matrix, 0)
        result = ""
        while 1==1:
            r = 8
            f = f_matrix[y * ele:y * ele + ele, x * ele: x * ele + ele]
            dc = self.decode(f, k, w, r)
            num = int(dc, 2)
            result += chr(num)
            x += 1
            if (x * ele + ele > max_size_h):
                y += 1
                x = 0

            if y * ele + ele > max_size_v:
                break

            if codeToEndDecode in result:
                result = result[:-len(codeToEndDecode)]
                break
        return result


k = np.matrix([[1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],    #1
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],   #2
                [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],   #3
                [1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0],   #4
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0],   #5
                [0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],   #6
                [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],   #7
                [1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],   #8
                [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1],   #9
                [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0],   #10
                [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],   #11
                [0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],   #12
                [1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],   #13
                [1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],   #14
                [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1],   #15
                [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0]])  #16

w = [[208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223],                 #1
    [8, 1, 2, 3, 4, 5, 6, 7, 1, 9, 10, 11, 12, 13, 14, 15],                             #2
    [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47],                   #3
    [144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159],   #4
    [240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255],   #5
    [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63],                   #6
    [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95],                   #7
    [192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207],   #8
    [96, 97, 98, 99, 100, 101, 102, 103, 104, 1, 106, 107, 108, 109, 110, 111],         #9
    [128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143],   #10
    [16, 17, 18, 19, 20, 1, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],                    #11
    [160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175],   #12
    [64, 65, 66, 67, 68, 69, 70, 71, 72, 1, 74, 75, 76, 77, 78, 79],                    #13
    [176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191],   #14
    [224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239],   #15
    [112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 1, 126, 127]]     #16

codeToEndDecode = "Truong.Nguyen@Student.HTW-Berlin.de"


#util = Util()
# img = util.runEncode("./img/demo.jpg","input.txt")
# util.convertMatrixToImage(img,"./output/test.jpg")
# text = util.runDecode("./output/test.jpg")
# file = open("./output/test.txt","w")
# file.write(text)
# file.close()