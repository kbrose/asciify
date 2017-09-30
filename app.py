import asciify

import flask
import requests

app = flask.Flask(__name__)

app.config['error_format'] = '''
<div style="font-family: Open Sans, Arial; color:#d55;" align="center">
{}
</div>
'''

@app.route('/')
def main():
    return flask.render_template('form.html')

@app.route('/asciified/', methods=['POST'])
def asciify_api():
    try:
        fr = flask.request
        img = fr.files['file']
        if not img.filename:
            try:
                img = requests.get(fr.form['imagelink'], stream=True).raw
            except requests.exceptions.MissingSchema:
                return app.config['error_format'].format('Problem loading URL.')
        return asciify.asciify(img,
                               float(fr.form['charwidth']),
                               float(fr.form['brightness']),
                               to='html',
                               fontsize=float(fr.form['fontsize'])
                               )
    except Exception:
        return app.config['error_format'].format('Unknown error occured.')
