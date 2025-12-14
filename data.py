# Portfolio Data Management
# 모든 데이터를 중앙 집중식으로 관리하여 코드의 유기성을 높입니다.

# 이모지 및 아이콘 매핑
icons = {
    'Python': 'fab fa-python',
    'SQL': 'fas fa-database',
    'Swift': 'fab fa-swift',
    'R': 'fas fa-chart-bar',
    'HTML/CSS': 'fab fa-html5',
    'JS': 'fab fa-js',
    'Word': 'fas fa-file-word',
    'Excel': 'fas fa-file-excel',
    'PowerPoint': 'fas fa-file-powerpoint',
    'Notion': 'fas fa-sticky-note',
    'Slack': 'fab fa-slack',
    'Teams': 'fas fa-users',
    'Figma': 'fab fa-figma',
    'Miricanvas': 'fas fa-palette',
    'Windows': 'fab fa-windows',
    'Linux': 'fab fa-linux',
    'macOS': 'fab fa-apple'
}

portfolio_data = {
    'site_title': '장선규 | Portfolio',

    # Hero Section
    'hero': {
        'status_badge': '"Promising interdisciplinary talent',
        'greeting': '안녕하세요,',
        'title': '저는 장선규입니다.',
        'typing_prefix': "I'm a ",
        'typing_texts': ['Digital Business Major', 'AI Developer', 'Data Researcher', 'Tech Strategist'],
        'subtitle': '성장과 도전을 멈추지 않으며, 선한 영향력을 주는',
        'subtitle_strong': '인공지능 연구자',
        'stats': [
            {'number': 15, 'label': 'Projects'},
            {'number': 6, 'label': 'Awards'},
            {'number': 10, 'label': 'Activities'}
        ],
        'tech_icons': [
            {'icon': 'fab fa-python', 'title': 'Python'},
            {'icon': 'fas fa-database', 'title': 'SQL'},
            {'icon': 'fab fa-swift', 'title': 'Swift'},
            {'icon': 'fas fa-chart-line', 'title': 'Data Analysis'},
            {'icon': 'fas fa-brain', 'title': 'AI/ML'}
        ]
    },

    # About Me Section
    'about': {
        'profile_image': '/static/images/profile.jpg',
        'profile_alt': '장선규 프로필 사진',
        'current_position': {
            'badge_icon': 'fas fa-briefcase',
            'badge_text': 'Current Position',
            'icon': 'fas fa-graduation-cap',
            'title': '부총학생회장',
            'organization': '고려대학교 세종캠퍼스 제38대 총학생회 \'비범\'',
            'period': '2025.12 ~ 현재'
        },
        'info': [
            {
                'icon': 'far fa-calendar-alt',
                'label': 'Birth Date',
                'value': '2004.06.16',
                'link': None
            },
            {
                'icon': 'fas fa-envelope',
                'label': 'Email',
                'value': 'dsng3419@korea.ac.kr',
                'link': 'mailto:dsng3419@korea.ac.kr'
            },
            {
                'icon': 'fab fa-github',
                'label': 'Github',
                'value': 'SeonGyuJang',
                'link': 'https://github.com/SeonGyuJang'
            },
            {
                'icon': 'fab fa-kaggle',
                'label': 'Kaggle',
                'value': 'seongyujang04',
                'link': 'https://www.kaggle.com/seongyujang04'
            },
            {
                'icon': 'fas fa-blog',
                'label': 'Blog',
                'value': 'Naver Blog',
                'link': 'https://blog.naver.com/ergosphere29'
            },
            {
                'icon': 'fab fa-instagram',
                'label': 'Instagram',
                'value': '@ditdah_ditdit_0616',
                'link': 'https://www.instagram.com/ditdah_ditdit_0616'
            }
        ]
    },

    # Experience & Education
    'history': {
        'current': [
            {
                'date': '2023.03.01 ~ ing',
                'title': '고려대학교 세종캠퍼스 재학',
                'desc': '디지털경영전공'
            },
            {
                'date': '2023.09.01 ~ ing',
                'title': 'Cactusun CTO',
                'desc': '브랜드 창업 및 기술 총괄'
            },
            {
                'date': '2025.12.06 ~ ing',
                'title': '제38대 총학생회 \'비범\' 부총학생회장',
                'desc': '고려대학교 세종캠퍼스'
            },
            {
                'date': '2025.07.01 ~ ing',
                'title': '중앙동아리 AD-ZONE 2025-02 총무',
                'desc': '고려대학교 세종캠퍼스'
            },
            {
                'date': '2024.03.12 ~ ing',
                'title': 'One-Stop 서비스센터 근로장학생',
                'desc': '고려대학교 세종캠퍼스'
            }
        ],
        'past': [
            {
                'date': '2025.01.01 ~ 2025.11.07',
                'title': '제45대 총동아리연합회 \'파란\' 기획국 국장',
                'desc': None
            },
            {
                'date': '2025.01.01 ~ 2025.07.01',
                'title': '중앙동아리 AD-ZONE 2025-01 부회장',
                'desc': None
            },
            {
                'date': '2024.07.01 ~ 2024.12.20',
                'title': '(주)팜킷 AI Developer 인턴',
                'desc': '기업부설연구소'
            },
            {
                'date': '2024.03.27 ~ 2024.12.31',
                'title': '데이터분석 및 인공지능 학회 \'PRISM\' 1기 학회장',
                'desc': '고려대학교 세종캠퍼스 크림슨브레인 소속'
            },
            {
                'date': '2024.07.07 ~ 2024.12.31',
                'title': '중앙동아리 AD-ZONE 2024-02 기획 운영진',
                'desc': None
            },
            {
                'date': '2024.03.22 ~ 2024.12.31',
                'title': '제44대 총동아리연합회 \'동심\' 홍보국 국원',
                'desc': None
            },
            {
                'date': '2020.03 ~ 2023.02',
                'title': '서울 선사고등학교 졸업',
                'desc': None
            },
            {
                'date': '2017.03 ~ 2020.01',
                'title': '대구 경북대학교 사범대학 부설중학교 졸업',
                'desc': None
            }
        ]
    },

    # Skills (using remote values which may be more up to date)
    'skills': {
        'Coding': [
            {'name': 'Python', 'level': 100, 'icon': icons['Python']},
            {'name': 'SQL', 'level': 70, 'icon': icons['SQL']},
            {'name': 'Swift', 'level': 65, 'icon': icons['Swift']},
            {'name': 'R', 'level': 60, 'icon': icons['R']}
        ],
        'OA': [
            {'name': 'Excel', 'level': 90, 'icon': icons['Excel']},
            {'name': 'PowerPoint', 'level': 90, 'icon': icons['PowerPoint']},
            {'name': 'Word', 'level': 100, 'icon': icons['Word']}
        ],
        'Collaboration': [
            {'name': 'Notion', 'level': 100, 'icon': icons['Notion']},
            {'name': 'Slack', 'level': 80, 'icon': icons['Slack']},
            {'name': 'Teams', 'level': 100, 'icon': icons['Teams']}
        ],
        'Design & OS': [
            {'name': 'Figma', 'level': 70, 'icon': icons['Figma']},
            {'name': 'macOS', 'level': 100, 'icon': icons['macOS']},
            {'name': 'Linux', 'level': 80, 'icon': icons['Linux']}
        ]
    },

    # Projects
    'projects': [
        {
            'title': '셔틀버스/식단표 트래킹 웹사이트',
            'desc': '고려대학교 세종캠퍼스 학생들을 위한 실시간 정보 제공 서비스',
            'period': '2024.11 ~ ing',
            'url': 'https://kus-bus-app-feb0ef7b8941.herokuapp.com/',
            'icon': 'fas fa-bus'
        },
        {
            'title': '총동아리연합회 홈페이지',
            'desc': '고려대학교 세종캠퍼스 총동아리연합회 공식 웹사이트 개발 및 운영',
            'period': '2025.07.25 ~ ing',
            'url': 'https://kus-club-union.fly.dev/',
            'icon': 'fas fa-users-cog'
        }
    ],

    # Awards
    'awards': [
        {'name': '충청ICT ML/DL 과정 발표회', 'icon': 'fas fa-trophy'},
        {'name': '창업경진대회 (고려대, 세종)', 'icon': 'fas fa-trophy'},
        {'name': 'DB 금융경제 공모전', 'icon': 'fas fa-award'},
        {'name': '2024 T-SUM 데이터분석/AI 경진대회', 'icon': 'fas fa-trophy'},
        {'name': '2024 세종시 기업분석 경진대회', 'icon': 'fas fa-trophy'},
        {'name': '2025 하계 한국데이마이닝학회', 'icon': 'fas fa-star'},
    ],

    # Academic & Certifications
    'academic': {
        'papers': [
            {
                'date': '2024.03 ~ 12',
                'title': '고려대 세종 PRISM 학회 활동 (1기 학회장)',
                'link': '#'
            },
            {
                'date': 'YYYY.MM.DD',
                'title': '(논문 제목을 입력하세요)',
                'link': '#'
            }
        ],
        'certifications': [
            {
                'date': 'YYYY.MM.DD',
                'name': '(자격증 명을 입력하세요)',
                'issuer': '(발행기관)'
            },
            {
                'date': 'YYYY.MM.DD',
                'name': '(자격증 명을 입력하세요)',
                'issuer': '(발행기관)'
            }
        ]
    },

    # Activity Log (Gallery)
    'gallery': {
        'filters': ['all', 'paper', 'study', 'school', 'reading'],
        'items': [
            {
                'category': 'school',
                'icon': 'fas fa-university fa-2x',
                'cat_label': '학교',
                'title': '총학생회 선거 활동',
                'date': '2025.11'
            },
            {
                'category': 'study',
                'icon': 'fas fa-code fa-2x',
                'cat_label': '개인공부',
                'title': 'Swift 노치 프로그램 개발',
                'date': '2025.12'
            },
            {
                'category': 'paper',
                'icon': 'fas fa-file-alt fa-2x',
                'cat_label': '논문',
                'title': 'AI 윤리 연구 (AIPEDA)',
                'date': '2025.11'
            },
            {
                'category': 'reading',
                'icon': 'fas fa-book fa-2x',
                'cat_label': '독서',
                'title': '개발 관련 서적 독서',
                'date': 'ongoing'
            }
        ]
    }
}
