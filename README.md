# Spoilfy
This program aims to build a lifetime-persistant personal favorites/collections/history management system in music,
as a supplementary solution to the "isolated" media platforms like Spotify and iTunes.
The core idea to achieve this is to build a unified Mapper database which maps music information across multiple media platforms with the support of APIs of Spotify and MusicBrainz.
The goal is to build a music focused Personal Cloud that differs to Owncloud/Plex/SeaFile.



## TODO

Trello Scrum Board: https://trello.com/b/FfMzYWKy/spoilfy-scrum-board

TODO:
- [x] Design Database & ORM
- [ ] Quick implementation: ORM Data Insertion
    - [x] Spotify
        - [x] Accounts
        - [x] Tracks
        - [x] Albums
        - [x] Artists
        - [x] Playlists
    - [x] MusicBrainz
        - [x] Recordings
        - [x] Releases
        - [x] Artists
    - [ ] Filesystem
        - [ ] MP3 file
        - [ ] Folder structure
- [x] Quick implementation: Data Query
    - [x] Accounts
    - [x] Tracks
    - [x] Albums
    - [x] Artists
    - [x] Playlists
- [x] Quick implementation: Web API
    - [x] Postman Test
    - [x] Spotify
        - [x] Authentication
        - [x] Retrieving
        - [x] Paging
    - [x] MusicBrainz
        - [x] Authentication
        - [x] Retrieving
- [x] Quick implementation: Flask
- [ ] Quick implementation: Tagging (Auto-tagger)
    - [ ] Spotify -> MusicBrainz
        - [x] Track
        - [ ] Album
        - [ ] Artist
    - [ ] Local files -> MusicBrainz
- [ ] Design Code Architecture
- [ ] Modularization
- [ ] Implement Models & Unit tests
- [ ] Create Frontend Pages
- [ ] Integrate Frontend & Backend
- [ ] Integration Test
- [ ] Deploy on Server
- [ ] Documentation
- [ ] Publish beta




## ERP Design with URI [UPDATE]

