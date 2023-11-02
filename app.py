#!/usr/bin/env python3

import os
import subprocess
import re
import time
import requests
from bs4 import BeautifulSoup

def home():
    global vpn_dir, files

    os.system('clear')

    vpn_dir = "./VPN"

    files = [f for f in os.listdir(vpn_dir) if f.endswith('.ovpn')]

    print("\033[0;33m _____     ____            \033[0;36m  __  __     ____     __  __      ")
    print("\033[0;33m/\___ \   /\  _'\          \033[0;36m /\ \/\ \   /\  _'\  /\ \/\ \     ")
    print("\033[0;33m\/__/\ \  \ \ \L\_\        \033[0;36m \ \ \ \ \  \ \ \L\ \\ \ '\\ \    ")
    print("\033[0;33m   _\ \ \  \ \ \L_L        \033[0;36m  \ \ \ \ \  \ \ ,__/ \ \ , ' \   ")
    print("\033[0;33m  /\ \_\ \  \ \ \/, \      \033[0;36m   \ \ \_/ \  \ \ \/   \ \ \'\ \  ")
    print("\033[0;33m  \ \____/   \ \____/      \033[0;36m    \ '\___/   \ \_\    \ \_\ \_\ ")
    print("\033[0;33m   \/___/     \/___/       \033[0;36m     '\/__/     \/_/     \/_/\/_/ ")

    print("\n\033[0;37mmake by Garmin055\n")

    print("ctrl + c 키를 눌러 종료")
    print(f"\033[0;34m[+]\033[0;37m 현재 존재하는 프록시: {len(files)}개")
    print("=========================")
    print("\033[0;35m[\033[0;37m:\033[0;35m]\033[0;37m 명령 선택 \033[0;35m[\033[0;37m:\033[0;35m]\033[0;37m\n")
    print("\033[0;35m[\033[0;37m1\033[0;35m]\033[0;37m 프록시 선택")
    print("\033[0;35m[\033[0;37m2\033[0;35m]\033[0;37m 빠른 연결")
    print("\033[0;35m[\033[0;37m3\033[0;35m]\033[0;37m 빠른 연결(해외)")
    print("\033[0;35m[\033[0;37m4\033[0;35m]\033[0;37m 프록시 재설정")
    print("\033[0;35m[\033[0;37m5\033[0;35m]\033[0;37m 정리")
    print()

def connect_vpn(choice):
    try:
        choice = int(choice)
        if 1 <= choice <= len(files):
            selected_file = os.path.join(vpn_dir, files[choice - 1])
            print("\033[0;32m[*]\033[0;37m 프록시 연결중")
            subprocess.run(["sudo", "/opt/homebrew/opt/openvpn/sbin/openvpn", "--config", selected_file])
            print("\033[0;31m[!]\033[0;37m 프록시 연결 실패")
        else:
            print("\033[0;31m[!]\033[0;37m 프록시 연결 실패")
    except ValueError:
        print("\033[0;31m[!]\033[0;37m 프록시 연결 실패")

def ping_time(host):
    try:
        output = subprocess.check_output(["ping", "-c", "1", host]).decode("utf-8")
        
        time_value = re.findall("time=(\d+\.\d+)", output)[0]
        return float(time_value)
    except Exception as e:
        return float('inf')

def select_proxy():

    print("proxy list")
    print("==========")
    print("    #  Name")
    print("    -  ----")
    for i, file in enumerate(files):
        print(f"    \033[0;35m{i + 1}  \033[0;37m{file}")

    choice = input("\n프록시 선택: ")

    connect_vpn(choice)

from concurrent.futures import ThreadPoolExecutor, as_completed

