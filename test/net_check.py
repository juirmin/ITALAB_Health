import urllib3

def internet_on():
    try:
        http = urllib3.PoolManager()
        url = 'https://www.google.com/'
        if http.request('GET', url):
            return True
    except:
        return False


if __name__ == "__main__":
    print(internet_on())
