
from flask import Flask
from app import views
import sys
sys.path.append('D:\fp\image\app')

app = Flask(__name__)


app.add_url_rule('/base','base',views.base)
app.add_url_rule('/','index',views.index)
app.add_url_rule('/gender','gender',views.gender,methods=['GET','POST'])
app.add_url_rule('/help','help',views.help)
app.add_url_rule('/about','about',views.about)


if __name__ == "__main__":
    app.run(port=5000,debug=True)