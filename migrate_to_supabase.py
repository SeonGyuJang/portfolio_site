#!/usr/bin/env python3
"""
Portfolio data + image migration script for Supabase.

Usage:
    python migrate_to_supabase.py              # migrate data + prompt about images
    python migrate_to_supabase.py --dry-run    # show what would happen, no writes
    python migrate_to_supabase.py --images     # only upload images to Supabase Storage
    python migrate_to_supabase.py --data       # only migrate data to Supabase DB
"""

import mimetypes
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import base64
import json

# ---------------------------------------------------------------------------
# Environment & CLI flags
# ---------------------------------------------------------------------------

load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("✗ Environment variables SUPABASE_URL and SUPABASE_KEY must be set.")
    print("  Add them to your .env file or export them in your shell.")
    sys.exit(1)

DRY_RUN: bool = "--dry-run" in sys.argv
MODE_IMAGES: bool = "--images" in sys.argv
MODE_DATA: bool = "--data" in sys.argv

# Default (no mode flags): run data migration then prompt about images.
RUN_DATA: bool = MODE_DATA or (not MODE_IMAGES and not MODE_DATA)
RUN_IMAGES: bool = MODE_IMAGES or (not MODE_IMAGES and not MODE_DATA)

from supabase import create_client  # noqa: E402  (import after env-check)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Base directory of this script (so it can be run from any cwd)
BASE_DIR = Path(__file__).parent.resolve()
BUCKET = "portfolio-images"

print(f"{'[DRY RUN] ' if DRY_RUN else ''}Connected to Supabase: {SUPABASE_URL[:50]}...")

# ---------------------------------------------------------------------------
# Migration data
# ---------------------------------------------------------------------------

CURRENT_ACTIVITIES = [
    {
        "title": "고려대학교 세종캠퍼스 재학",
        "description": "디지털경영전공",
        "date_start": "2023.03.01",
        "date_end": "",
        "is_ongoing": True,
        "sort_order": 1,
    },
    {
        "title": "Cactusun CTO",
        "description": "브랜드 창업 및 기술 총괄",
        "date_start": "2023.09.01",
        "date_end": "",
        "is_ongoing": True,
        "sort_order": 2,
    },
    {
        "title": "제38대 총학생회 '비범' 부총학생회장",
        "description": "고려대학교 세종캠퍼스",
        "date_start": "2025.12.06",
        "date_end": "",
        "is_ongoing": True,
        "sort_order": 3,
    },
    {
        "title": "One-Stop 서비스센터 근로장학생",
        "description": "고려대학교 세종캠퍼스",
        "date_start": "2024.03.12",
        "date_end": "",
        "is_ongoing": True,
        "sort_order": 4,
    },
]

PAST_ACTIVITIES = [
    {
        "title": "중앙동아리 AD-ZONE 2025-02 총무",
        "description": "",
        "date_start": "2025.07.01",
        "date_end": "2025.12.20",
        "sort_order": 1,
    },
    {
        "title": "제45대 총동아리연합회 '파란' 기획국 국장",
        "description": "",
        "date_start": "2025.01.01",
        "date_end": "2025.11.07",
        "sort_order": 2,
    },
    {
        "title": "중앙동아리 AD-ZONE 2025-01 부회장",
        "description": "",
        "date_start": "2025.01.01",
        "date_end": "2025.07.01",
        "sort_order": 3,
    },
    {
        "title": "(주)팜킷 AI Developer 인턴",
        "description": "기업부설연구소",
        "date_start": "2024.07.01",
        "date_end": "2024.12.20",
        "sort_order": 4,
    },
    {
        "title": "데이터분석 및 인공지능 학회 'PRISM' 1기 학회장",
        "description": "고려대학교 세종캠퍼스 크림슨브레인 소속",
        "date_start": "2024.03.27",
        "date_end": "2024.12.31",
        "sort_order": 5,
    },
    {
        "title": "중앙동아리 AD-ZONE 2024-02 기획 운영진",
        "description": "",
        "date_start": "2024.07.07",
        "date_end": "2024.12.31",
        "sort_order": 6,
    },
    {
        "title": "제44대 총동아리연합회 '동심' 홍보국 국원",
        "description": "",
        "date_start": "2024.03.22",
        "date_end": "2024.12.31",
        "sort_order": 7,
    },
    {
        "title": "서울 선사고등학교 졸업",
        "description": "",
        "date_start": "2020.03",
        "date_end": "2023.02",
        "sort_order": 8,
    },
    {
        "title": "대구 경북대학교 사범대학 부설중학교 졸업",
        "description": "",
        "date_start": "2017.03",
        "date_end": "2020.01",
        "sort_order": 9,
    },
]

