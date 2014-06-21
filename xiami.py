# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:33:08 2013

@author: latyas
"""

import sys
try:
    import xmltodict
except:
    print('missing library: xmltodict')
    sys.exit(0)
try:
    import requests
except:
    print('missing library: requests')
    sys.exit(0)

try:
    import urllib2
except:
    import urllib.parse as urllib2
import os


try:
    from BeautifulSoup import BeautifulSoup
except:
    print('missing library: xmltodict')
    sys.exit(0)

import json
import getopt

# if you wish getting a VIP account, pls contact me.

username = 'USERNAME'
password = 'PASSWORD'
axel_opts = '-n5'


def text_validate(text):
    return text.replace('\'', '').replace('\\', '').replace('/', '')


def set_320k(s):
    url = 'http://www.xiami.com/vip/myvip'
    header = {'user-agent': 'Mozilla/5.0',
              'Referer': 'http://img.xiami.com/static/swf/seiya/'
                         'player.swf?v=1394535902294'}

    ret = s.get(url, headers=header).text
    bs = BeautifulSoup(ret)
    user_id = bs.find('input', attrs={'id': 'user_id'}).get('value')
    data = {'user_id': user_id,
            'tone_type': '1',
            '_xiamitoken': s.cookies.get('_xiamitoken')
            }

    ret = s.post('http://www.xiami.com/vip/update-tone', data=data,
                 headers=header)

    ret = json.loads(ret.text)
    if ret['info'] == 'success':
        print('Qualities of the songs have been set to 320kbps.')
    else:
        print('You are not a VIP, songs will be downloaded'
              ' with normal quality.')


def xiami(s):
    start = s.find('h')
    row = int(s[0:start])
    length = len(s[start:])
    column = length / row
    output = ''
    real_s = list(s[1:])
    sucks = []
    suck = length % row  # = 0 -> good! if not , sucks!
    for i in range(1, suck+1):
        sucks.append(real_s[i*(column)])
        real_s[i*(column)] = 'sucks'
        real_s.remove('sucks')
    for i in range(column):
        output += ''.join(real_s[i:][slice(0, length, column)])
    output += ''.join(sucks)
    return urllib2.unquote(output).replace('^', '0')


def usage():
    print('''Usage: %s --type=album/songlist/single \
          [--remove] [--320k] [--onefolder] id_list \
                 --remove: delete files if already existed \
                 --320k: download for 320kbps primarily (VIP needed) \
                 --onefolder: all musics will be downloaded into one folder \
                 "songlist_listid", if type is songlist''' % (sys.argv[0]))


def exception():
    usage()
    sys.exit(1)


def login(s):
    header = {'user-agent': 'Mozilla/5.0'}
    login_url = 'https://login.xiami.com/member/login'
    data = {'email': username,
            'password': password,
            'done': 'http://www.xiami.com/account',
            'submit': '登 录'}

    s.post(login_url, data=data, headers=header)


def download(s, album_type, id):
    global arg_remove, arg_onefolder
    if album_type != 'single':
        foo = s.get('http://www.xiami.com/song/playlist/id/'
                    '%s/type/%s' % (id, album_type),
                    headers={'user-agent': 'Mozilla/5.0'}).text
    else:
        foo = s.get('http://www.xiami.com/song/playlist/id/%s' % (id),
                    headers={'user-agent': 'Mozilla/5.0'}).text

    data = xmltodict.parse(foo)['playlist']['trackList']['track']

    delete_all = arg_remove

    if arg_onefolder is True:
        if not os.path.exists('songlist_%s' % id):
            print('Creating folder')
            os.system('mkdir \'%s\'' % ('songlist_%s' % id))
    if album_type != 'single':
        for i in data:
            if arg_onefolder is not True:
                folder = text_validate(i['album_name'])
                if not os.path.exists(folder):
                    print('Creating folder')
                    os.system('mkdir \'%s\'' % folder)
                if not os.path.exists('%s/cover.jpg' % (folder)):
                    print('Downloading cover ...')
                    os.system('curl \'%s\' > \'%s/cover.jpg\'' % (
                              i['album_pic'].replace('_1', ''),
                              folder)
                              )
            else:
                folder = 'songlist_%s' % id

            if not hq:
                url = xiami(i['location'])
            else:
                url = xiami(json.loads(req.get(
                            'http://www.xiami.com/song/gethqsong/sid/'
                            + i['song_id'], headers=header).text)['location'])

            print('Downloading', i['title'])

            if os.path.exists('%s/%s.mp3' % (folder,
                              text_validate(i['title']))):

                if not delete_all:
                    foofoo = raw_input('%s existed, '
                                       'do you want to delete it?'
                                       '(yes/ALL for files existed/'
                                       'others for skipping)'
                                       % i['title'])

                    if foofoo == 'ALL':
                        delete_all = True

                    if foofoo != 'yes' and foofoo != 'ALL':
                        print('skipped')
                        continue

                os.system('rm \'%s/%s.mp3\''
                          % (folder, text_validate(i['title'])))

            os.system('axel -n5 --user-agent="Mozilla/5.0" %s -o \'%s\''
                      % (url, '%s/%s.mp3' % (folder,
                                             text_validate(i['title']))))
    else:
        if not hq:
            url = xiami(data['location'])
        else:
            url = xiami(json.loads(
                        req.get('http://www.xiami.com/song/gethqsong/sid/'
                                + data['song_id'],
                                headers=header).text)['location'])

        folder = 'singles'

        if not os.path.exists(folder):
            print('Creating [singles] folder')
            os.system('mkdir \'%s\'' % folder)

        print('Downloading', data['title'])
        if os.path.exists('%s/%s.mp3' % (folder, text_validate(data['title']))):

            if not delete_all:
                foofoo = raw_input('%s existed, delete?'
                                   '(yes/ALL for files existed/others to skip)'
                                   % data['title'])

                if foofoo == 'ALL':
                    delete_all = True

                if foofoo != 'yes' and foofoo != 'ALL':
                    print('skipped')

            os.system('rm \'%s/%s.mp3\''
                      % (folder, text_validate(data['title'])))

        os.system('axel -n5 --user-agent="Mozilla/5.0" %s -o \'%s\''
                  % (url, '%s/%s.mp3'
                          % (folder, text_validate(data['title']))))

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    arg_remove = False
    arg_lists = []
    arg_type = ''
    hq = False  # high quality switch
    arg_onefolder = False

    opts, args = getopt.getopt(sys.argv[1:],
                               'h',
                               ['remove', 'type=', 'help', '320k', 'onefolder'])

    foo = [i[0] for i in opts]
    if '--type' not in foo or args == []:
        exception()

    for o, v in opts:
        if o == '--remove':
            arg_remove = True
        elif o == '--type' and v != '':
            if v == 'album':
                arg_type = '1'
            elif v == 'songlist':
                arg_type = '3'
            elif v == 'single':
                arg_type = 'single'
            else:
                exception()
        elif o == '--320k':
            hq = True
        elif o == '--onefolder' and ('--type', 'songlist') in opts:
            arg_onefolder = True
        elif o == '--help':
            exception()
        else:
            print('unrecognized argument', o)
            exception()
    # song list
    arg_lists.extend(args)

    header = {'user-agent': 'Mozilla/5.0',
			  'Referer': 'http://img.xiami.com/static/swf/seiya/player.swf?v=1394535902294'}

    album = sys.argv[1]
    list_type = sys.argv[2]

    req = requests.session()

    login(req)
    if hq:
        set_320k(req)  # set quality to 320kbps

    for i in arg_lists:
        print('id:%s' % i)
        download(req, arg_type, i)
