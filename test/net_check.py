import urllib3

def internet_on():
    try:
        http = urllib3.PoolManager()
        url = 'https://healthy-api.huakai.com.tw/'
        if http.request('GET', url):
            return True
    except:
        return False


if __name__ == "__main__":
    print(internet_on())
