## Quick start

[Python Quickstart | Google Drive API | Google Developers](https://developers.google.com/drive/api/v3/quickstart/python?authuser=1)

- 위에 나와있는 거 그대로 해서 `credential.json` 이용해서 `token.pickle`을 만들면 그 다음부터는 `credential.json`이 필요하지 않음. 하지만 `token.pickle` 을 재생성하거나 지워졌을 경우에는 필요하니 잃어버리면 안 되기는 함.

## Authentication

[Authenticate your users | Google Drive API | Google Developers](https://developers.google.com/drive/api/v3/about-auth)

- token.pickle이 없을 때 브라우저를 통해 인증을 하는데 이때 `scope` 에 따라 접근할 수 있는 범위가 달라짐.
- shared_drive에 있는 file에 접근하기 위해서는 `scope`로 [`https://www.googleapis.com/auth/drive`](https://www.googleapis.com/auth/drive) 가 필요함.

## base client

- drive api를 이용하기 위해서 파이썬 코드 내에서 필요한 client
```
    from googleapiclient.discovery import build
    
    # token.pickle이 없을 경우 위의 Quick start를 참고해서 token.pickle을 만들 것
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    
    service = build('drive', 'v3', credentials=creds)
```
## driveId

- shared drives를 이용하기 위해서는 해당 드라이브의 Id가 뭔지 알아야 됨.
```
    results = service.drives().list(
            fields='nextPageToken, drives(id, name)',
            pageToken=None).execute()
    items = results.get('drives', [])
    print(items)
```
## list files

- folder 내에 파일이 있을 경우 query로 name을 쓸 경우 결과로 여러 개가 나올 수 있음. 이는 trash에 있는 파일도 포함돼서임
```
    results = service.files().list(
    			  q="name='{file name}' and trashed=false"
            corpora='drive', # default는 user인데 user이면 동작 안 함
            driveId='{driveId}',
            pageSize=10, 
            fields="nextPageToken, files(id, name)", 
            supportsAllDrives=True,
            includeItemsFromAllDrives=True).execute()
     items = results.get('files', [])
```
## download files

- 무슨 파일을 다운로드 받을거냐에 따라 `files`에서 사용하는 함수가 달라짐

[Download files | Google Drive API | Google Developers](https://developers.google.com/drive/api/v3/manage-downloads)
```
    import io
    from googleapiclient.http import MediaIoBaseDownload
    
    request = service.files().get_media(fileId='{fileId}')
    # google api guide에서는 BytesIO를 쓰고 있는데 이걸 쓰면 다운로드가 제대로 안 됨
    fh = io.FileIO('{target path}', 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
```
## Create and populate folders

[Create and populate folders | Google Drive API | Google Developers](https://developers.google.com/drive/api/v3/folder)

[How do I upload to a shared drive in Python with Google Drive API v3?](https://stackoverflow.com/questions/57582032/how-do-i-upload-to-a-shared-drive-in-python-with-google-drive-api-v3)

## mime types

- You can use MIME types to filter query results or have your app listed in the Chrome Web Store list of apps that can open specific file types

[Supported MIME Types | Google Drive API | Google Developers](https://developers.google.com/drive/api/v3/mime-types)

[Google drive API download files - python - no files downloaded](https://stackoverflow.com/questions/36173356/google-drive-api-download-files-python-no-files-downloaded)