![image](https://user-images.githubusercontent.com/14041622/50371963-0975ea00-0600-11e9-92ce-8cc0daae8c34.png)


Updates:
- Replace ID with URI in the format of: `<Group>:<Type>:<ID>`
- Abandon most Foreign Keys to add flexibilities.
- Treat everything as a RESOURCE, and introduce a REFERENCE to connect.

The core idea is simple:
One real existence, can have multiple identities, or located in multiple providers.
In this case, the `Real Existence` would be referred to `Track / Album / Artist / Playlist`,
and they might exist with different identities: Spotify's resource, MusicBrainz's info, Local file...

### Mapping
![image](https://user-images.githubusercontent.com/14041622/50376934-8aa89d80-064f-11e9-823d-f9a633ff5352.png)



### Table Groups
![image](https://user-images.githubusercontent.com/14041622/50376930-7fee0880-064f-11e9-8c7d-35b88a457bb6.png)



### URI
![image](https://user-images.githubusercontent.com/14041622/50376940-a3b14e80-064f-11e9-89b9-5e49797b6c79.png)


### Workflow
![image](https://user-images.githubusercontent.com/14041622/50376937-92684200-064f-11e9-9d2b-0a35ef093870.png)







## PROJECT DESIGN

![snip20181207162](https://user-images.githubusercontent.com/14041622/49634078-a2b8d400-fa36-11e8-9394-1ce2b438eb2a.png)


### REQUIREMENTS ANALYSIS

- Music Player
    - Display music library [playlists, artists, albums, songs, recommendations]
    - Online stream music playing
- `? Personal Data Management`
    - Backup [playlists, liked songs, albums, artists]
        - Save to database [sqlite]
        - Export to local files  [m3u, csv]
        - Import from local data [m3u, csv, sqlite]
    - Apply changes to Spotify
- Media File Organizing
    - Auto Tagging: take Spotify's as dominant, others as supplementaries.
        - By folder structure
        - By filename
        - By existing tags
        - By fingerprint
    - File renaming
        - Rename file
        - Re-structure folder
- Media File Sources
    - Import From Local Files
        - Only import recognizable files
        - Group un-recognized files into one folder to be further processed
    - Refer to Cloud drives: [Webdav, Google drive, [AWS-S3](https://aws.amazon.com/s3/)]
    - Refer to Spotify 30s preview file: ["Spotify API"](https://developer.spotify.com/documentation/web-api/)
    - Refer to Youtube [albums, songs]: ["Track Connectors"](http://developers.music-story.com/developers/track)
    - Refer to Search engines: "Piratebay"


### PROTOTYPE & Frontend

No need for Frontend design, it's supposed to be a completely copy from Spotify.



### Tech Stacks

- Hosting: AWS Lightsail Ubuntu 16.04
- Language: Python + JS
- HTTP Server: Nginx + WSGI
- Application Framework: Django
- Databases: Postgresql + Redis + Sqlite
- DevOps: Bash scripts, Git, Travis CI, Docker, Ansible
- Utilities: Github Issues, Axure prototype
- Editors: Vim, Sublime Text, Visual Studio Code
- Business tools: Google Ads

https://stackshare.io/solomonxie/spoilfy


### Modulization (by Class)

Root:
- [ ] Providers
    - [ ] Spotify
        - [x] ORM
        - [ ] API
        - [ ] Mange
    - [ ] MusicBrainz
        - [ ] ORM
        - [ ] API
        - [ ] Manage
- [ ] Template
    - [ ] Tracks
    - [ ] Albums
    - [ ] Artists
    - [ ] Playlists
- [ ] Route.py


### Modulization (by Page)

- [ ] Music Library (Spotify)
    - [ ] Track: `[Display, Play, Add, Delete, Export, Sync, Import, Export]`
    - [ ] Albums: `[Display, Play, Add, Delete, Export, Sync, Export]`
    - [ ] Artists: `[Display, Play, Add, Delete, Export, Sync, Export]`
    - [ ] Playlists: `[Display, Play, Add, Delete, Update, Import, Export, Sync]`
    - [ ] Recent Played: `[Display, Play]`
    - [ ] Home: `[Display, Play]`
    - [ ] Browse: `[Display, Play]`
    - [ ] Recommends: `[Display, Play]`
- [ ] Dashboard (Management)
    - [ ] Sync Library
        - [ ] From Spotify: `[API Fetching]`
        - [ ] From Xiami
        - [ ] From iTunes
    - [ ] Local File Importation: `[Tagging, Relating]`
    - [ ] Cloud Drive Importation
        - [ ] Webdav: `[Tagging, Relating]`
        - [ ] Google Drive: `[Tagging, Relating]`
        - [ ] Dropbox: `[Tagging, Relating]`


### Interfaces Definitions

Instead of directly extract data from database to Jinja2 Templates,
it's more flexible to make data as `RESTful API`.

When the frontend requires some data, like an album,
the program will first check whether the data already exists in the database on server.
If not, it'll then request Spotify API, MusicBrainz API and other APIs.
What it does next is doing both saving retrieved new data and also presenting it to the user.

### RESTful API Design

This API only response data from CURRENT User Library.
Data will be returned in JSON format.

BASE URL: `http://music.solomonxie.top/spoilfy/api/v1`

Entry points:
- `/tracks`: Return a list of user's Liked Tracks.
- `/artists`: Return a list of user's Followed Artists.
- `/albums`: Return a list of user's Saved Albums.
- `/playlist`: Return a list of user's Saved Playlists.

### Backend work flow

Init/Update User Library Flow:
- `@1 Fetch User full data from Spotify API` ->
- `@2 Process retried data` ->
- `@3 Save to Local Spotify Library` ->
- `@4 Cross searching MusicBrainz Library`
- `@5 Save to User Library`.



User Library API:
- Client sends request ->
- `@1 API Entry point` ->
- `@2 Get LIST from User's library` ->
- `@3 Check information from Local Public Library for each item in the LIST` ->
- `@4 If not exists, RETRIEVE each item's data from Provider's Web API` ->
- `@5 Process retried data` ->
- `@6 Save to Local Public Library` ->
- `@7 Return to client`.



User flow:
- Import library ->
- Music Play or Manage

Tagging flow:
- Import files ->
- Tagging ->
- Relate to MusicBrainz ->
- Relate to Spotify
