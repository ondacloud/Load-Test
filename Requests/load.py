import requests
import time
import threading
import signal
import sys
import json
import os
import concurrent.futures
import base64
import random

# Export URL
url_endpoint = '<URL>'
url_health_path = '/healthz'
url_path = '/v1/static'

# Request_url_path
requests_processed_health = 0
requests_failed_health = 0
requests_timed_out_health = 0

requests_processed_url = 0
requests_failed_url = 0
requests_timed_out_url = 0

def send_health_request():
    global url_endpoint
    global requests_processed_health
    global requests_failed_health
    global requests_timed_out_health
    try:
        response = requests.get(url_endpoint + url_health_path, timeout=2)
        if response.status_code != 200:
            requests_failed_health += 1
        else:
            requests_processed_health += 1
    except requests.Timeout:
        requests_timed_out_health += 1

def send_url_request():
    global url_endpoint
    global requests_processed_url
    global requests_failed_url
    global requests_timed_out_url
    try:
        response = requests.get(url_endpoint + url_path, timeout=2)
        if response.status_code != 200:
            requests_failed_url += 1
        else:
            requests_processed_url += 1
    except requests.Timeout:
        requests_timed_out_url += 1

def scenario0(duration_minutes):
    while True:
        send_health_request()
        time.sleep(1)

def scenario1(duration_minutes):
    while True:
        send_url_request()
        time.sleep(1)

def scenario2(duration_minutes):
    while True:
        send_url_request()
        time.sleep(1)

def show_results():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("----health----")
        print("전체 /healthz 요청 수:", requests_processed_health + requests_failed_health + requests_timed_out_health)
        print("처리된 /healthz 요청 수:", requests_processed_health)
        print("타임아웃 된 /healthz 요청 수:", requests_timed_out_health)
        print("처리되지 않은 /healthz 요청 수:", requests_failed_health)
        print(" ")
        print("----/v1/static----")
        print("전체 /v1/static 요청 수:", requests_processed_url + requests_failed_url + requests_timed_out_url)
        print("처리된 /v1/static 요청 수:", requests_processed_url)
        print("타임아웃 된 /v1/static 요청 수:", requests_timed_out_url)
        print("처리되지 않은 /v1/static 요청 수:", requests_failed_url)
        time.sleep(1)

def signal_handler(sig, frame):
    print("Ctrl+C를 눌렀습니다. 현재까지의 결과를 출력합니다.")
    print_results()
    sys.exit(0)

def print_results():
    print("최종 결과:")
    print("처리된 /healthz 요청 수:", requests_processed_health)
    print("타임아웃 된 /healthz 요청 수:", requests_timed_out_health)
    print("처리되지 않은 /healthz 요청 수:", requests_failed_health)
    print("전체 /healthz 요청 수:", requests_processed_health + requests_failed_health + requests_timed_out_health)
    print("처리된 /v1/static 요청 수:", requests_processed_url)
    print("타임아웃 된 /v1/static 요청 수:", requests_timed_out_url)
    print("처리되지 않은 /v1/static 요청 수:", requests_failed_url)
    print("전체 /v1/static 요청 수:", requests_processed_url + requests_failed_url + requests_timed_out_url)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    print("시나리오 0 실행")
    t0 = threading.Thread(target=scenario0, args=(180*60,))
    t0.start()

    print("시나리오 1 실행")
    t1 = threading.Thread(target=scenario1, args=(180*30,))
    t1.start()

    print("시나리오 2 실행")
    t2 = threading.Thread(target=scenario2, args=(180*10,))
    t2.start()

    print("실시간 결과 표시 시작")
    t3 = threading.Thread(target=show_results)
    t3.start()

    t0.join()
    t1.join()
    t2.join()
    t3.join()

if __name__ == "__main__":
    main()