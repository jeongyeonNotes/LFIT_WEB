#!/usr/bin/env bash
set -e

# 1) 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate

# 2) pip 업그레이드 & 의존성 설치
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3) .env 없으면 샘플 복사
[ -f ".env" ] || { [ -f ".env.example" ] && cp .env.example .env; }

# 4) DB 마이그레이션
python manage.py migrate

echo -e "\n✔ Setup finished. To run:  source .venv/bin/activate && python manage.py runserver"
