CREATE TABLE `u_Users` (
  `uid` <type>,
  `name` <type>,
  PRIMARY KEY (`uid`)
);

CREATE TABLE `u_Hosts` (
  `id` <type>,
  `host_id` <type>,
  `uid` <type>,
  `host_user_id` <type>,
  `auth` <type>,
  `name` <type>,
  `nickname` <type>,
  `email` <type>,
  `info` <type>,
  PRIMARY KEY (`id`),
  KEY `FK` (`host_id`, `uid`)
);

CREATE TABLE `hosts` (
  `host_id` <type>,
  `name` <type>,
  `URI` <type>,
  `auth_methods` <type>,
  `info` <type>,
  PRIMARY KEY (`host_id`)
);

CREATE TABLE `u_Artists` (
  `id` <type>,
  `atid` <type>,
  `uid` <type>,
  `name` <type>,
  `liked_at` <type>,
  `memo` <type>,
  PRIMARY KEY (`id`),
  KEY `FK` (`atid`, `uid`)
);

CREATE TABLE `mp_Artists` (
  `atid` <type>,
  `atid_spt` <type>,
  `atid_mbz` <type>,
  PRIMARY KEY (`atid`),
  KEY `FK` (`atid_spt`, `atid_mbz`)
);

CREATE TABLE `spotify_Artists` (
  `atid_spt` <type>,
  `name` <type>,
  `......` <type>,
  PRIMARY KEY (`atid_spt`)
);

CREATE TABLE `musicbrainz_Artists` (
  `atid_mbz` <type>,
  `name` <type>,
  `......` <type>,
  PRIMARY KEY (`atid_mbz`)
);

CREATE TABLE `u_Albums` (
  `id` <type>,
  `abid` <type>,
  `uid` <type>,
  `title` <type>,
  `liked_at` <type>,
  `memo` <type>,
  PRIMARY KEY (`id`),
  KEY `FK` (`abid`, `uid`)
);

CREATE TABLE `mp_Albums` (
  `abid` <type>,
  `abid_spt` <type>,
  `abid_mbz` <type>,
  PRIMARY KEY (`abid`),
  KEY `FK` (`abid_spt`, `abid_mbz`)
);

CREATE TABLE `musicbrainz_Albums` (
  `abid_mbz` <type>,
  `title` <type>,
  `......` <type>,
  PRIMARY KEY (`abid_mbz`)
);

CREATE TABLE `spotify_Albums` (
  `abid_spt` <type>,
  `title` <type>,
  `......` <type>,
  PRIMARY KEY (`abid_spt`)
);

CREATE TABLE `u_Tracks` (
  `id` <type>,
  `uid` <type>,
  `tid` <type>,
  `last_played` <type>,
  `added_at` <type>,
  `count` <type>,
  `rate` <type>,
  `memo` <type>,
  PRIMARY KEY (`id`),
  KEY `FK` (`uid`, `tid`)
);

CREATE TABLE `spotify_Tracks` (
  `tid_spt` <type>,
  `name` <type>,
  `......` <type>,
  PRIMARY KEY (`tid_spt`)
);

CREATE TABLE `mp_Tracks` (
  `tid` <type>,
  `tid_spt` <type>,
  `tid_mbz` <type>,
  `[tid_fs]` <type>,
  PRIMARY KEY (`tid`),
  KEY `FK` (`tid_spt`, `tid_mbz`, `[tid_fs]`)
);

CREATE TABLE `musicbrainz_Tracks` (
  `tid_mbz` <type>,
  `name` <type>,
  `......` <type>,
  PRIMARY KEY (`tid_mbz`)
);

CREATE TABLE `fs_Tracks` (
  `id` <type>,
  `tid` <type>,
  `path` <type>,
  `file_info` <type>,
  `tags` <type>,
  PRIMARY KEY (`id`),
  KEY `FK` (`tid`),
  KEY `Unique` (`path`)
);

CREATE TABLE `fs_Playlists` (
  `id` <type>,
  `[fs_ids]` <type>,
  `path` <type>,
  PRIMARY KEY (`id`),
  KEY `FK` (`[fs_ids]`),
  KEY `Uniq` (`path`)
);

CREATE TABLE `u_Playlists` (
  `plid` <type>,
  `uid` <type>,
  `[tids]` <type>,
  `host_id` <type>,
  `title` <type>,
  `created_at` <type>,
  `modified_at` <type>,
  `info` <type>,
  `memo` <type>,
  PRIMARY KEY (`plid`),
  KEY `FK` (`uid`, `[tids]`, `host_id`)
);


