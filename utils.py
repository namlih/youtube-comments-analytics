from googleapiclient.discovery import build
import pandas as pd
import argparse
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

if "GOOGLE-API-KEY" in os.environ:
    api_key = os.environ["GOOGLE-API-KEY"]
else:
    raise Exception("Please provide Google API Key in the .env file with 'GOOGLE-API-KEY' as the key name.")

def get_comments(video_id, save_data=False):
    # creating youtube resource object
    youtube = build('youtube', 'v3', developerKey=api_key)

    # retrieve youtube video results
    comments = []
    publishDates = []
    likeCounts = []
    names = []
    request = youtube.commentThreads().list(part='snippet,replies',videoId=video_id)
    response = request.execute()
    pageNumber = 0
    while True:
        print("Reading comments of the video " + video_id + " page number: " + str(pageNumber))
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            publishedAt = item['snippet']['topLevelComment']['snippet']['publishedAt']
            likeCount = item['snippet']['topLevelComment']['snippet']['likeCount']
            authorDisplayName = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            if len(comment) < 500:
                comments.append(comment)
                publishDates.append(publishedAt)
                names.append(authorDisplayName)
                likeCounts.append(likeCount)
        try:
            request = youtube.commentThreads().list_next(previous_request=request, previous_response=response)
            response = request.execute()
            pageNumber += 1
        except:
            print("End of pages..")
            break
    
    
    if save_data:
        df = pd.DataFrame(data={ 'video_id': [video_id for _ in comments], 
                                 'publishDates': publishDates, 
                                 'authorName': names, 
                                 'comments': comments, 
                                 'likeCount': likeCounts})
        df.to_csv('comments_'+video_id+'.csv',index=False)
    
if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='youtube comments extractor')
    parser.add_argument('--video', '-v', type=str, help="video_id")
    parser.add_argument('--save', '-s', type=str, help="save_data")

    args = parser.parse_args()
    video_id = args.video
    if args.save == 'yes' or args.save == 'y':
        get_comments(video_id=video_id, save_data=True)
    else:
        get_comments(video_id=video_id)
