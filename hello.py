from flask import Flask, render_template, request #追加
import tweet_parser


app = Flask(__name__)

@app.route('/', methods=["GET","POST"]) #Methodを明示する必要あり
def hello():
    contents = tweet_parser.get_data()
    # if request.method == 'POST':
    #     name = request.form['name']
    # else:
    #     name = "no name."
    print(contents)
    return render_template('hello.html', contents=contents)