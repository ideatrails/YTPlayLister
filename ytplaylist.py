import argparse
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

import json
import logging
import os
import re

# google-auth 
# https://google-auth.readthedocs.io/en/master/
#   oauth2client was recently deprecated in favor of this library.
#   For more details on the deprecation, see oauth2client deprecation.
# https://google-auth.readthedocs.io/en/master/user-guide.html
#   pip install --upgrade google-auth

# import google_auth_oauthlib.flow
# from google_auth_oauthlib.flow import Flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account



def main():
    load_dotenv()
    version = 0.8
    parser = config_argparse(version)
    args = parser.parse_args()

    # Logfile for application
    log_file = './logs/ytplaylist.log'

    log_level = args.logLevel
    if log_level == "critical" : log_level = logging.CRITICAL
    elif log_level == "debug" : log_level = logging.DEBUG
    elif log_level == "info" : log_level = logging.INFO
    elif log_level == "warning" : log_level = logging.WARNING
    elif log_level == "error" : log_level = logging.ERROR
    elif log_level == "notset" : log_level = logging.NOTSET
    else: log_level = logging.NOTSET

    logging.basicConfig(filename=log_file,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        level=log_level)

    logging.info("NEW RUN =======================================================")
    logging.info(vars(args))

    corpus = args.corpus
    playlist = args.playlist

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # # A. Get credentials and create an API client
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    client_secrets_file = "./yt-trans-trail-6362902f66f4.json"
    credentials = service_account.Credentials.from_service_account_file(client_secrets_file)
    scoped_credentials = credentials.with_scopes(scopes)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=scoped_credentials)

    # OR B. use the API_Key
    # token = os.environ.get("api-token")
    # api_key=token
    # youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    nextPageToken=""
    vid_input_list = []

    while True:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            pageToken=nextPageToken,
            maxResults=25,
            playlistId=playlist
        )
        response = request.execute()

        items = response['items']
        try:
            nextPageToken = response['nextPageToken']
        except KeyError:
            nextPageToken = None
        except TypeError:
            nextPageToken = None

        # for item in tqdm(enumerate(items)):
        for item in items:
            title = item['snippet']['title']
            title = re.sub(',', '\,', title)
            title = f'"{title}"'

            pub_date_converted = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%S%fZ").strftime("%Y%m%d")
            if item['snippet']['resourceId']['kind'] == 'youtube#video':
                video = item['snippet']['resourceId']['videoId']
                ref = playlist # default for now

                description = item['snippet']['description']
                description = re.sub('"', '\"', description)
                description = re.sub("[\r\n]+", " ", description)
                description = description.replace(u'\xa0', u' ')

                description = f'"{description}"'
                thumb = ""
                try:
                    thumb = item['snippet']['thumbnails']['default']['url'] 
                except:
                    thumb = ""

                vid_link = f"https://youtu.be/{video}"
                vid_input_list.append((pub_date_converted, title, vid_link, ref, thumb, description))

        if not nextPageToken:
            break

    df_jobs_new = pd.DataFrame(vid_input_list, columns=['pub_date', 'title', 'video', 'ref', 'thumb', 'desc'])
    df_jobs_new.to_csv(f"../generated_playlists/playlist_v3_{corpus}_{playlist}.csv", index=None)
    df_jobs_new.to_json(f"../generated_playlists/playlist_v3_{corpus}_{playlist}.json", orient="records", indent=2)
    outputJson = df_jobs_new.to_json(orient="records")
    parsed = json.loads(outputJson)
    print(json.dumps(parsed))

def config_argparse(version):
    
    parser = argparse.ArgumentParser(   prog='python ./ytplaylist.py',                                        
                                        description='Build csv import list for getTrans.',
                                        epilog='Enjoy the program! :)')
    
    parser.version = f'{version}'

    parser.add_argument(    '-c', '--corpus', 
                            type=str,
                            action='store',
                            metavar='corpus',
                            required=True,
                            help='prefix for storing different corpus')

    parser.add_argument(   '--playlist', 
                            type=str,
                            action='store',
                            metavar='playlist',
                            required=True,
                            help='youtube playlist to build an input file')

    parser.add_argument(    '-d', '--debug',
                            action='store_true',
                            help='set debug mode for testing and diagnostics')

    parser.add_argument(    '-p', '--progress',
                            action='store_true',
                            help='show progress of search')

    parser.add_argument(    '-v', action='version')

    parser.add_argument(    '-l', '--logLevel', 
                            type=str,
                            action='store',
                            choices=['critical', 'debug', 'info', 'warning', 'error', 'notset'],
                            metavar='logLevel',
                            help='the logging level')

    return parser


if __name__ == "__main__":
    main()
