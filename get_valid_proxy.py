import concurrent.futures
import requests
from collections import deque
import get_raw_proxy as gr


def put_in_queue(raw_proxy_list):
    q = deque()
    for proxy in raw_proxy_list:
        q.append(proxy)
    return q


def check_proxies(proxy):
    try:
        response = session.get("https://api.ipify.org", proxies={"http": proxy, "https": proxy}, timeout=4)
        if response.status_code == 200:
            print(f"Valid proxy: {proxy}")
            return proxy
    except requests.exceptions.Timeout:
        print(f"Proxy timed out: {proxy}")
        return None
    except requests.exceptions.RequestException:
        print(f"Error occurred with proxy: {proxy}")
        return None


def make_threads():
    threads = []
    for _ in range(10):
        t = threading.Thread(target=check_proxies)
        threads.append(t)
    print("Threads created.")
    return threads
    

def start_threads():
    threads = make_threads()
    print("Starting threads...")
    for t in threads:
        t.start()
        t.join()


def save_valid_proxies(valid_proxies):
    with open("valid_proxy.txt", "w") as f:
        f.write("\n".join(valid_proxies))


if __name__ == "__main__":
    valid_proxy = []

    raw_proxy_list = gr.get_raw_proxy()
    q = put_in_queue(raw_proxy_list)

    session = requests.Session()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_proxies, proxy) for proxy in q]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                valid_proxy.append(result)

    save_valid_proxies(valid_proxy)
    print(f"Total valid proxies: {len(valid_proxy)}")
    print("Valid proxies saved to valid_proxy.txt")
