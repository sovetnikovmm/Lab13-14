from flask import render_template, redirect

from app import app


@app.route('/')
@app.route('/index')
def index():
    return redirect('goods')