TECH_STACKS = [
    # Coding
    {"category": "Coding", "category_icon": "💻", "name": "Python", "icon_class": "fab fa-python", "level": 95, "sort_order": 1},
    {"category": "Coding", "category_icon": "💻", "name": "SQL", "icon_class": "fas fa-database", "level": 80, "sort_order": 2},
    {"category": "Coding", "category_icon": "💻", "name": "Swift", "icon_class": "fab fa-swift", "level": 60, "sort_order": 3},
    {"category": "Coding", "category_icon": "💻", "name": "R", "icon_class": "fas fa-chart-bar", "level": 60, "sort_order": 4},
    # Data & Collaboration
    {"category": "Data & Collaboration", "category_icon": "📊", "name": "Notion", "icon_class": "fas fa-sticky-note", "level": 95, "sort_order": 5},
    {"category": "Data & Collaboration", "category_icon": "📊", "name": "Slack", "icon_class": "fab fa-slack", "level": 90, "sort_order": 6},
    {"category": "Data & Collaboration", "category_icon": "📊", "name": "Teams", "icon_class": "fas fa-users", "level": 80, "sort_order": 7},
    # Design & OA
    {"category": "Design & OA", "category_icon": "🎨", "name": "Figma", "icon_class": "fab fa-figma", "level": 80, "sort_order": 8},
    {"category": "Design & OA", "category_icon": "🎨", "name": "Miricanvas", "icon_class": "fas fa-palette", "level": 90, "sort_order": 9},
    {"category": "Design & OA", "category_icon": "🎨", "name": "MS Office", "icon_class": "fas fa-file-powerpoint", "level": 100, "sort_order": 10},
    # OS
    {"category": "OS", "category_icon": "⚙️", "name": "Windows", "icon_class": "fab fa-windows", "level": 100, "sort_order": 11},
    {"category": "OS", "category_icon": "⚙️", "name": "Linux", "icon_class": "fab fa-linux", "level": 80, "sort_order": 12},
    {"category": "OS", "category_icon": "⚙️", "name": "macOS", "icon_class": "fab fa-apple", "level": 100, "sort_order": 13},
]

PROJECTS = [
    {
        "title": "셔틀버스/식단표 트래킹 웹사이트",
        "description": "고려대학교 세종캠퍼스 학생들을 위한 실시간 셔틀버스 정보 제공 서비스",
        "icon_class": "fas fa-bus",
        "date_start": "2024.11",
        "date_end": "",
        "is_ongoing": True,
        "link": "https://kus-bus-app-feb0ef7b8941.herokuapp.com/",
        "sort_order": 1,
    },
    {
        "title": "제38대 총학생회 홈페이지",
        "description": "고려대학교 세종캠퍼스 총학생회 공식 웹사이트 개발 및 운영",
        "icon_class": "fas fa-users-cog",
        "date_start": "2025.12.20",
        "date_end": "",
        "is_ongoing": True,
        "link": "https://koreauniv-38th-website-869fb3bc771c.herokuapp.com/",
        "sort_order": 2,
    },
    {
        "title": "총동아리연합회 홈페이지",
        "description": "고려대학교 세종캠퍼스 총동아리연합회 공식 웹사이트 개발 및 운영",
        "icon_class": "fas fa-users-cog",
        "date_start": "2025.07.25",
        "date_end": "",
        "is_ongoing": True,
        "link": "https://kus-club-union.fly.dev/",
        "sort_order": 3,
    },
]

