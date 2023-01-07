from flask import Flask,jsonify,request
import symbl
from pytube import YouTube
import openai


app = Flask(__name__)

@app.route("/")
def hello_world():
    return




openai.api_key = ("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")



def youtube_video_download(data):
    path = r"C:\Users\MAHESH\Desktop\YouTube-Video-Simplify-main\new\public\videos\\"
    url = data
    youtubeObject = YouTube(url)
    youtubeObject = youtubeObject.streams.get_lowest_resolution()
    try:
        youtubeObject.download(filename = "my.mp4", output_path = path)
    except:
        print("An error has occurred")
    print("Download is completed successfully")




@app.route('/video', methods=["POST","GET"])
def output():
    data = request.json
    print(data)
    youtube_video_download(data)
    print(data)
    conversation_object = symbl.Video.process_file(file_path=r'C:\Users\MAHESH\Desktop\YouTube-Video-Simplify-main\new\public\videos\my.mp4')
    print(conversation_object.get_messages())
    print(conversation_object.get_topics())
    textoutput = conversation_object.get_messages()
    msg = conversation_object.get_topics()
    
    
    out = " "
    for i in range(len(msg.topics)):
        out = msg.topics[i].text+',  ' + out 
        print(out)


    message = " "
    for i in range(len(textoutput.messages)):
        message = message + ' ' +textoutput.messages[i].text+' ' 
        print(message)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= message,
        temperature=0.7,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    response = response.choices[0].text


    return jsonify({'data':message},{'topics':out},{'summary':response})