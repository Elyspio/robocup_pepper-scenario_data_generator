# !pip install
from __future__ import print_function

import io
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# If modifying these scopes, delete the file token.pickle.
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']


class ExcelGenerator:
    def __init__(self, root_folder_id, excel_path="excels"):
        if not os.path.exists(excel_path):
            os.mkdir(excel_path)

        self.service = ExcelGenerator.init_drive_connection()
        self.import_drive_folder(root_folder_id, excel_path)
        pass

    def import_drive_folder(self, folder_id, dest_path):

        folder_id = "'{0}' in parents".format(folder_id)
        req = self.service.files().list(pageSize=50, q=folder_id).execute()

        for f in req.get('files', []):
            file_path = os.path.join(os.path.abspath(dest_path), f['name'])
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                if not os.path.exists(file_path):
                    os.mkdir(file_path)
                ExcelGenerator.import_drive_folder(self, f['id'], os.path.join(dest_path, f['name']))
            else:
                request = self.service.files().export_media(fileId=f['id'],
                                                            mimeType='application/vnd.openxmlformats-officedocument'
                                                                     '.spreadsheetml.sheet')
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download {0:30} {1:3d}%.".format(f['name'], int(status.progress() * 100)))
                with open(os.path.join(file_path + '.xlsx'), "wb") as excel_file:
                    excel_file.write(fh.getvalue())
                fh.close()

    @staticmethod
    def init_drive_connection(path_to_credential="./credential.json"):
        """Shows basic usage of the Drive v3 API.
           Prints the names and ids of the first 10 files the user has access to.
           """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    path_to_credential, SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('drive', 'v3', credentials=creds)
