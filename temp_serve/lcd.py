import LCD1602

class LCD(object):
    def __init__(self):
        LCD1602.init(0x27, 1)

    def write(self, x, y, text):
        LCD1602.write(x, y, text)

    def clear(self):
        LCD1602.clear()