AWARDS = [
    {
        "name": "충청ICT ML/DL 과정 발표회 (은상)",
        "subject": "Computer Vision을 이용한 도로 상태 판단 AI",
        "award_result": "은상",
        "date_text": "2023.11.12",
        "organization": "",
        "description": "",
        "images": ["static/images/awards/ICT_3.jpg", "static/images/awards/ICT_2.png"],
        "icon_class": "fas fa-trophy",
        "sort_order": 1,
    },
    {
        "name": "충청ICT ML/DL 과정 발표회 (동상)",
        "subject": "Computer Vision을 이용한 CCTV 영상 분석",
        "award_result": "동상",
        "date_text": "2023.11.12",
        "organization": "",
        "description": "",
        "images": ["static/images/awards/ICT_3.jpg", "static/images/awards/ICT_1.png"],
        "icon_class": "fas fa-trophy",
        "sort_order": 2,
    },
    {
        "name": "창업경진대회 (고려대학교)",
        "subject": "JooInJang 캐릭터를 이용한 브랜딩 사업",
        "award_result": "우수상",
        "date_text": "2023.12.08",
        "organization": "",
        "description": "",
        "images": [
            "/static/images/awards/JooInJang_2.png",
            "/static/images/awards/JooInJang_5.jpg",
            "/static/images/awards/JooInJang_6.jpg",
            "/static/images/awards/JooInJang_1.jpg",
        ],
        "icon_class": "fas fa-trophy",
        "sort_order": 3,
    },
    {
        "name": "고려대학교 & 한국발명진흥회 연구 과제 수행",
        "subject": "수직농장 AI제어 시스템 적용 및 생육 이미지 데이터 활용",
        "award_result": "사업 진행",
        "date_text": "2023.08.16 ~ 2023.12.10",
        "organization": "한국발명진흥회",
        "description": "",
        "images": ["/static/images/awards/KIPA.png"],
        "icon_class": "fas fa-lightbulb",
        "sort_order": 4,
    },
    {
        "name": "DB 금융경제 공모전",
        "subject": "종합적 블록체인 이상거래 탐지방법 제언 ─ 암호화폐 거래의 사용자별 행동 패턴 분석 규칙을 기반으로",
        "award_result": "출품 완료",
        "date_text": "2024.02.28",
        "organization": "",
        "description": "",
        "images": ["/static/images/awards/DB_2.png", "/static/images/awards/DB_1.png"],
        "icon_class": "fas fa-award",
        "sort_order": 5,
    },
    {
        "name": "2024 T-SUM 데이터분석/인공지능 경진대회",
        "subject": "킥보드 주행 영상 분석을 통한 객체 탐지 인공지능 개발",
        "award_result": "대상 및 우수멘토상",
        "date_text": "2024.06.07",
        "organization": "",
        "description": "",
        "images": ["static/images/awards/TSUM.jpg"],
        "icon_class": "fas fa-trophy",
        "sort_order": 6,
    },
    {
        "name": "2024 KUS-TUDY",
        "subject": "파이썬을 활용한 Business Data Analytics",
        "award_result": "최우수상",
        "date_text": "2024.06.17",
        "organization": "",
        "description": "",
        "images": ["static/images/awards/KUSTUDY.png"],
        "icon_class": "fas fa-trophy",
        "sort_order": 7,
    },
    {
        "name": "2024 산학협력친화형PBL 수강 후기 공모전",
        "subject": "데이터분석과 인공지능을 통해 선한 영향력 끼치는 개발자에 다가가다",
        "award_result": "은상",
        "date_text": "2024.07.05",
        "organization": "",
        "description": "",
        "images": ["static/images/awards/PBL.jpeg"],
        "icon_class": "fas fa-trophy",
        "sort_order": 8,
    },
    {
        "name": "2024 세종시 기업분석 경진대회",
        "subject": "주식회사 서북에 대한 분석",
        "award_result": "최우수상",
        "date_text": "2024.10.08",
        "organization": "세종시",
        "description": "",
        "images": [
            "static/images/awards/SEJONG_C.jpeg",
            "static/images/awards/SEJONG_A.jpeg",
            "static/images/awards/SEJONG_B.png",
        ],
        "icon_class": "fas fa-trophy",
        "sort_order": 9,
    },
    {
        "name": "2024 R&SD 성과공유회",
        "subject": "(주)팜킷 - 이커머스 전력과 테크놀로지, TableOCR 연계 식품 챗봇 프로세스 개발",
        "award_result": "우수상",
        "date_text": "2024.10.25",
        "organization": "",
        "description": "",
        "images": [],
        "icon_class": "fas fa-trophy",
        "sort_order": 10,
    },
    {
        "name": "2024 기업기술혁신PBL",
        "subject": "(주)팜킷 - 이커머스 전력과 테크놀로지, TableOCR 연계 식품 챗봇 프로세스 개발",
        "award_result": "우수상",
        "date_text": "2024.12.20",
        "organization": "",
        "description": "",
        "images": [],
        "icon_class": "fas fa-trophy",
        "sort_order": 11,
    },
    {
        "name": "2025 하계 한국데이터마이닝학회",
        "subject": "Controlling Informational Freedom in Large Language Models via Degree of Freedom Prompting",
        "award_result": "최우수논문상",
        "date_text": "2025.08.28",
        "organization": "한국데이터마이닝학회",
        "description": "",
        "images": ["static/images/awards/DATA.png"],
        "icon_class": "fas fa-star",
        "sort_order": 12,
    },
]

