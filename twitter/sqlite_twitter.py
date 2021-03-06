#!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3

import sqlite3
import MeCab
import yaml
from collections import namedtuple


class SqliteTwitter(object):
    """
    Twitter Save to the SQLite
    """
    def __init__(self):
        """
        Initial Setting
        Get the mecab dict by the yaml
        """
        Twitter = namedtuple("Twitter", ["mecab"])
        config_file = "enviroment_twitter.yml"

        with open(config_file, encoding="utf-8") as cf:
            e = yaml.load(cf)
            twitter = Twitter(e["twitter"]["mecab"])

        self.tagger = MeCab.Tagger("-Owakati -d %s" % twitter.mecab)
        conn = sqlite3.connect('./twitter_data.db')
        self.cur = conn.cursor()

    def call_sql(self):
        """
        call SQlite and save the twitter in the SQLite
        """
        self.cur.execute("""SELECT source_txt, replay_txt FROM ms_rinna;""")
        source_file = open('source_twitter_data.txt', 'w')
        replay_file = open('replay_twitter_data.txt', 'w')
        for source_txt, replay_txt in self.cur.fetchall():
            replay_file.write(self.tagger.parse(source_txt).replace("\n", "") + '\n')
            source_file.write(self.tagger.parse(replay_txt).replace('\n', '') + '\n')
        source_file.close()
        replay_file.close()

if __name__ == '__main__':
    sqlite_twitter = SqliteTwitter()
    sqlite_twitter.call_sql()
