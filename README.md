# Generic file downloader

##### Command line tool that recursively downloads files from websites with indexing enabled

### Examples
----

**Do NOT download files with all messages enabled (debug):**
```
python downloader.py --debug -u 'http://mywordpresssite/wp-content/uploads/' -t ./files
```


**Download files with all messages enabled (debug):**
```
python downloader.py --debug -u 'http://mywordpresssite/wp-content/uploads/' -t ./files -d
```

**Download files without too many messages:**
```
python downloader.py -u 'http://mywordpresssite/wp-content/uploads/' -t ./files -d
```

**Download *docx* files:**
```
python downloader.py -u 'http://mywordpresssite/wp-content/uploads/' -t ./files -d -g '.*\.docx$'
```

**Download *mp3* files:**
```
python downloader.py -u 'http://mywordpresssite/wp-content/uploads/' -t ./files -d -g '.*\.mp3$'
```

You can download any binary file as long as the website has indexes enabled or the hrefs have the file extension visible.


### Regex
---
You can provide custom regular expressions for the directories and files you want to traverse and download respectively.
Directory regex is given with the -n argument and the one for files with -g.


### Included help
---
```
$ python downloader.py --help

usage: downloader.py [-h] [-d] -u BASE_URL [-t OUTPUT_DIR]
                     [-n DIRECTORY_REGEX] [-g FILE_REGEX] [--debug]

Crawl a website for file links and download them.


arguments:
  -h, --help            show this help message and exit
  -d, --download        When provided, files are downloaded.
  -u BASE_URL, --base-url BASE_URL
                        The url to crawl for files
  -t OUTPUT_DIR, --output-dir OUTPUT_DIR
                        The local directory to store files into. Default: ./
  -n DIRECTORY_REGEX, --directory-regex DIRECTORY_REGEX
                        The directory regex of the remote site. Default:
                        '^\d+/$'
  -g FILE_REGEX, --file-regex FILE_REGEX
                        The file regex of the remote site. Default: '.*\.pdf$'
  --debug               Show debug messages
```