ACADEMIC_ITEMS = [
    {
        "name": "고려대학교(세종) 크림슨브레인소속 데이터분석 및 인공지능학회 'PRISM' 1기 학회장",
        "description": "데이터분석 및 인공지능 학회에서 1기 학회장으로 활동하며 학회원들과 함께 다양한 프로젝트 및 스터디를 진행했습니다.",
        "date_text": "2024.03 ~ 2024.12",
        "paper_link": "",
        "images": ["static/images/academic/DOF/PRISM.jpeg"],
        "sort_order": 1,
    },
    {
        "name": "2023 한국IT서비스학회 춘계학술대회 참여 및 교육이수",
        "description": "한국IT서비스학회 춘계학술대회에 참여하여 IT 서비스 분야의 최신 연구 동향을 학습하였습니다.",
        "date_text": "2023.05.24",
        "paper_link": "",
        "images": ["static/images/academic/DOF/IT_service.png"],
        "sort_order": 2,
    },
    {
        "name": "2024 한국데이터마이닝학회 춘계학술대회 참여",
        "description": "한국데이터마이닝학회 춘계학술대회에 참여하여 데이터마이닝 및 AI 분야의 최신 연구를 접하였습니다.",
        "date_text": "2024.05.30",
        "paper_link": "",
        "images": ["static/images/academic/DOF/KDMS2024_C.png"],
        "sort_order": 3,
    },
    {
        "name": "2024 한국데이터마이닝학회 추계학술대회 참여",
        "description": "한국데이터마이닝학회 추계학술대회에 참여하여 데이터마이닝 및 AI 분야의 연구 발표를 청강하였습니다.",
        "date_text": "2024.11.22 ~ 2024.11.23",
        "paper_link": "",
        "images": ["static/images/academic/DOF/KDMS2024_CC.png"],
        "sort_order": 4,
    },
    {
        "name": "2025 한국데이터마이닝학회 하계학술대회 참여 및 발표",
        "description": "한국데이터마이닝학회 하계학술대회에 참여하여 최신 데이터마이닝 연구 및 AI 분야를 학습하고, 포스터발표를 진행하였습니다.",
        "date_text": "2025.08.28 ~ 2025.08.30",
        "paper_link": "",
        "images": ["static/images/academic/DOF/KDMS2025_CC.png"],
        "sort_order": 5,
    },
    {
        "name": "Moral Alignment in Large Language Models : Effects of Linguistic Framing and Domain Personas",
        "description": "KDMS2025 포스터 발표 - 대규모 언어 모델에서의 도덕적 정렬에 대한 언어적 프레이밍과 도메인 페르소나의 영향을 연구하였습니다.",
        "date_text": "2025.08.29",
        "paper_link": "",
        "images": ["static/images/academic/DOF/MORAL.png"],
        "sort_order": 6,
    },
    {
        "name": "Controlling Informational Freedom in Large Language Models via Degree of Freedom Prompting",
        "description": "KDMS2025 포스터 발표 - 자유도 프롬프팅을 통해 대규모 언어 모델의 정보 자유도를 제어하는 방법론을 제시하였습니다.",
        "date_text": "2025.08.29",
        "paper_link": "",
        "images": ["static/images/academic/DOF/DOF.png"],
        "sort_order": 7,
    },
    {
        "name": "Cross-Linguistic Moral Preferences in Large Language Models: Evidence from Distributive Justice Scenarios and Domain Persona Interventions",
        "description": "MDPI Electronics 게재 논문 - 대규모 언어 모델에서의 언어 간 도덕적 선호도에 대한 분배 정의 시나리오 및 도메인 페르소나 개입 연구를 진행하였습니다.",
        "date_text": "2025.12.11",
        "paper_link": "",
        "images": ["static/images/academic/DOF/MDPI-2.png", "static/images/academic/DOF/MDPI-1.png"],
        "sort_order": 8,
    },
]

