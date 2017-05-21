# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

from flask import Flask, render_template, redirect, url_for, request

from google.appengine.api import users
from google.appengine.ext import ndb
from models import Events
from utils import generate_combination

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/generated', methods=['GET', 'POST'])
def generate():
    login_user = users.get_current_user()
    attendee_list_raw = request.form['attendee_list']
    attendee_list = []
    for u in attendee_list_raw.split('\n'):
        if u.strip():
            attendee_list.append(u.strip())
    event = Events(user=login_user, attendee_list=attendee_list,
                   attendee_combination=generate_combination(attendee_list))
    event_key = event.put()
    return redirect(url_for('generated', data_store_key=event_key.urlsafe()))


@app.route('/generated/<data_store_key>', methods=['GET', 'POST'])
def generated(data_store_key):
    event_key = ndb.Key(urlsafe=data_store_key)
    event = event_key.get()
    login_user = users.get_current_user()
    if (event.user != login_user) and event.public is False:
        return 'invalid request', 401
    return render_template('generated.html', event=event)


@app.route('/result/<data_store_key>', methods=['GET'])
def result(data_store_key):
    event_key = ndb.Key(urlsafe=data_store_key)
    event = event_key.get()
    login_user = users.get_current_user()
    if (event.user != login_user) and event.public is False:
        return 'invalid request', 401
    return render_template('result.html', event=event)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# [END app]
