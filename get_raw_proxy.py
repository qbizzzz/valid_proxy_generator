import requests
import bs4


result_ip = []

def get_html(url="https://free-proxy-list.net/"):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        return None



def get_raw_proxy():
    html = get_html()
    result_ip = []
    if html is None:
        return result_ip
    else:
        soup = bs4.BeautifulSoup(html, "lxml")
        raw_info = soup.find("tbody").find_all("tr")

        for i in raw_info:
            ip = i.find_all("td")[0].text
            port = i.find_all("td")[1].text
            result_ip.append(ip + ":" + port)
    return result_ip


if __name__ == "__main__":
    print(get_raw_proxy())
    









#print(result_ip)
