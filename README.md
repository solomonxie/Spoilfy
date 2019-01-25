# Spoilfy
This program aims to build a lifetime-persistant personal favorites/collections/history management system in music,
as a supplementary solution to the "isolated" media platforms like Spotify and iTunes.
The core idea to achieve this is to build a unified Mapper database which maps music information across multiple media platforms with the support of APIs of Spotify and MusicBrainz.
The goal is to build a music focused Personal Cloud that differs to Owncloud/Plex/SeaFile.

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

## Mapping
![image](https://user-images.githubusercontent.com/14041622/50376934-8aa89d80-064f-11e9-823d-f9a633ff5352.png)



## Table Groups
![image](https://user-images.githubusercontent.com/14041622/50376930-7fee0880-064f-11e9-8c7d-35b88a457bb6.png)



## URI
![image](https://user-images.githubusercontent.com/14041622/50376940-a3b14e80-064f-11e9-89b9-5e49797b6c79.png)


## Workflow
![image](https://user-images.githubusercontent.com/14041622/50376937-92684200-064f-11e9-9d2b-0a35ef093870.png)

