# -*- coding: utf-8 -*-
"""「「02 CNN.ipynb」」作業

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qs_nwEhpP22vl53_pyYpFbIUFWpKVdjV
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
#大小3x3所以是2D
from tensorflow.keras.layers import Dense, Flatten
#讓電腦自己拉平
from tensorflow.keras.optimizers import SGD
#優化方法

"""### 1. 讀入 MNSIT 數據集"""

from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
#training跟test資料要分開讀

"""### 2. 資料整理

### Channel

CNN 要注意一張圖有多少個 channel, 開始我們因為只有灰階, 所以只有一個 channel。因此我們要轉一下我們的資料格式:

    (28,28) --> (28, 28, 1)
"""

x_train = x_train.reshape(60000, 28, 28, 1) / 255
#1的意思：灰階1個channel，彩色圖片為3，28x28為圖片大小

x_test = x_test.reshape(10000, 28, 28, 1) / 255

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
#10的意思：種類數量

"""### 3. step 1: 打造函數學習機 (CNN)"""

model = Sequential()

model.add(Conv2D(10, (3,3), padding='same',
                input_shape=(28,28,1),
                activation='relu'))
#10決定要幾個filter，3x3為fliter大小，1為灰階，28x28為計分板

model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(20, (3,3), padding='same',
                activation='relu'))
#第一次用10個第二次用20個

model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(40, (3,3), padding='same',
                activation='relu'))

model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(20, activation='relu'))
#決定該層使用幾個神經元

model.add(Dense(10, activation='softmax'))
#輸出十個神經元

"""#### 看一下我們的神經網路"""

model.summary()
#第一行8為計分板個數，28x28為大小，以此類推，到288拉平
#9個權重+1偏執=10，總共8個計分板＝80個要調

"""#### 組裝"""

model.compile(loss='mse', optimizer=SGD(lr=0.087),
             metrics=['accuracy'])

"""### 4. step 2: fit"""

model.fit(x_train, y_train, batch_size=128, epochs=12)
#訓練12次

"""### Step 3. 預測"""

result = model.predict_classes(x_test)

"""### 看看測試資料表現如何"""

loss, acc = model.evaluate(x_test, y_test)

print(f'測試資料的正確率為 {acc*100:.2f}%')

def my_predict(n):
    print('我可愛的 CNN 預測是', result[n])
    X = x_test[n].reshape(28,28)
    plt.imshow(X, cmap='Greys')

from ipywidgets import interact_manual

interact_manual(my_predict, n=(0, 9999));

"""### 把我們的 model 存起來"""

model.save('myCNNmodel.h5')