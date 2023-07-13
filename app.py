import streamlit as st
import pandas as pd
import numpy as np
import random
import requests
import json


# Create the Streamlit app
st.set_page_config(page_title="YouTube Comments Analytics")
st.title("YouTube Comments Analytics")

# The Video
df = pd.read_csv("../data/comments_Beld090NIoo.csv")
video_id = df["video_id"].values[0]
st.video("https://youtu.be/"+video_id)

tab1, tab2 = st.tabs(["Comments with Sentiment Scores","Summary of the Comments"])

# Comments with Sentiment Scores Tab
with tab1:
    st.header("Comments with Sentiment Scores")
    st.caption("currently only showing top 20 comments by like count")
    df.sort_values(by=['likeCount'],ascending=False,inplace=True)

    def showComment(commentText, authorName, likeCount):
        #commentText = "What a dumb video"
        st.text(authorName)
        comment, likes = st.columns([0.9, 0.1])
        comment.write(commentText)
        likes.text("👍 "+str(likeCount))

        response = requests.post("http://127.0.0.1:8000/sentiments/", json={"comment":commentText})
        sentiments = {}
        for r in response.json()["sentimentList"]:
            sentiments[r['label']] = str(round(r['score'] * 100, 2))
        # sentiments = dict(sorted(sentiments.items(), key=lambda item: item[0]))
        st.text("anger 🤬 %"+sentiments['anger'])
        st.text("disgust 🤢 %"+sentiments['disgust'])
        st.text("fear 😨 %"+sentiments['fear'])
        st.text("joy 😀 %"+sentiments['joy'])
        st.text("neutral 😐 %"+sentiments['neutral'])
        st.text("sadness 😭 %"+sentiments['sadness'])
        st.text("surprise 😲 %"+sentiments['surprise'])


    for i, row in df[:20].iterrows():
        showComment(row.comments,row.authorName,row.likeCount)
        st.divider()


# Summary of the Comments Tab
with tab2:
    st.header("Summary of the Comments")
    st.caption("currently only using top 20 comments by like count. The summarization takes up to 20 seconds to process")
    df.sort_values(by=['likeCount'],ascending=False,inplace=True)

    theComment = "This youtube video's name is Percussive Dub, Spiritual Jazz & Psychedelic Grooves with Millie McKee. "
    theComment += "The fans of her, made these comments about her video : "
    #theComment = " "
    for i, row in df[:10].iterrows():
        #theComment += str(i) + " - " + row.comments + ". "
        theComment += row.comments + '. '
    print('comment for summarization:')
    print(theComment)
    response = requests.post("http://127.0.0.1:8000/summaries/", json={"comment":theComment})

    summary = response.json()['summary']
    st.header("The Summary")
    st.divider()
    st.write(summary)