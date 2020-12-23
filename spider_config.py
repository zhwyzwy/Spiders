import time
from fake_useragent import UserAgent

HEADERS = {"User-Agent": UserAgent().random}


TOUTIAO_COOKIE = {'Cookie': 'tt_webid=6905955543991584264; ttcid=58be55c31b34434896760736ad3f201831; s_v_web_id=verify_kio0wvcn_AggiIFZM_U3GK_4fyk_AVb3_R8XMb2Q3x18F; tt_webid=6905955543991584264; __tasessionId=76d04h5r91607918088554; csrftoken=a422a89dbbacb86c8625e005812408a6; __ac_nonce=05fd6e2140014d6fe4e77; __ac_signature=_02B4Z6wo00f01fhHnLQAAIBB.vVwNDbWprH4Q5gAACHJSAj98uZhDf82gYrtU5wf.Vx37Ngma-Fl.YEOhYWsYUB2Wsmoj4RKf9KF97hgaZawnUvt6dIPnpYxYSxvjx3h3az0Q-sBXu2Gfdxwd6; MONITOR_WEB_ID=bd44b1f0-c6bf-461f-9d1f-4b0b8492e493; tt_scid=nEGPuxU8x51Y6zoYupSz.CDp5Ii0B6bnjndpOCKK.8gEn4PRylEPVmPJvxatHJGA402d'}
TOUTIAO_PARAMS = {
    'aid': '24',
    'app_name': 'web_search',
    'offset': 40,
    'origined': '',
    'autoload': 'true',
    'count': 20,
    'en_qc': 1,
    'cur_tab': 1,
    'from': 'search_tab',
    'pd': 'synthesis',
    'timestamp': int(time.time())

}


ZHIHU_COOKIE = '"ACBaJW67SBKPTi2AhkI6gtBmYuAgbBm-Kzk=|1606898617"'