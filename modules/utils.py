import os
import ctypes

class Counter:
    Registered = 0
    Failed = 0
    PromosFetched = 0

def get_formatted_proxy(proxy: str) -> dict:

    try:
        if '@' in proxy or len(proxy.split(':')) == 2:
            formatted_proxy = proxy

        else:
            parts = proxy.split(':')

            if '.' in parts[0]:
                formatted_proxy = ':'.join(parts[2:]) + '@' + ':'.join(parts[:2])

            else:
                formatted_proxy = ':'.join(parts[:2]) + '@' + ':'.join(parts[2:])
        
        return {
            'http': f'http://{formatted_proxy}',
            'https': f'http://{formatted_proxy}'
        }
    
    except:
        return None


def title_set_loop():

    if os.name == "nt":
        while True:
            ctypes.windll.kernel32.SetConsoleTitleW(f"Chess.com Promo Generator (@zadowchi_afw) | Registered: {Counter.Registered} | Failed: {Counter.Failed} | Promos Fetched: {Counter.PromosFetched}")