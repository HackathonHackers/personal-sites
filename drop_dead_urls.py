import re
import requests


def return_url(s):
    url = s.strip().split(' ')[-1]
    if url.startswith('http'):
        return url
    elif url.startswith('['):
        url = re.search('\[(.+?)\]', url)
        if url:
            return url.group(1)
    else:
        return 'http://' + url


def check_line_for_reachable_url(line, file):
    if line.startswith('- '):
        url = return_url(line)
        try:
            get = requests.get(url, timeout=5)
            if get.status_code == 200:
                print(line)
                file.write(line)
        except Exception as e:
            print(e)
    else:
        file.write(line)
        print(line)


def drop_dead_urls():
    with open('README.md', "r") as f:
        lines = f.readlines()
    with open('README.md', "w") as f:
        # multiprocessing?
        for line in lines:
            check_line_for_reachable_url(line, f)


if __name__ == '__main__':
    drop_dead_urls()
