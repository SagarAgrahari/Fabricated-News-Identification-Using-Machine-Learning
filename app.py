from flask import Flask, escape, request, render_template
import pickle
import speech_recognition as sr
import moviepy.editor as mp
from flask import Flask, request, render_template

vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("finalizer_model.pkl", 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == "POST":
        news = str(request.form['news'])
        print(news)

        predict = model.predict(vector.transform([news]))[0]
        print(predict)

        return render_template("prediction.html", prediction_text="News headline is -> {}".format(predict))


    else:
        return render_template("prediction.html")
    
@app.route('/abc')
def abc():
    return render_template('index2.html')
    
@app.route('/convert', methods=['POST'])
def convert():
    video = request.files['video']
    video.save('input_video.mp4')
    clip = mp.VideoFileClip('input_video.mp4')
    clip.audio.write_audiofile('converted_audio.wav')
    r = sr.Recognizer()
    audio = sr.AudioFile('converted_audio.wav')
    with audio as source:
        audio_file = r.record(source)
    result = r.recognize_google(audio_file)
    with open('recognized_text_file.txt', mode='w') as file:
        file.write(result)
    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.debug = True
    app.run()