import json

import requests

BASE_URL = 'https://robotax.io/api/v1/'


def main():
    with open('token.txt') as f:
        token = f.read()

    session = requests.session()
    session.headers.update({'Authorization': f'Token {token}'})
    organizations = session.get(f'{BASE_URL}organization/').json()['results']
    print(organizations[0])

    res = session.post(f'{BASE_URL}사업자/', json={
        '법인명_상호': '주식회사 테스트',
        '대표자주민등록번호': 'xxxx',
        '납세자ID': '1293300000', # 사업자번호 (개인은 주민등록번호)
        '홈택스ID': 'test', # 홈택스 계정. 전자신고파일을 업로드하는 계정과 일치해야 함
        '사업장소재지': '경기도 성남시 백현로 97',
        '사업장전화번호': '01012345678',
        '성명_대표자명': '홍길동',
        '개업일': '2017-12-22',
        '업종코드_list': ['722005']
    })
    print(res.status_code)
    사업자 = res.json()
    print(사업자['법인명_상호'])

    with open('전표.json') as f:
        session.post(f'{BASE_URL}전표/', json=[dict(data, 사업자=사업자['id']) for data in json.load(f)])

    종합소득세 = session.post(f'{BASE_URL}종합소득세/', json=dict(
        사업자=사업자['id'],
        신고구분상세코드='01',
        민원종류코드='FA001',
        과세기간_년월=f'201901',
        신고유형코드='32',  # 추계-단순율
    )).json()
    print(종합소득세)

    session.delete(f'{BASE_URL}사업자/{사업자["id"]}/')


if __name__ == '__main__':
    main()

