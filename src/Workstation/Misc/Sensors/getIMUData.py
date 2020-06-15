import socket
import sys
import time

TCP_IP = '0.0.0.0'
TCP_PORT = 5007 # Port number on which to send data
BUFFER_SIZE = 200 # Normally 1024, but I want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)



def main():

    while True:
        dataString = conn.recv(BUFFER_SIZE)

        dataList = dataString.split(',')

        accelX, accelY, accelZ = dataList[0], dataList[1], dataList[2]
        gyroX, gyroY, gyroZ = dataList[3], dataList[4], dataList[5]
        magX, magY, magZ = dataList[6], dataList[7], dataList[8]
        temp = dataList[9]

        accel = {'x': accelX,
                 'y': accelY,
                 'z': accelZ
                }

        gyro = {'x': gyroX,
                 'y': gyroY,
                 'z': gyroZ
               }

        mag = {'x': magX,
                 'y': magY,
                 'z': magZ
              }


        print("accel: ", accel)
        print("gyro: ", gyro)
        print("mag: ", mag)
        print("temp: ", temp)

        time.sleep(0.1)

    conn.close()

if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)