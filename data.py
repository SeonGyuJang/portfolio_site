# 이모지 및 아이콘 매핑
icons = {
    'Python': 'fab fa-python', 'SQL': 'fas fa-database', 'Swift': 'fab fa-swift', 'R': 'fas fa-chart-bar',
    'HTML/CSS': 'fab fa-html5', 'JS': 'fab fa-js',
    'Word': 'fas fa-file-word', 'Excel': 'fas fa-file-excel', 'PowerPoint': 'fas fa-file-powerpoint',
    'Notion': 'fas fa-sticky-note', 'Slack': 'fab fa-slack', 'Teams': 'fas fa-users',
    'Figma': 'fab fa-figma', 'Miricanvas': 'fas fa-palette',
    'Windows': 'fab fa-windows', 'Linux': 'fab fa-linux', 'macOS': 'fab fa-apple'
}

portfolio_data = {
    'site_title': '장선규 | Portfolio',
    'hero': {
        'title': '안녕하세요, 장선규입니다.',
        'typing_text': ['Data Researcher', 'Project Manager', 'Student Leader', 'Challenge Seeker'], # 타이핑 효과 텍스트
        'subtitle': '성장과 도전을 멈추지 않으며, 선한 영향력을 주는 연구자가 되는 것이 목표입니다.'
    },
    'about': {
        'birth': '2004.06.16',
        'email': 'dsng3419@korea.ac.kr',
        'socials': [
            {'name': 'Github', 'url': 'https://github.com/SeonGyuJang', 'icon': 'fab fa-github'},
            {'name': 'Kaggle', 'url': 'https://www.kaggle.com/seongyujang04', 'icon': 'fab fa-kaggle'},
            {'name': 'Blog', 'url': 'https://blog.naver.com/ergosphere29', 'icon': 'fas fa-blog'},
            {'name': 'Instagram', 'url': 'https://www.instagram.com/ditdah_ditdit_0616', 'icon': 'fab fa-instagram'}
        ],
        # [요청사항 반영] 최근 핵심 직책 하이라이트
        'highlights': [
            '고려대학교 세종캠퍼스 디지털경영전공 재학',
            '제38대 총학생회 ‘비범’ 부총학생회장',
            'Cactusun CTO (브랜드 창업)',
            '전) (주)팜킷 AI Developer 인턴'
        ]
    },
    # 스킬 데이터와 숙련도 (0~100%)
    'skills': {
        'Coding': [
            {'name': 'Python', 'level': 90, 'icon': icons['Python']},
            {'name': 'SQL', 'level': 85, 'icon': icons['SQL']},
            {'name': 'Swift', 'level': 70, 'icon': icons['Swift']},
            {'name': 'R', 'level': 75, 'icon': icons['R']},
        ],
        'OA': [
            {'name': 'Excel', 'level': 95, 'icon': icons['Excel']},
            {'name': 'PowerPoint', 'level': 95, 'icon': icons['PowerPoint']},
            {'name': 'Word', 'level': 90, 'icon': icons['Word']},
        ],
        'Collaboration': [
            {'name': 'Notion', 'level': 95, 'icon': icons['Notion']},
            {'name': 'Slack', 'level': 90, 'icon': icons['Slack']},
            {'name': 'Teams', 'level': 85, 'icon': icons['Teams']},
        ],
        'Design & OS': [
            {'name': 'Figma', 'level': 80, 'icon': icons['Figma']},
            {'name': 'macOS', 'level': 95, 'icon': icons['macOS']},
            {'name': 'Linux', 'level': 70, 'icon': icons['Linux']},
        ]
    },
    # 현재 진행중인 프로젝트
    'current_projects': [
        {
            'title': '셔틀버스/식단표 트래킹 웹사이트',
            'desc': '고려대 세종캠퍼스 학생을 위한 실시간 정보 제공',
            'period': '2024.11 ~ ing',
            'url': 'https://www.kus-bus.site/',
            'icon': 'fas fa-bus'
        },
        {
            'title': '총동아리연합회 홈페이지',
            'desc': '동아리 정보 통합 관리 및 홍보 플랫폼',
            'period': '2025.07 ~ ing',
            'url': 'https://kus-club-union.fly.dev/',
            'icon': 'fas fa-users'
        }
    ],
    # 활동 연혁 (Recent -> Past 순서 권장)
    'history': [
        {'date': '2025.12 ~ ing', 'title': '제38대 총학생회 ‘비범’ 부총학생회장', 'desc': '고려대학교 세종캠퍼스'},
        {'date': '2023.09 ~ ing', 'title': 'Cactusun CTO', 'desc': '브랜드 창업 및 기술 총괄'},
        {'date': '2024.07 ~ 2024.12', 'title': '(주)팜킷 AI Developer 인턴', 'desc': '기업부설연구소 근무'},
        # ... (나머지 내용도 여기에 추가하면 됨)
    ],
     'awards': [
        '충청ICT ML/DL 과정 발표회', '창업경진대회 (고려대, 세종)', 'DB 금융경제 공모전',
        '2024 T-SUM 데이터분석/AI 경진대회', '2024 세종시 기업분석 경진대회'
    ]
}