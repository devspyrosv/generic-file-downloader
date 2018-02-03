import bs4
import requests
import re
import shutil
import sys
import time
import argparse


def recurse(base_url: str, file_urls: list, link_regex: dict):
    """
    Walk recursively and follow only specific urls
    @:param base_url
    @:param file_urls
    @:param link_regex
    """
    r = requests.get(base_url)
    if r.status_code != 200:
        return
    else:
        if DEBUG:
            print("Directory " + base_url)

    data = bs4.BeautifulSoup(r.text, "html.parser")
    for link in data.find_all("a", href=True):
        if re.match(link_regex.get('directory'), link['href']):
            if re.match(link_regex.get('directory'), link['href']):
                recurse(base_url=base_url + link['href'], file_urls=file_urls, link_regex=link_regex)
            else:                            
                recurse(base_url=base_url + link['href'], file_urls=file_urls, link_regex=link_regex)
        elif re.match(link_regex.get('file'), link['href']):
            file_urls.append(base_url + link['href'])
            if DEBUG:
                print("File: {}".format(link['href']))


def download_file(directory: str, file_url: str):
    """
    Download a file residing in file_url inside directory
    @:param directory
    @:param file_url
    """
    if directory[-1] != '/':
        directory = directory + '/'

    output_file = directory + file_url.split('/')[-1]
    r = requests.get(file_url, stream=True)
    with open(output_file, 'wb') as fp:
        shutil.copyfileobj(r.raw, fp)
    return output_file


def start_crawl(config):
    """
    Crawl the website
    :return:
    """
    cur_file_no = 1

    file_list = []

    # Follow links recursively
    recurse(base_url=config.get('base_url'), file_urls=file_list,
            link_regex=config.get('link_regular_expressions'))

    total_files = len(file_list)

    print("Got {} total files. Starting download.".format(total_files))

    for item in file_list:
        if not DRY_RUN:
            download_file(config.get('directory'), item)

        if DEBUG and not DRY_RUN:
            print("Downloaded: {item}, file {current}/{total}".format(item=item, current=cur_file_no,
                                                                      total=total_files))
        else:
            print("{0:.2f}% of total files downloaded.".format(cur_file_no / total_files * 100), end='\r')
            sys.stdout.flush()
            if DEBUG and DRY_RUN:
                time.sleep(0.1)

        cur_file_no += 1


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Crawl a website for file links and download them.')
    parser.add_argument('-d', '--download', help='When provided, files are downloaded.', default=False,
                        action='store_true')
    parser.add_argument('-u', '--base-url', help='The url to crawl for files', default=None,
                        action='store', required=True)
    parser.add_argument('-t', '--output-dir', help='The local directory to store files into. Default: ./',
                        default='./',
                        action='store', required=False)
    parser.add_argument('-n', '--directory-regex', help='The directory regex of the remote site. Default: \'^\d+/$\'',
                        default='^\d+/$',
                        action='store', required=False)
    parser.add_argument('-g', '--file-regex', help='The file regex of the remote site. Default: \'.*\.pdf$\'',
                        default='.*\.pdf$',
                        action='store', required=False)

    parser.add_argument('--debug', help='Show debug messages', default=False,
                        action='store_true')

    args = parser.parse_args()

    DEBUG = args.debug
    DRY_RUN = not args.download

    """
    Configuration dict
    'base_url': The base url to crawl for file links    
    'link_regular_expressions': The dict containing regular expressions for the directories and files
    'directory': The local directory where the files are going to be stored
    'dry_run': Boolean. When True it stops files from downloading. Controlled by argument.
    """

    configuration = {
        'base_url': args.base_url,
        'link_regular_expressions': {
            'directory': args.directory_regex,
            'file': args.file_regex,
        },
        'directory': args.output_dir,
    }

    sys.exit(start_crawl(configuration))

