import requests
import concurrent.futures
import colorama
from colorama import Fore, Style
import time
from bs4 import BeautifulSoup
import threading
import os
import platform
import psutil
import urllib3
import sys

class ProxyFinder:
    def __init__(self):
        try:
            colorama.init(autoreset=True)
            self.proxies = set()
            self.working_proxies = []
            self.lock = threading.Lock()
            self.proxy_lock = threading.Lock()
            self.start_time = time.time()
            self.timeout = 5
            self.thread_count = min(50, (os.cpu_count() or 1) * 2)
            self.target_region = None
            self.error_count = 0
            self.session = requests.Session()
            self.session.verify = False
            self.session.timeout = self.timeout
            
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        except Exception as e:
            print(f"Başlatma hatası: {str(e)}")
            sys.exit(1)

    def print_banner(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        banner = f"""
{Fore.CYAN}╔════════════════════════════════════╗
║      {Fore.YELLOW}TR PROXY FINDER V2.0{Fore.CYAN}        ║
╟────────────────────────────────────╢
║  {Fore.YELLOW}Developer: {Fore.GREEN}github.com/mehmetTRX{Fore.CYAN}  ║
║  {Fore.YELLOW}Telegram: {Fore.GREEN}t.me/mhmetrr{Fore.CYAN}          ║
║  {Fore.YELLOW}Discord: {Fore.GREEN}discord.gg/mhmetr{Fore.CYAN}      ║
║  {Fore.YELLOW}Instagram: {Fore.GREEN}instagram.com/phicel0l{Fore.CYAN}║
╚════════════════════════════════════╝

{Fore.YELLOW}[*] Sistem Bilgileri:
{Fore.WHITE}    → İşletim Sistemi: {platform.system()} {platform.release()}
    → CPU Kullanımı: {psutil.cpu_percent()}%
    → RAM Kullanımı: {psutil.virtual_memory().percent}%

{Fore.RED}[1] {Fore.WHITE}Proxy Aramaya Başla
{Fore.RED}[2] {Fore.WHITE}Proxy Listesini Görüntüle
{Fore.RED}[3] {Fore.WHITE}Proxy Test Et
{Fore.RED}[4] {Fore.WHITE}Oyun Proxyleri
{Fore.RED}[5] {Fore.WHITE}Platform Proxyleri
{Fore.RED}[6] {Fore.WHITE}Ülke Proxyleri
{Fore.RED}[7] {Fore.WHITE}Çıkış
"""
        print(banner)

    def check_proxy(self, proxy, proxy_type="http"):
        if not self.validate_proxy_format(proxy):
            return False
        
        try:
            start = time.time()
            proxies = {
                'http': f'{proxy_type}://{proxy}',
                'https': f'{proxy_type}://{proxy}'
            }
            
            with self.session.get(
                'http://ip-api.com/json',
                proxies=proxies,
                timeout=self.timeout,
                allow_redirects=False
            ) as response:
                speed = round(time.time() - start, 2)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('status') == 'success':
                            country_code = data.get('countryCode', '')
                            if not self.target_region or country_code == self.target_region:
                                with self.lock:
                                    self.working_proxies.append((proxy, speed, country_code))
                                return True
                    except ValueError:
                        pass
                return False
        except Exception:
            with self.proxy_lock:
                self.error_count += 1
            return False

    def fetch_proxies(self, proxy_type="http"):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            self.session.headers.update(headers)
            
            sources = {
                "http": [
                    # API Kaynakları
                    f'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&country={self.target_region}&ssl=all',
                    f'https://www.proxy-list.download/api/v1/get?type=http&country={self.target_region}',
                    'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&ssl=yes',
                    'https://www.proxy-list.download/api/v1/get?type=https',
                    'https://api.openproxylist.xyz/http.txt',
                    f'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&protocols=http%2Chttps&country={self.target_region}',
                    'https://api.proxyscan.io/v1/proxies?protocol=http',
                    'https://api.proxyscan.io/v1/proxies?protocol=https',
                    f'https://api.getproxylist.com/proxy?protocol=http&country={self.target_region}',
                    
                    # Github Repo Kaynakları
                    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
                    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
                    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
                    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
                    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
                    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
                    'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
                    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
                    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
                    'https://raw.githubusercontent.com/MuRongPIG/Proxy-List/main/http.txt',
                    'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
                    'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt',
                    'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
                    'https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt',
                    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
                    'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt',
                    'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt',
                    'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt',
                    'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt',
                    'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
                    'https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt',
                    'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt',
                    
                    # Diğer Kaynaklar
                    f'https://proxyspace.pro/http.txt?country={self.target_region}',
                    f'https://www.proxy-list.download/api/v1/get?type=http&anon=elite&country={self.target_region}',
                    'https://www.proxyscan.io/download?type=http',
                    'https://www.proxy-list.download/api/v1/get?type=http&anon=anonymous',
                    f'https://advanced.name/freeproxy?type=http&country={self.target_region}',
                    'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
                    'http://spys.me/proxy.txt',
                    'https://www.proxy-list.download/api/v1/get?type=http&anon=transparent'
                ],
                "socks4": [
                    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4',
                    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
                    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
                    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
                    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt',
                    'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt',
                    'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt',
                    'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt',
                    'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt',
                    'https://www.proxy-list.download/api/v1/get?type=socks4',
                    'https://api.proxyscan.io/v1/proxies?protocol=socks4',
                    'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt'
                ],
                "socks5": [
                    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5',
                    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
                    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
                    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
                    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt',
                    'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt',
                    'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt',
                    'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt',
                    'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt',
                    'https://www.proxy-list.download/api/v1/get?type=socks5',
                    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
                    'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt',
                    'https://api.proxyscan.io/v1/proxies?protocol=socks5',
                    'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt'
                ]
            }

            if proxy_type == "all":
                all_sources = []
                for protocol_sources in sources.values():
                    all_sources.extend(protocol_sources)
                current_sources = all_sources
            else:
                current_sources = sources.get(proxy_type, sources["http"])

            max_proxies = 5000
            chunk_size = 1024
            retry_count = 3
            
            for url in current_sources:
                if len(self.proxies) >= max_proxies:
                    break
                
                for _ in range(retry_count):
                    try:
                        with self.session.get(url, stream=True, timeout=10) as response:
                            if response.status_code == 200:
                                content_type = response.headers.get('content-type', '').lower()
                                
                                if 'application/json' in content_type:
                                    self._handle_json_response(response)
                                else:
                                    self._handle_text_response(response, chunk_size, max_proxies)
                                    
                                break
                    except Exception:
                        continue
                    
        except Exception as e:
            print(f"\n{Fore.RED}[!] Proxy toplama hatası: {str(e)}")

    def _handle_json_response(self, response):
        try:
            json_data = response.json()
            if isinstance(json_data, dict) and 'data' in json_data:
                for item in json_data['data']:
                    if isinstance(item, dict):
                        ip = item.get('ip')
                        port = item.get('port')
                        if ip and port:
                            proxy = f"{ip}:{port}"
                            if self.validate_proxy_format(proxy):
                                with self.proxy_lock:
                                    self.proxies.add(proxy)
        except Exception:
            pass

    def _handle_text_response(self, response, chunk_size, max_proxies):
        try:
            for chunk in response.iter_content(chunk_size=chunk_size, decode_unicode=True):
                if chunk:
                    try:
                        lines = chunk.decode('utf-8', errors='ignore').splitlines()
                        for line in lines:
                            proxy = line.strip()
                            if self.validate_proxy_format(proxy):
                                with self.proxy_lock:
                                    self.proxies.add(proxy)
                                    if len(self.proxies) >= max_proxies:
                                        return
                    except UnicodeDecodeError:
                        continue
        except Exception:
            pass

    def validate_proxy_format(self, proxy):
        try:
            if not proxy or ':' not in proxy:
                return False
            
            ip, port = proxy.split(':')
            ip_parts = ip.split('.')
            
            if len(ip_parts) != 4:
                return False
            
            for part in ip_parts:
                if not part.isdigit() or not 0 <= int(part) <= 255:
                    return False
            
            if not port.isdigit() or not 1 <= int(port) <= 65535:
                return False
            
            return True
        except:
            return False

    def save_proxies(self, filename, region=None):
        if not self.working_proxies:
            print(f"\n{Fore.RED}[!] Kaydedilecek proxy bulunamadı!")
            return False
        
        try:
            temp_filename = f"{filename}.tmp"
            with open(temp_filename, "w", encoding='utf-8') as f:
                f.write(f"# {'TR' if not region else region} Proxy Listesi - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Toplam: {len(self.working_proxies)} proxy\n\n")
                for proxy, speed in sorted(self.working_proxies, key=lambda x: x[1]):
                    f.write(f"{proxy} # Hız: {speed}s\n")
                
            if os.path.exists(filename):
                os.replace(temp_filename, filename)
            else:
                os.rename(temp_filename, filename)
                
            print(f"\n{Fore.GREEN}[+] {len(self.working_proxies)} proxy {filename} dosyasına kaydedildi!")
            
            print(f"\n{Fore.CYAN}[*] En Hızlı 5 Proxy:")
            for proxy, speed in sorted(self.working_proxies, key=lambda x: x[1])[:5]:
                print(f"{Fore.GREEN}    → {proxy} (Hız: {speed}s)")
                
            return True
            
        except Exception as e:
            print(f"\n{Fore.RED}[!] Dosya kaydetme hatası: {str(e)}")
            if os.path.exists(temp_filename):
                try:
                    os.remove(temp_filename)
                except:
                    pass
            return False

    def run(self, region=None, proxy_type="http"):
        try:
            self.target_region = region
            print(f"\n{Fore.YELLOW}[*] Proxyler toplanıyor...")
            self.fetch_proxies(proxy_type)
            
            if not self.proxies:
                print(f"{Fore.RED}[!] Hiç proxy bulunamadı!")
                return False
            
            print(f"{Fore.GREEN}[+] {len(self.proxies)} proxy bulundu!")
            print(f"{Fore.YELLOW}[*] Proxyler test ediliyor...")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count) as executor:
                list(executor.map(self.check_proxy, self.proxies))
                
            if self.error_count > 0:
                print(f"{Fore.YELLOW}[!] {self.error_count} proxy test edilirken hata oluştu.")
                
            return bool(self.working_proxies)
        except Exception as e:
            print(f"\n{Fore.RED}[!] Hata: {str(e)}")
            return False
        finally:
            self.target_region = None
            self.error_count = 0

    def menu(self):
        while True:
            self.print_banner()
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Seçiminiz: {Fore.WHITE}")
                
                if choice == "1":
                    self.proxies.clear()
                    self.working_proxies.clear()
                    self.run()
                    input(f"\n{Fore.YELLOW}[?] Devam etmek için Enter'a basın...")
                elif choice == "2":
                    if os.path.exists("working_tr_proxies.txt"):
                        with open("working_tr_proxies.txt", "r") as f:
                            print(f"\n{Fore.GREEN}[+] Çalışan Proxyler:")
                            print(f.read())
                    else:
                        print(f"\n{Fore.RED}[!] Proxy listesi bulunamadı!")
                    input(f"\n{Fore.YELLOW}[?] Devam etmek için Enter'a basın...")
                elif choice == "3":
                    proxy = input(f"\n{Fore.YELLOW}[?] Test edilecek proxy (ip:port): {Fore.WHITE}")
                    if self.validate_proxy_format(proxy):
                        if self.check_proxy(proxy):
                            print(f"\n{Fore.GREEN}[+] Proxy çalışıyor: {proxy}")
                        else:
                            print(f"\n{Fore.RED}[-] Proxy çalışmıyor: {proxy}")
                    else:
                        print(f"\n{Fore.RED}[!] Geçersiz proxy formatı!")
                    input(f"\n{Fore.YELLOW}[?] Devam etmek için Enter'a basın...")
                elif choice == "4":
                    self.game_proxy_menu()
                elif choice == "5":
                    self.platform_proxy_menu()
                elif choice == "6":
                    self.country_proxy_menu()
                elif choice == "7":
                    print(f"\n{Fore.YELLOW}[*] Program sonlandırılıyor...")
                    break
                else:
                    print(f"\n{Fore.RED}[!] Geçersiz seçim!")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}[!] Program sonlandırıldı!")
                break
            except Exception as e:
                print(f"\n{Fore.RED}[!] Hata: {str(e)}")
                time.sleep(1)

    def game_proxy_menu(self):
        while True:
            os.system('cls' if platform.system() == 'Windows' else 'clear')
            print(f"""
{Fore.CYAN}╔════════���═══════════════════════════╗
║         {Fore.YELLOW}OYUN PROXY MENÜSÜ{Fore.CYAN}         ║
╚════════════════════════════════════╝

{Fore.RED}[1] {Fore.WHITE}CraftRise Proxy {Fore.YELLOW}(TR)
{Fore.RED}[2] {Fore.WHITE}Zula Proxy {Fore.YELLOW}(TR)
{Fore.RED}[3] {Fore.WHITE}DarkOrbit Proxy {Fore.YELLOW}(TR/US)
{Fore.RED}[4] {Fore.WHITE}Sonoyuncu Proxy {Fore.YELLOW}(TR)
{Fore.RED}[5] {Fore.WHITE}Ana Menüye Dön

{Fore.CYAN}[*] {Fore.WHITE}Not: Parantez içindeki ülkeler önerilen proxy lokasyonlarıdır.
""")
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Seçiminiz: {Fore.WHITE}")
                
                if choice == "1":
                    print(f"\n{Fore.YELLOW}[*] CraftRise için TR proxy aranıyor...")
                    self.find_game_proxy("craftrise", "TR")
                elif choice == "2":
                    print(f"\n{Fore.YELLOW}[*] Zula için TR proxy aranıyor...")
                    self.find_game_proxy("zula", "TR")
                elif choice == "3":
                    while True:
                        print(f"\n{Fore.YELLOW}[1] {Fore.WHITE}TR Proxy")
                        print(f"{Fore.YELLOW}[2] {Fore.WHITE}US Proxy")
                        region = input(f"\n{Fore.YELLOW}[?] Proxy bölgesi seçin: {Fore.WHITE}")
                        if region in ["1", "2"]:
                            self.find_game_proxy("darkorbit", "TR" if region == "1" else "US")
                            break
                elif choice == "4":
                    print(f"\n{Fore.YELLOW}[*] Sonoyuncu için TR proxy aranıyor...")
                    self.find_game_proxy("sonoyuncu", "TR")
                elif choice == "5":
                    break
                else:
                    print(f"\n{Fore.RED}[!] Geçersiz seçim!")
                    time.sleep(1)
                    
                if choice in ["1", "2", "3", "4"]:
                    input(f"\n{Fore.YELLOW}[?] Devam etmek için Enter'a basın...")
                    
            except Exception as e:
                print(f"\n{Fore.RED}[!] Hata: {str(e)}")
                time.sleep(1)

    def find_game_proxy(self, game, region):
        print(f"{Fore.YELLOW}[*] {game.capitalize()} için {region} proxy'ler aranıyor...")
        self.proxies.clear()
        self.working_proxies.clear()
        
        # Her oyun için özel proxy gereksinimleri
        if game == "craftrise":
            self.timeout = 5
            self.thread_count = 50
        elif game == "zula":
            self.timeout = 3
            self.thread_count = 100
        elif game == "darkorbit":
            self.timeout = 8
            self.thread_count = 30
        elif game == "sonoyuncu":
            self.timeout = 5
            self.thread_count = 50
            
        self.run(region)
        
        # Sonuçları oyuna özel dosyaya kaydet
        if self.working_proxies:
            filename = f"working_{game}_{region.lower()}_proxies.txt"
            with open(filename, "w") as f:
                f.write(f"# {game.capitalize()} {region} Proxy Listesi - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Toplam: {len(self.working_proxies)} proxy\n\n")
                for proxy, speed in self.working_proxies:
                    f.write(f"{proxy} # Hız: {speed}s\n")
                    
            print(f"\n{Fore.GREEN}[+] {len(self.working_proxies)} proxy {filename} dosyasına kaydedildi!")

    def platform_proxy_menu(self):
        while True:
            os.system('cls' if platform.system() == 'Windows' else 'clear')
            print(f"""
{Fore.CYAN}╔════════════════════════════════════╗
║       {Fore.YELLOW}PLATFORM PROXY MENÜSÜ{Fore.CYAN}       ║
╚════════════════════════════════════╝

{Fore.RED}[1] {Fore.WHITE}EXXEN Proxy {Fore.YELLOW}(TR)
{Fore.RED}[2] {Fore.WHITE}BluTV Proxy {Fore.YELLOW}(TR/US)
{Fore.RED}[3] {Fore.WHITE}Netflix Proxy {Fore.YELLOW}(TR/US/EU/UK/AZ/CN/FR)
{Fore.RED}[4] {Fore.WHITE}Ana Menüye Dön

{Fore.CYAN}[*] {Fore.WHITE}Not: Parantez içindeki ülkeler desteklenen lokasyonlardır.
""")
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Seçiminiz: {Fore.WHITE}")
                
                if choice == "1":
                    print(f"\n{Fore.YELLOW}[*] EXXEN için TR proxy aranıyor...")
                    self.find_platform_proxy("exxen", "TR")
                elif choice == "2":
                    while True:
                        print(f"\n{Fore.YELLOW}[1] {Fore.WHITE}TR Proxy")
                        print(f"{Fore.YELLOW}[2] {Fore.WHITE}US Proxy")
                        region = input(f"\n{Fore.YELLOW}[?] Proxy bölgesi seçin: {Fore.WHITE}")
                        if region in ["1", "2"]:
                            self.find_platform_proxy("blutv", "TR" if region == "1" else "US")
                            break
                elif choice == "3":
                    while True:
                        print(f"\n{Fore.YELLOW}[1] {Fore.WHITE}TR Proxy")
                        print(f"{Fore.YELLOW}[2] {Fore.WHITE}US Proxy")
                        print(f"{Fore.YELLOW}[3] {Fore.WHITE}EU Proxy")
                        print(f"{Fore.YELLOW}[4] {Fore.WHITE}UK Proxy")
                        print(f"{Fore.YELLOW}[5] {Fore.WHITE}AZ Proxy")
                        print(f"{Fore.YELLOW}[6] {Fore.WHITE}CN Proxy")
                        print(f"{Fore.YELLOW}[7] {Fore.WHITE}FR Proxy")
                        region = input(f"\n{Fore.YELLOW}[?] Proxy bölgesi seçin: {Fore.WHITE}")
                        regions = {"1": "TR", "2": "US", "3": "EU", "4": "UK", "5": "AZ", "6": "CN", "7": "FR"}
                        if region in regions:
                            self.find_platform_proxy("netflix", regions[region])
                            break
                elif choice == "4":
                    break
                else:
                    print(f"\n{Fore.RED}[!] Geçersiz seçim!")
                    time.sleep(1)
                    
                if choice in ["1", "2", "3"]:
                    input(f"\n{Fore.YELLOW}[?] Devam etmek için Enter'a basın...")
                    
            except Exception as e:
                print(f"\n{Fore.RED}[!] Hata: {str(e)}")
                time.sleep(1)

    def find_platform_proxy(self, service, region):
        print(f"{Fore.YELLOW}[*] {service.capitalize()} için {region} proxy'ler aranıyor...")
        self.proxies.clear()
        self.working_proxies.clear()
        
        # Her streaming servisi için özel proxy gereksinimleri
        if service == "exxen":
            self.timeout = 5
            self.thread_count = 50
        elif service == "blutv":
            self.timeout = 5
            self.thread_count = 50
        elif service == "netflix":
            self.timeout = 8
            self.thread_count = 30
            
        self.run(region)
        
        if self.working_proxies:
            filename = f"working_{service}_{region.lower()}_proxies.txt"
            with open(filename, "w") as f:
                f.write(f"# {service.capitalize()} {region} Proxy Listesi - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Toplam: {len(self.working_proxies)} proxy\n\n")
                for proxy, speed in self.working_proxies:
                    f.write(f"{proxy} # Hız: {speed}s\n")
                    
            print(f"\n{Fore.GREEN}[+] {len(self.working_proxies)} proxy {filename} dosyasına kaydedildi!")

    def country_proxy_menu(self):
        countries = {
            "1": ("TR", "Türkiye"),
            "2": ("US", "Amerika"),
            "3": ("DE", "Almanya"),
            "4": ("GB", "İngiltere"),
            "5": ("FR", "Fransa"),
            "6": ("NL", "Hollanda"),
            "7": ("IT", "İtalya"),
            "8": ("ES", "İspanya"),
            "9": ("RU", "Rusya"),
            "10": ("JP", "Japonya"),
            "11": ("CN", "Çin"),
            "12": ("BR", "Brezilya"),
            "13": ("CA", "Kanada"),
            "14": ("AU", "Avustralya"),
            "15": ("IN", "Hindistan")
        }
        
        while True:
            os.system('cls' if platform.system() == 'Windows' else 'clear')
            print(f"""
{Fore.CYAN}╔════════════════════════════════════╗
║         {Fore.YELLOW}ÜLKE PROXY MENÜSÜ{Fore.CYAN}         ║
╚════════════════════════════════════╝
""")
            
            # Ülkeleri düzenli bir şekilde yazdır
            for i in range(0, len(countries), 3):
                row = []
                for j in range(3):
                    if i + j < len(countries):
                        key = str(i + j + 1)
                        code, name = countries[key]
                        # Her ülke için sabit genişlik kullan
                        row.append(f"{Fore.RED}[{key:2}] {Fore.WHITE}{name:<10} {Fore.YELLOW}({code})")
                print("     ".join(row))  # Sütunlar arası boşluğu artırdık
                
            print(f"\n{Fore.RED}[0] {Fore.WHITE}Ana Menüye Dön")
            print(f"\n{Fore.CYAN}[*] {Fore.WHITE}Not: Parantez içindeki kodlar ülke kodlarıdır.")
            
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Seçiminiz: {Fore.WHITE}")
                
                if choice == "0":
                    break
                elif choice in countries:
                    code, name = countries[choice]
                    print(f"\n{Fore.YELLOW}[*] {name} için {code} proxy aranıyor...")
                    self.find_country_proxy(code)
                    input(f"\n{Fore.YELLOW}[?] Devam etmek için Enter'a basın...")
                else:
                    print(f"\n{Fore.RED}[!] Geçersiz seçim!")
                    time.sleep(1)
                    
            except Exception as e:
                print(f"\n{Fore.RED}[!] Hata: {str(e)}")
                time.sleep(1)

    def find_country_proxy(self, country_code):
        print(f"{Fore.YELLOW}[*] {country_code} proxy'leri aranıyor...")
        self.proxies.clear()
        self.working_proxies.clear()
        self.target_region = country_code  # Hedef bölgeyi ayarla
        
        # Proxy arama optimizasyonları
        self.timeout = 3
        self.thread_count = min(100, (os.cpu_count() or 1) * 4)
        
        try:
            self.run()
            
            if self.working_proxies:
                filename = f"working_{country_code.lower()}_proxies.txt"
                self.save_proxies(filename, country_code)
                
        except Exception as e:
            print(f"\n{Fore.RED}[!] Hata: {str(e)}")
            return False
        finally:
            self.target_region = None

if __name__ == "__main__":
    finder = ProxyFinder()
    finder.menu()