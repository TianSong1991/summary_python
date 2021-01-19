import mmap
import contextlib
import struct
import time
import numpy as np
from data_analysis_python.FrequencyAnalysisUtil import convertToFrequency
from tensorflow import keras
from data_analysis_python.TrainingDataUtil import readConfigFile
import os
while True:
  time.sleep(0.01)
  with contextlib.closing(mmap.mmap(-1, 6, tagname="matlab", access=mmap.ACCESS_WRITE)) as f:
    f.tell()
    s0 = f.read()

    print("type = " + str(s0[0]))
    print("status = " + str(s0[1]))
    print("length = " + str(s0[2]+s0[3]*256+s0[4]*256*256+s0[5]*256*256*256))
    print(len(s0))

    s_length = int(s0[2]+s0[3]*256+s0[4]*256*256+s0[5]*256*256*256)

    if s0[0] != 1:
      print("type != 1")
      continue

    with contextlib.closing(mmap.mmap(-1, 6 + s_length, tagname="matlab", access=mmap.ACCESS_WRITE)) as m:
      m.tell()
      s = m.read()

      if (len(s) - 6) != int(s[2] + s[3] * 256 + s[4] * 256 * 256 + s[5] * 256 * 256 * 256):
        print("Len(s) != s_length")
        continue

      m.seek(1)
      m.write(bytes([2]))
      m.seek(0)
      s = m.read()

      print("type2 = " + str(s[0]))
      print("status2 = " + str(s[1]))
      print("length2 = " + str(s[2]+s[3]*256+s[4]*256*256+s[5]*256*256*256))

      list_length = (len(s) -6) // 8
      python_value = struct.unpack("d" * list_length, s[6:(6 + list_length * 8)])
      python_value = np.asarray(python_value).reshape(list_length)

      t_value = python_value[0:int(list_length / 2)]
      ref_value = python_value[int(list_length / 2):]
      fRange, xfRange = convertToFrequency(t_value, ref_value, 0.1, 2.5)

      if int(s[0]) == 100:#type=100,传入的数据进行物质识别

        workPath = r'D:\训练模型刘虎'
        configFileDir = os.path.join(workPath, "config.txt")
        (dataDir, fRange, _, _, trainSampNames, testFileNames) = readConfigFile(configFileDir)

        width = int((2.5 - 0.1) * 100)
        inputShape = (1, width, 1)
        seriesList = []
        series = np.array(xfRange).reshape(inputShape)
        seriesList.append(series)
        seriesList = np.array(seriesList)

        # Load the trained model
        model = keras.models.load_model(workPath)

        # Classify all the series from the input file
        predicts = model.predict(seriesList)
        numSamps = len(trainSampNames)

        for predict in predicts:
          line = ""
          for i in range(numSamps):
            sampName = trainSampNames[i]
            sampPredict = predict[i]
            line += sampName + " {:.3f}".format(sampPredict)
            if i < numSamps - 1:
              line += ", "

          print(line)

      xfRange = np.array(xfRange)
      fRange = np.array(fRange)
      data = np.append(fRange, xfRange)
      data2bytes = struct.pack('d'*data.shape[0],*data)


      m.seek(2)
      data_length = len(data2bytes)
      m.write(data_length.to_bytes(4,byteorder='little'))
      m.seek(6)
      m.write(data2bytes)
      m.seek(1)
      m.write(bytes([3]))
      m.seek(0)

      s1 = m.read()
      print("type3 = " + str(s1[0]))
      print("status3 = " + str(s1[1]))
      print("length3 = " + str(s1[2]+s1[3]*256+s1[4]*256*256+s1[5]*256*256*256))
      print("data_length = ",data_length)

    #type 1:频域  2:求吸收率，折射率
    #status 1:上位机发送  2:python接受处理中 3:python返回成功 4:上位机接收中 5：上位机接收完成  99：异常
  break
  time.sleep(1)
