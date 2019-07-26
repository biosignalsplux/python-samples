import threading
import platform
import sys

osDic = {"Darwin": "MacOS",
         "Linux": "Linux64",
         "Windows": ("Win32", "Win64")}
if platform.system() != "Windows":
    sys.path.append("PLUX-API-Python3/{}/plux.so".format(osDic[platform.system()]))
else:
    if platform.architecture()[0] == '64bit':
        sys.path.append("PLUX-API-Python3/Win64")
    else:
        sys.path.append("PLUX-API-Python3/Win32")
import plux


class NewDevice(plux.MemoryDev):

    def __init__(self, address):
        plux.MemoryDev.__init__(address)
        self.time = 0
        self.frequency = 0

    def onRawFrame(self, nSeq, data):  # onRawFrame takes three arguments
        if nSeq % 2000 == 0:
            print(nSeq)
        if nSeq/self.frequency > self.time:
            return True
        return False

# example routines


def exampleAcquisition(address, time, freq, code):  # time acquisition for each frequency
    """
    Example acquisition.

    Supported channel number codes:
    {1 channel - 0x01, 2 channels - 0x03, 3 channels - 0x07
    4 channels - 0x0F, 5 channels - 0x1F, 6 channels - 0x3F
    7 channels - 0x7F, 8 channels - 0xFF}

    Maximum acquisition frequencies for number of channels:
    1 channel - 8000, 2 channels - 5000, 3 channels - 4000
    4 channels - 3000, 5 channels - 3000, 6 channels - 2000
    7 channels - 2000, 8 channels - 2000
    """
    device = NewDevice(address)
    device.time = time  # interval of acquisition
    device.frequency = freq
    device.start(device.frequency, code, 16)
    device.loop()  # calls device.onRawFrame until it returns True
    device.stop()
    device.close()


def createThreads(address_list, time, freq_list, code_list):

    thread1 = threading.Thread(target=exampleAcquisition, args=(address_list[0], time, freq_list[0], code_list[0]))
    thread2 = threading.Thread(target=exampleAcquisition, args=(address_list[1], time, freq_list[1], code_list[1]))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    if platform.system() == 'Darwin':
        plux.MacOS.stopMainLoop()


def createMainThread(address_list, time, freq_list, code_list):

    main_thread = threading.Thread(target=createThreads, args=(address_list, time, freq_list, code_list))
    main_thread.start()
    if platform.system() == 'Darwin':
        plux.MacOS.runMainLoop()
    main_thread.join()


createMainThread(["BTH00:07:80:4D:2E:76", "BTH00:07:80:3B:46:58"], 20, [1000, 2000], [0xFF, 0x01])
