from flask import *
from wtforms import *
import requests
app = Flask(__name__)


urlsInDB = {}

class HomePage(Form):
    enter_url = StringField('Enter Actual URL')


def Request(url):
    base_url = 'http://tinyurl.com/api-create.php?url='
    #base_url2 = 'https://tinyurl.com/app/api/create'
    url = base_url + url
    #myobj = {
#  "data": [
 #   {
  #    "url": url,
   #   "active": True,
   #   "no_affiliate": False
  #  }
 # ]
#}
    r = requests.get(url)
    #r2 = requests.post(base_url2, data=myobj, headers={"content-type": "application/json;charset=UTF-8"})
    return r.text


@app.route('/', methods=['GET','POST'])
def index():
    form = HomePage(request.form)
    if request.method == 'POST':
        url = form.enter_url.data
        if url in urlsInDB:
            tiny_url = urlsInDB[url]
        else:
            tiny_url = Request(url)
            urlsInDB[url] = tiny_url

        if (tiny_url == 'Error'):
            flash(Markup('Bad URL. Try Again!'), 'success')
        else:
            flash(Markup('<a href="%s" class="alert-link">%s</a>' %(tiny_url, tiny_url)), 'success')
        redirect(url_for('index'))

    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
