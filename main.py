import datetime
import os
import time
from queue import Queue
import sched
from threading import Thread

from flask import Flask, request, send_from_directory

app = Flask(__name__)
MAX_REQUESTS = 10  # maximum number of requests allowed per second
request_queue = Queue(maxsize=MAX_REQUESTS)
scheduler = sched.scheduler(time.time, time.sleep)


def process_queue():
    while True:
        time.sleep(1)  # wait for one second
        try:
            request_queue.get(block=False)
        except:
            pass


def delete_files():
    # 获取一小时前的时间戳
    one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    timestamp = one_hour_ago.timestamp()
    # 遍历image目录下的所有文件
    for root, dirs, files in os.walk('image'):
        for file in files:
            # 获取文件创建时间
            file_path = os.path.join(root, file)
            create_time = os.path.getctime(file_path)
            # 如果文件创建时间早于一小时前，则删除文件
            if create_time < timestamp:
                os.remove(file_path)


scheduler.enter(3600, 1, delete_files, ())


@app.route('/img', methods=['POST'])
def image():
    file = request.files.get('image')
    if file:
        # add the current timestamp to the queue
        request_queue.put(time.time())
        # 1524ca7a-a95c-11ed-9acc-0028f80fc0b6.jpg
        # 保存到本地
        file.save(rf"/home/host/image/{file.filename}")
        # 返回图片的 URL
        return f"https://yoururl/image/{file.filename}"
    else:
        return "No image provided."


@app.route("/image/<path:filename>", methods=['GET'])
def serve_image(filename):
    _file_path = "/home/host/image"
    return send_from_directory(_file_path, filename)


if __name__ == '__main__':
    scheduler.run()
    t = Thread(target=process_queue)
    t.daemon = True
    t.start()
    app.run()
