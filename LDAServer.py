#coding: utf8

"""
pldaのデータ形式でアクセスすると
topicの多項分布が返ってくる

Example:
$ #server起動
$ python LDAServer.py

以下のようにアクセス
http://localhost:5000/python%201java%202
"""

import os
import subprocess
import urllib
from flask import Flask

app = Flask(__name__)

HOME = os.environ["HOME"]
lda_model = "%s/sron/lda_model2.txt" % HOME
test_data = "%s/sron/plda/testdata/hoge.txt" % HOME
result = "/tmp/inference_result.txt"

cwd = "%s/sron" % HOME
cmdline = """plda/myinfer \
  --alpha 0.5    \
  --beta 0.1                                           \
  --inference_data_file %s \
  --inference_result_file /tmp/inference_result.txt \
  --model_file %s                      \
  --burn_in_iterations 10                              \
  --total_iterations 15
""" % (test_data, lda_model)

p = subprocess.Popen(cmdline,
                     shell=True,
                     cwd=cwd,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     close_fds=True)


@app.route("/<bag_of_words>")
def get_topic(bag_of_words):
    bag_of_words = bag_of_words.encode("utf8")
    p.stdin.write(bag_of_words+"\n")
    line = p.stdout.readline()
    return line.rstrip("\n")


if __name__ == "__main__":
    app.run()