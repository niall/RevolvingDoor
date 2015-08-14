from . import jobs
from flask import render_template
from .forms import NewJobForm

@jobs.route('/')
def index():

    return render_template('jobs/index.html')

@jobs.route('/new-job')
def new_job():
    form = NewJobForm()
    return render_template('jobs/new-job.html')