def fast_proxy():
    print("\033[0;34m[+]\033[0;37m 빠른 프록시 찾는 중...")

    host_to_file = {}
    for file in files:
        with open(os.path.join(vpn_dir, file), 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            if line.startswith("remote"):
                host = line.split()[1]
                host_to_file[host] = file
                break

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_host = {executor.submit(ping_time, host): host for host in host_to_file}

    best_time = float('inf')
    best_file = None

    for future in as_completed(future_to_host):
        host = future_to_host[future]
        try:
            current_time = future.result()
            print(f"\033[0;32m[*]\033[0;37m ping 검사 완료 {host_to_file[host]} : {current_time}ms")
            if current_time < best_time:
                best_time = current_time
                best_file = host_to_file[host]
        except Exception as e:
            print(f"\033[0;31m[!]\033[0;37m {host_to_file[host]} 핑 실패: {e}")

    if best_file:
        print(f"\033[0;34m[+]\033[0;37m 가장 빠른 프록시: {best_file} (Ping: {best_time}ms)")
        connect_vpn(files.index(best_file) + 1)
    else:
        print("\033[0;31m[!]\033[0;37m 빠른 프록시를 찾을 수 없습니다.")


from concurrent.futures import ThreadPoolExecutor, as_completed

def fast_proxy_nk():
    print("\033[0;34m[+]\033[0;37m 빠른 프록시(해외) 찾는 중...")

    korea_keywords = ['korea', 'Korea', 'kr']
    host_to_file = {}

    for file in files:
        if not any(keyword in file for keyword in korea_keywords):
            with open(os.path.join(vpn_dir, file), 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                if line.startswith("remote"):
                    host = line.split()[1]
                    host_to_file[host] = file
                    break

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_host = {executor.submit(ping_time, host): host for host in host_to_file}

    best_time = float('inf')
    best_file = None

    for future in as_completed(future_to_host):
        host = future_to_host[future]
        try:
            current_time = future.result()
            print(f"\033[0;32m[*]\033[0;37m ping 검사 완료 {host_to_file[host]} : {current_time}ms")
            if current_time < best_time:
                best_time = current_time
                best_file = host_to_file[host]
        except Exception as e:
            print(f"\033[0;31m[!]\033[0;37m {host_to_file[host]} 핑 실패: {e}")

    if best_file:
        print(f"\033[0;34m[+]\033[0;37m 가장 빠른 해외 프록시: {best_file} (Ping: {best_time}ms)")
        connect_vpn(files.index(best_file) + 1)
    else:
        print("\033[0;31m[!]\033[0;37m 빠른 해외 프록시를 찾을 수 없습니다.")


def clear_vpn_directory(vpn_dir):
    print("\033[0;34m[+]\033[0;37m proxy 파일 제거 중...")
    for filename in os.listdir(vpn_dir):
        file_path = os.path.join(vpn_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    print("\033[0;32m[*]\033[0;37m proxy 파일 제거 완료")

def download_ovpn_files(base_url, vpn_dir):
    print("\033[0;34m[+]\033[0;37m proxy 파일 재설치 중...")
    response = requests.get(base_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    download_links = soup.select('center > div > div > div > p > a')
    print("\033[0;34m[+]\033[0;37m XPath에 해당하는 BeautifulSoup 셀렉터로 변경 완료")

    for link in download_links[3:]:
        href = link.get('href')

        download_url = f"https://www.freeopenvpn.org/{href}"
        file_name = download_url.split('/')[-1]
        download_response = requests.get(download_url)
        print(f"\033[0;34m[+]\033[0;37m {download_url} 설치 시도")
        with open(os.path.join(vpn_dir, file_name), 'wb') as file:
            file.write(download_response.content)
        print(f"\033[0;32m[*]\033[0;37m {file_name} 설치 완료")

def reload_proxy():
    vpn_dir = "./VPN"
    if not os.path.exists(vpn_dir):
        os.makedirs(vpn_dir)
    
    clear_vpn_directory(vpn_dir)

    country_urls = [
        'https://www.freeopenvpn.org/private.php?cntid=Korea&lang=en',
        'https://www.freeopenvpn.org/private.php?cntid=Japan&lang=en',
        'https://www.freeopenvpn.org/private.php?cntid=USA&lang=en'
    ]

    for url in country_urls:
        print("\033[0;34m[+]\033[0;37m 국가 설정 완료")
        download_ovpn_files(url, vpn_dir)

home()

while True:
    com = input("\033[0;35m[\033[0;37m+\033[0;35m]\033[0;37m 명령 선택 : ")
    if com == "1":
        select_proxy()
    elif com == "2":
        fast_proxy()
    elif com == "3":
        fast_proxy_nk()
    elif com == "4":
        reload_proxy()
        home()
    elif com == "5":
        home()

    else:
        print("\033[0;31m[!]\033[0;37m 존재하지 않는 명령입니다.")