xiami-downloader
================

由于调用axel，目前仅支持linux系。本人是axel的脑残粉。
curl有windows版本，同理可以将axel换成curl下载。

范例：
下载专辑地址：http://www.xiami.com/album/1890715345
python xiami.py --type=album 1890715345 

如果要下载高清，首先需要vip
python xiami.py --type=album --320k 1890715345 


下载用户精选集：http://www.xiami.com/song/showcollect/id/28243855
python xiami.py --type=songlist 28243855

下载单曲 http://www.xiami.com/song/1772511950
python xiami.py --type=single 1772511950