CERTIFICATES = [
    {
        "name": "ADsP (데이터분석준전문가)",
        "issuer": "한국데이터산업진흥원",
        "date_text": "2023.09.08",
        "image": "/static/images/awards/ADsP.png",
        "sort_order": 1,
    },
    {
        "name": "SQLD (SQL개발자)",
        "issuer": "한국데이터산업진흥원",
        "date_text": "2024.03.29",
        "image": "/static/images/awards/SQLD.png",
        "sort_order": 2,
    },
]

TABLES = {
    "current_activities": CURRENT_ACTIVITIES,
    "past_activities": PAST_ACTIVITIES,
    "tech_stacks": TECH_STACKS,
    "projects": PROJECTS,
    "awards": AWARDS,
    "academic_items": ACADEMIC_ITEMS,
    "certificates": CERTIFICATES,
}

# ---------------------------------------------------------------------------
# Image upload configuration
#
# Each entry describes one source directory and the flat prefix to apply.
# Certificate images live in the awards/ directory but get the ct_ prefix.
# ---------------------------------------------------------------------------

# Files in awards/ that are certificates (get ct_ prefix instead of aw_)
CERTIFICATE_FILENAMES = {"ADsP.png", "SQLD.png"}

IMAGE_SOURCES = [
    {
        "dir": BASE_DIR / "static" / "images" / "awards",
        "prefix": "aw_",
        # certificate files inside this dir are handled separately
    },
    {
        "dir": BASE_DIR / "static" / "images" / "academic" / "DOF",
        "prefix": "ac_",
    },
    {
        "dir": BASE_DIR / "static" / "images" / "Paper_1",
        "prefix": "pp_",
        "space_to_underscore": True,
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def public_url(filename: str) -> str:
    """Construct a Supabase Storage public URL for a flat-named file."""
    base = SUPABASE_URL.rstrip("/")
    return f"{base}/storage/v1/object/public/{BUCKET}/{filename}"


def flat_name(prefix: str, original_filename: str, space_to_underscore: bool = False) -> str:
    """Return the flat storage filename for an image."""
    name = original_filename
    if space_to_underscore:
        name = name.replace(" ", "_")
    return f"{prefix}{name}"


def award_path_to_flat(path: str) -> str | None:
    """
    Convert a local award image path such as
      'static/images/awards/ICT_3.jpg'  or
      '/static/images/awards/ICT_3.jpg'
    to its flat storage filename.  Returns None if the path is not
    recognised as an awards image.
    """
    norm = path.lstrip("/")
    prefix_dir = "static/images/awards/"
    if not norm.startswith(prefix_dir):
        return None
    filename = norm[len(prefix_dir):]
    if filename in CERTIFICATE_FILENAMES:
        return flat_name("ct_", filename)
    return flat_name("aw_", filename)


def academic_path_to_flat(path: str) -> str | None:
    """
    Convert a local academic image path such as
      'static/images/academic/DOF/PRISM.jpeg'
    to its flat storage filename.  Returns None if not recognised.
    """
    norm = path.lstrip("/")
    prefix_dir = "static/images/academic/DOF/"
    if not norm.startswith(prefix_dir):
        return None
    filename = norm[len(prefix_dir):]
    return flat_name("ac_", filename)


def certificate_path_to_flat(path: str) -> str | None:
    """
    Convert a local certificate image path such as
      '/static/images/awards/ADsP.png'
    to its flat ct_ storage filename.  Returns None if not recognised.
    """
    norm = path.lstrip("/")
    prefix_dir = "static/images/awards/"
    if not norm.startswith(prefix_dir):
        return None
    filename = norm[len(prefix_dir):]
    if filename not in CERTIFICATE_FILENAMES:
        return None
    return flat_name("ct_", filename)


# ---------------------------------------------------------------------------
# Data migration
# ---------------------------------------------------------------------------


def migrate_table(table_name: str, rows: list[dict]) -> None:
    print(f"\n{'─' * 55}")
    print(f"  Table: {table_name}  ({len(rows)} rows)")

    if DRY_RUN:
        for i, row in enumerate(rows, 1):
            label = row.get("title") or row.get("name") or "(no label)"
            print(f"    [{i}] {label}")
        print("  --> DRY RUN: no writes performed")
        return

    # Check for existing data and prompt before overwriting.
    try:
        existing = supabase.table(table_name).select("id").execute()
        if existing.data:
            answer = input(
                f"  ⚠  Table already has {len(existing.data)} row(s). "
                "Delete all and re-insert? [y/N]: "
            ).strip().lower()
            if answer != "y":
                print("  --> Skipped")
                return
            supabase.table(table_name).delete().neq(
                "id", "00000000-0000-0000-0000-000000000000"
            ).execute()
            print(f"  Deleted {len(existing.data)} existing row(s).")
    except Exception as exc:
        print(f"  ⚠  Could not check existing data: {exc}")

    ok = fail = 0
    for row in rows:
        label = row.get("title") or row.get("name") or "?"
        try:
            supabase.table(table_name).insert(row).execute()
            print(f"  ✓ {label}")
            ok += 1
        except Exception as exc:
            print(f"  ✗ {label} --> {exc}")
            fail += 1

    print(f"  Done: {ok} inserted, {fail} failed.")


def run_data_migration() -> None:
    print("\n" + "=" * 55)
    print("  Phase 1: Data migration --> Supabase DB")
    if DRY_RUN:
        print("  Mode: DRY RUN (no writes)")
    print("=" * 55)

    for table_name, rows in TABLES.items():
        migrate_table(table_name, rows)

    # 이미지 마이그레이션
    if TARGET_TABLE is None or TARGET_TABLE in ['awards', 'academic_items']:
        migrate_images()

    print(f"\n{'='*50}")
    print("  마이그레이션 완료!")
    print("  이제 포트폴리오 사이트에서 데이터를 확인하세요.")
    print("=" * 50)


def migrate_images():
    """Migrate images from static/images to database."""
    print(f"\n{'─'*50}")
    print(f"🖼  이미지 마이그레이션")
    
    if DRY_RUN:
        print("  → DRY RUN: 실제 저장 안 함")
        return
    
    base_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
    if not os.path.exists(base_dir):
        print(f"  ⚠️  이미지 폴더 없음: {base_dir}")
        return
    
    # 수집할 이미지들
    image_map = {}  # {file_path: image_id}
    image_count = 0
    
    # AWARDS에서 이미지 수집
    for award in AWARDS:
        if isinstance(award.get('images'), list):
            image_ids = []
            for img_path in award['images']:
                # 경로 정규화
                img_path = img_path.lstrip('/')
                if img_path.startswith('static/images/'):
                    img_path = img_path[len('static/images/'):]
                
                full_path = os.path.join(base_dir, img_path)
                
                if os.path.exists(full_path):
                    img_id = upload_image_to_db(full_path, 'awards', img_path)
                    if img_id:
                        image_ids.append(img_id)
                        image_count += 1
                        print(f"  ✓ {img_path}")
                else:
                    print(f"  ✗ 파일 없음: {img_path}")
            
            award['images'] = image_ids
    
    # ACADEMIC_ITEMS에서 이미지 수집
    for item in ACADEMIC_ITEMS:
        if isinstance(item.get('images'), list):
            image_ids = []
            for img_path in item['images']:
                # 경로 정규화
                img_path = img_path.lstrip('/')
                if img_path.startswith('static/images/'):
                    img_path = img_path[len('static/images/'):]
                
                full_path = os.path.join(base_dir, img_path)
                
                if os.path.exists(full_path):
                    img_id = upload_image_to_db(full_path, 'academic_items', img_path)
                    if img_id:
                        image_ids.append(img_id)
                        image_count += 1
                        print(f"  ✓ {img_path}")
                else:
                    print(f"  ✗ 파일 없음: {img_path}")
            
            item['images'] = image_ids
    
    print(f"  완료: {image_count}개 이미지 업로드")


def upload_image_to_db(file_path, item_type, relative_path):
    """Upload image to database and return image ID."""
    try:
        with open(file_path, 'rb') as f:
            image_data = f.read()
        
        # MIME 타입 결정
        ext = os.path.splitext(file_path)[1].lower()
        mime_map = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png', '.gif': 'image/gif',
            '.webp': 'image/webp', '.svg': 'image/svg+xml'
        }
        mime_type = mime_map.get(ext, 'image/jpeg')
        
        # Base64 인코딩 (JSON 직렬화 가능)
        image_data_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # 데이터베이스에 저장
        result = supabase.table('portfolio_images').insert({
            'filename': relative_path,
            'mime_type': mime_type,
            'image_data': image_data_b64,
            'item_type': item_type
        }).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]['id']
        return None
    except Exception as e:
        print(f"    오류: {e}")
        return None


if __name__ == "__main__":
    main()
