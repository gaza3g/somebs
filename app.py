from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask import jsonify
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job
from worker import conn
import operator
import os
import requests
import re
import nltk
from converter import Converter

import sys
import subprocess

#################
# configuration #
#################

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

q = Queue(connection=conn)

from models import *

##########
# helper #
##########


def count_and_save_words(url):

    errors = []

    c = Converter()

    vidcon_root = '/Volumes/EdulearnNetUpload/asknlearn/vidcon/'

    input_dir = 'input/'
    output_dir = 'output/'
    exc = ""

    # input_file = 'test1.ogg'
    # output_file = 'out1.mkv'

    # input_path = os.path.join(vidcon_root + input_dir, input_file)
    # output_path = os.path.join(vidcon_root + output_dir, output_file)

    input_path = "/Volumes/EdulearnNetUpload/asknlearn/vidcon/input/test1.ogg"
    output_path = "/Volumes/EdulearnNetUpload/asknlearn/vidcon/output/out1.mp4"

    # ffmpeg -i test1.ogg -acodec copy -vcodec libx264 -s 854x480 out2.mp4
    # whatever = subprocess.call(['ffmpeg', '-i', input_file, '-acodec',
    #                  'copy', '-vcodec', 'libx264', '-s', '854x480', output_file])


#ffmpeg -i "/Volumes/EdulearnNetUpload/asknlearn/vidcon/input/test1.ogg" -acodec copy -vcodec libx264 -s 854x480 "/Volumes/EdulearnNetUpload/asknlearn/vidcon/output/out1.mp4"

    cmd = "ffmpeg -i \"{infile}\" -acodec copy -vcodec libx264 -s 854x480 \"{outfile}\"".format(
        infile=input_path, outfile=output_path)

    #['MP4Box', '-cat', 'test_0.mp4', '-cat', 'test_1.mp4', '-cat', 'test_2.mp4', '-new', 'test_012d.mp4']
    ffmpeg_exec = ['ffmpeg', '-i', "{}".format(input_path), "-acodec", "copy", "-vcodec", "libx264", "-s", "854x480", "{}".format(output_path)]

    # return_code = subprocess.Popen(cmd, bufsize=2048,
    #                                stderr=subprocess.STDOUT,
    #                                stdout=subprocess.PIPE).wait()



    try:
	    # return_code = subprocess.Popen(cmd, bufsize=2048, shell=True,
	    #                                stderr=subprocess.STDOUT,
	    #                                stdout=subprocess.PIPE).wait()
	    return_code = subprocess.Popen(ffmpeg_exec, bufsize=2048,
	                                   stderr=subprocess.STDOUT,
	                                   stdout=subprocess.PIPE).wait()
        # output = subprocess.check_output(
        # cmd.encode(sys.getfilesystemencoding()), stderr=subprocess.STDOUT)
        # subprocess.call(["pwd"], shell=True)
        # subprocess.call(
        #     ["cd /Volumes/EdulearnNetUpload/asknlearn/vidcon/input/"], shell=True)
		# return_code = subprocess.Popen(cmd, shell=True, bufsize=2048,stderr=subprocess.STDOUT,stdout=subprocess.PIPE).wait()
# if output:
#     return (1, output)
# else:
#     return (0, "")
    except Exception as e:
        exc = "{}".format(e)

    # save the results
    try:
        result = Result(
            url=cmd,
            result_all=return_code,
            result_no_stop_words=exc)
        db.session.add(result)
        db.session.commit()
        return result.id
    except:
        errors.append("Unable to add item to database.")
        return {"error": errors}

    # conv = c.convert(input_path, output_path,
    #                  {
    #                      'format': 'mkv',
    #                      'audio': {
    #                          'codec': 'mp3',
    #                          'samplerate': 44100,
    #                          'channels': 2
    #                      },
    #                      'video': {
    #                          'codec': 'h264',
    #                          'width': 320,
    #                          'height': 240,
    #                          'fps': 24
    #                      }})

    # for timecode in conv:
    # 	print("Converting...")

    # try:
    #     r = requests.get(url)
    # except:
    #     errors.append(
    #         "Unable to get URL. Please make sure it's valid and try again."
    #     )
    #     return {"error": errors}

    # text processing
    # raw = BeautifulSoup(r.text).get_text()
    # nltk.data.path.append('./nltk_data/')  # set the path
    # tokens = nltk.word_tokenize(raw)
    # text = nltk.Text(tokens)

    # remove punctuation, count raw words
    # nonPunct = re.compile('.*[A-Za-z].*')
    # raw_words = [w for w in text if nonPunct.match(w)]
    # raw_word_count = Counter(raw_words)

    # stop words
    # no_stop_words = [w for w in raw_words if w.lower() not in stops]
    # no_stop_words_count = Counter(no_stop_words)

    # save the results
    # try:
    #     result = Result(
    #         url=url,
    #         result_all=raw_word_count,
    #         result_no_stop_words=no_stop_words_count
    #     )
    #     db.session.add(result)
    #     db.session.commit()
    #     return result.id
    # except:
    #     errors.append("Unable to add item to database.")
    #     return {"error": errors}

##########
# routes #
##########


@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        url = request.form['url']
        if 'http://' not in url[:7]:
            url = 'http://' + url
        job = q.enqueue_call(
            func=count_and_save_words, args=(url,), result_ttl=5000
        )
        print(job.get_id())

    return render_template('index.html', results=results)


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return job.get_status(), 202


if __name__ == '__main__':
    app.run()
