import json

import requests

BASE_URL = 'https://robotax.io/api/v1/'


def main():
    with open('token.txt') as f:
        token = f.read()

    session = requests.session()
    session.headers.update({'Authorization': f'Token {token}'})

    with open('법인세_records.json') as f:
        records = json.load(f)

    res = session.post(f'{BASE_URL}ntsreportformat/', json={
        'report_type': '법인세신고서식',
        'password': '12345678',  # 생략시 기본값: 12345678
        'date': '2021-01-01',  # 신고서 서식 기준일시
        'records': records})

    with open('output', 'wb') as out:
        out.write(res.content)


if __name__ == '__main__':
    main()
