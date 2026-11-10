"""
Long-form "details" text (KR, EN) shown when a visitor clicks an item.
Taken from the LinkedIn profile and CVs. Merged into content_seed.SEED.

Format (also usable in the admin):
  plain line      → paragraph
  - item          → bullet
  [Heading]       → sub-heading
"""

DETAILS = {
    # ── projects (key: KR title) ───────────────────────────────────────────
    'projects': {
        "제38대 총학생회 공식 웹 플랫폼": (
            "고려대학교 세종캠퍼스 제38대 총학생회 공식 웹사이트를 직접 개발·운영하고 있습니다. 학생 편의 향상, "
            "투명한 학생자치, 행정 업무 효율화를 목표로 자체 CMS 기반 플랫폼을 설계했습니다.\n"
            "[주요 기능]\n"
            "- 캠퍼스 생활 편의: 셔틀버스 실시간 트래커, 학식 메뉴, 학사 일정, 교내 프로그램 안내 등 필요한 정보를 한곳에서 제공\n"
            "- 투명한 학생자치: 조직도, 공약, 회의록, 회칙, 아카이브, 문의 시스템 모듈로 운영의 투명성과 소통 강화\n"
            "- 시설 예약 시스템: 학생회관 회의실을 손쉽게 예약할 수 있는 자동 예약 시스템 구현\n"
            "- 관리자 대시보드(CMS): 총학생회 구성원이 직접 콘텐츠를 관리해 모든 정보를 최신 상태로 유지\n"
            "- KUS-BUS 통합: 기존 셔틀버스·학식 서비스(2024–2026)를 플랫폼으로 흡수",
            "Developed and operate the official website of the 38th Student Council at Korea University Sejong "
            "Campus. The platform is designed to enhance student convenience, ensure transparent governance, and "
            "streamline administrative work through a custom-built content management system.\n"
            "[Key Features]\n"
            "- Campus Life & Convenience: real-time shuttle bus tracker, cafeteria menus, academic schedules and "
            "campus program listings in one place\n"
            "- Transparent Governance: modules for the organizational chart, campaign pledges, meeting minutes, "
            "bylaws, archives and an inquiry system\n"
            "- Facility Booking System: automated reservation system for meeting rooms in the Student Union building\n"
            "- Admin Dashboard (CMS): lets council members manage content directly so all information stays up to date\n"
            "- KUS-BUS Integration: absorbed the earlier shuttle & cafeteria service (2024–2026)",
        ),
        "KUS-BUS: 셔틀버스·학식 자동 트래킹 웹 서비스": (
            "고려대학교 세종캠퍼스 학생들을 위해 셔틀버스 실시간 도착 정보와 주간 학식 메뉴를 자동으로 제공하는 "
            "웹 서비스를 개발·배포했습니다. (서비스 종료 · 총학생회 플랫폼으로 통합)\n"
            "- 실시간 셔틀버스 트래커: 공식 버스 시간표를 CSV로 변환하고, JavaScript로 다음 도착까지 남은 시간을 계산해 표시\n"
            "- 자동 웹 스크래퍼: Python·BeautifulSoup으로 학교 공식 학식 페이지를 크롤링하고 HTML을 JSON으로 변환해 시각화\n"
            "- 파이프라인 자동화: 매주 월요일 아침 스크래핑이 자동 실행되고 API 엔드포인트로 JSON을 갱신해 수동 관리 불필요\n"
            "- 배포 및 인프라: Heroku로 배포하고 Gabia·Cloudflare로 도메인 라우팅과 DNS를 직접 관리",
            "Developed and deployed a utility web service for Korea University Sejong Campus students, providing "
            "real-time shuttle bus arrival times and automated weekly cafeteria menus. (Service concluded · merged "
            "into the student council platform)\n"
            "- Real-Time Shuttle Bus Tracker: converted official bus schedules into CSV and built JavaScript logic "
            "to calculate and display the exact time remaining until the next arrivals\n"
            "- Automated Web Scraper: used Python and BeautifulSoup to crawl the university's official cafeteria "
            "menu page, parsing the HTML into JSON for web visualization\n"
            "- Pipeline Automation: the scraper runs every Monday morning and updates the JSON through an API "
            "endpoint, requiring zero manual maintenance\n"
            "- Deployment & Infrastructure: deployed on Heroku and managed domain routing and DNS with Gabia and "
            "Cloudflare",
        ),
        "MeQSum 데이터셋을 활용한 의료 LLM 임상 텍스트 요약 비교 분석": (
            "디지털경영전공 강현구 교수님과 함께 진행한 연구 프로젝트입니다. MeQSum 데이터셋으로 의료 분야 대규모 "
            "언어 모델(LLM)의 임상 텍스트 요약 성능을 평가·비교하고, AlignScore로 사실 일관성과 정확성을 검증했습니다.\n"
            "- LLM 성능 비교: 복잡한 임상 텍스트와 의료 질의를 요약하는 여러 LLM의 역량을 평가·비교\n"
            "- 데이터셋 및 지표 활용: 의료 NLP 과제에 MeQSum 데이터셋을 사용하고, AlignScore로 생성 요약을 사실 기반으로 엄밀하게 평가\n"
            "- 헬스케어 AI 적용: 텍스트 생성 모델의 정렬도와 환각(hallucination) 비율을 분석해 신뢰할 수 있는 의료 AI 발전에 기여",
            "A research project with Professor Hyungu Kahng (Digital Management, Korea University), evaluating and "
            "comparing the clinical text summarization performance of large language models in the healthcare "
            "domain using the MeQSum dataset, with AlignScore to ensure factual consistency and accuracy.\n"
            "- LLM Performance Comparison: evaluated and compared various LLMs in summarizing complex clinical texts "
            "and medical inquiries\n"
            "- Dataset & Metric Utilization: leveraged MeQSum for medical NLP tasks and AlignScore for a rigorous, "
            "fact-based assessment of the generated summaries\n"
            "- Healthcare AI Application: analyzed the alignment and hallucination rates of text generation models "
            "to advance reliable AI in medicine",
        ),
        "수직농장 AI 제어 시스템을 위한 생육 이미지 데이터 활용 방안 개발": (
            "한국발명진흥회(KIPA) 주관 2023 미래전략 창업지원 프로그램의 일환으로, 수직농장 AI 제어 시스템에 적용할 "
            "작물 생육 이미지 데이터의 활용 방법 개발에 연구원으로 참여했습니다.",
            "Participated as a researcher in developing methods for applying crop growth image data to AI-based "
            "vertical farm control systems, as part of the 2023 Future Strategy Startup Support Program organized by "
            "the Korea Invention Promotion Association (KIPA).",
        ),
        "지도학습·연합학습 기반 CCTV 영상 객체 탐지": (
            "고려대학교 창의적 학부연구 프로그램(CURT)에서 지도학습과 연합학습(Federated Learning)을 활용해 "
            "Python 기반 CCTV 영상 객체 탐지 모델을 구축했습니다.",
            "Built CCTV object detection models in Python using supervised learning and federated learning, as part "
            "of Korea University's Creative Undergraduate Research Training Program (CURT).",
        ),
        "감정 인식 및 자살 위험 탐지를 위한 얼굴 영상 분석 시스템": (
            "전자및정보공학과 한철 교수님과 함께 진행한 연구 프로젝트로, 얼굴 영상에서 감정 표현과 자살 징후를 "
            "조기에 추출해 정신건강 개입을 강화하는 예측 기술을 개발했습니다.\n"
            "- 기술 개발: 얼굴 영상 데이터로 감정 상태와 잠재적 자살 징후를 정확하게 추출하는 알고리즘 개발\n"
            "- 조기 탐지 및 예방: 예방 조치를 강화해 자살률을 낮추는 것을 목표로 한 조기 탐지 모델 구축\n"
            "- 신속한 개입: 위험군을 조기에 식별해 신속하고 적절한 지원이 가능하도록 시스템 설계",
            "A research project with Professor Chul Han (Electronics and Information Engineering, Korea University), "
            "developing predictive technology that extracts emotional expressions and early signs of suicide risk "
            "from facial videos to strengthen mental health interventions.\n"
            "- Technology Development: an algorithm that accurately extracts emotional states and potential signs "
            "of suicide from facial video data\n"
            "- Early Detection & Prevention: an early-detection model aimed at reducing South Korea's suicide rate "
            "by enhancing preventative measures\n"
            "- Prompt Intervention: designed to identify at-risk individuals early, enabling swift and appropriate support",
        ),
    },

    # ── academic (key: "name|category") ────────────────────────────────────
    'academic_items': {
        "Cross-Linguistic Moral Preferences in Large Language Models: Evidence from Distributive Justice "
        "Scenarios and Domain Persona Interventions|journal": (
            "대규모 언어 모델(LLM)의 언어 간 추론 특성을 다룬 제1저자 연구입니다. AI 에이전트가 분배 정의 시나리오에서 "
            "언어에 따라 서로 다른 선호를 보이는 현상과, 이러한 불일치를 효과적으로 완화하는 방법을 제시했습니다.\n"
            "[주요 결과]\n"
            "- Gemini 2.0 Flash를 영어·한국어로 6개 행동경제학 분배 정의 시나리오에서 평가해 120만 건 이상의 관측치 생성\n"
            "- 최대 56%p의 격차와 완전한 선호 역전 등 큰 언어 의존적 차이를 발견 — 도덕 심리학의 인간 '외국어 효과'와 유사\n"
            "- 사회학·경제학·법학·철학·역사학 등 규범 학문의 도메인 페르소나를 주입하면 언어 간 격차가 평균 62.7% 감소\n"
            "- 다국어 LLM 배포를 위한 보완적 통합 프레임워크를 제안하고, 언어 간 일관성을 AI 정렬의 핵심 지표로 제시\n"
            "[게재]\n"
            "SeonGyu Jang, Chaewon Jeong, Jimin Kim, Hyungu Kahng (2025). Electronics, 14(24), 4919. "
            "doi:10.3390/electronics14244919",
            "A first-author study of the cross-linguistic reasoning of large language models, showing how AI agents "
            "exhibit language-dependent preferences in distributive justice scenarios and how these inconsistencies "
            "can be mitigated.\n"
            "[Key Findings]\n"
            "- Evaluated Gemini 2.0 Flash in English and Korean across six behavioral-economics distributive justice "
            "scenarios, generating over 1.2 million observations\n"
            "- Found substantial language-dependent divergences — gaps of up to 56 percentage points and complete "
            "preference reversals — paralleling the human foreign-language effect in moral psychology\n"
            "- Domain-specific personas from normative disciplines (sociology, economics, law, philosophy, history) "
            "reduce cross-linguistic gaps by 62.7% on average\n"
            "- Proposed a compensatory integration framework for multilingual LLM deployment, establishing "
            "cross-linguistic consistency as an AI alignment metric\n"
            "[Citation]\n"
            "SeonGyu Jang, Chaewon Jeong, Jimin Kim, Hyungu Kahng (2025). Electronics, 14(24), 4919. "
            "doi:10.3390/electronics14244919",
        ),
        "Cross-Linguistic Moral Preferences in Large Language Models: Evidence from Distributive Justice "
        "Scenarios and Domain Persona Interventions|presentation": (
            "Electronics(MDPI)에 게재된 제1저자 연구를 2025 한국데이터마이닝학회 추계학술대회에서 포스터로 발표했습니다.",
            "Presented the first-author study published in Electronics (MDPI) as a poster at the Korean Data Mining "
            "Society Fall Conference 2025.",
        ),
        "Controlling Informational Freedom in Large Language Models via Degree of Freedom Prompting|presentation": (
            "LLM이 출력에서 발휘하는 정보 자유도의 정도를 자유도 프롬프팅(Degree of Freedom Prompting)으로 제어하는 "
            "연구에 공동저자로 참여했습니다. 2025 한국데이터마이닝학회 하계학술대회에서 포스터로 발표해 "
            "최우수논문상을 수상했습니다.",
            "Co-authored a study on controlling how much informational freedom an LLM exercises in its outputs "
            "through degree-of-freedom prompting. Presented as a poster at the KDMS Summer Conference 2025 and "
            "awarded the Best Paper Award.",
        ),
        "Moral Alignment in Large Language Models: Effects of Linguistic Framing and Domain Personas|presentation": (
            "대규모 언어 모델의 도덕적 정렬에 언어적 프레이밍과 도메인 페르소나가 미치는 영향을 연구해 "
            "2025 한국데이터마이닝학회 하계학술대회에서 포스터로 발표했습니다.",
            "Studied how linguistic framing and domain personas affect the moral alignment of large language "
            "models; presented as a poster at the KDMS Summer Conference 2025.",
        ),
        "2025 한국데이터마이닝학회 하계학술대회|conference": (
            "최신 데이터마이닝 연구와 AI 분야를 학습하고, 포스터 발표를 진행했습니다.",
            "Learned about recent data mining and AI research and presented posters.",
        ),
        "2024 한국데이터마이닝학회 추계학술대회|conference": (
            "데이터마이닝 및 AI 분야의 연구 발표를 청강했습니다.",
            "Attended research presentations in data mining and AI.",
        ),
        "2024 한국데이터마이닝학회 춘계학술대회|conference": (
            "데이터마이닝 및 AI 분야의 최신 연구를 접했습니다.",
            "Explored recent research in data mining and AI.",
        ),
        "2023 한국IT서비스학회 춘계학술대회|conference": (
            "IT 서비스 분야의 최신 연구 동향을 학습하고 교육을 이수했습니다.",
            "Learned about recent research trends in IT services and completed the conference training.",
        ),
    },

    # ── awards (key: "name|award_result") ──────────────────────────────────
    'awards': {
        "한국데이터마이닝학회 하계학술대회|최우수논문상": (
            "2025 한국데이터마이닝학회(KDMS) 하계학술대회에서 'Controlling Informational Freedom in Large Language "
            "Models via Degree of Freedom Prompting' 논문으로 최우수논문상을 수상했습니다.",
            "Won the Best Paper Award at the 2025 KDMS (Korean Data Mining Society) Summer Conference for the paper "
            "'Controlling Informational Freedom in Large Language Models via Degree of Freedom Prompting'.",
        ),
        "최우수학생 표창|표창": (
            "우수한 학업 성적과 모범적인 생활을 인정받아 고려대학교 세종캠퍼스 최우수학생으로 선정되어 표창장을 받았습니다.",
            "Awarded a Certificate of Commendation as a Highest Honors Student at Korea University Sejong Campus in "
            "recognition of outstanding academic performance and exemplary conduct.",
        ),
        "2024 기업기술혁신 PBL|우수상": (
            "고려대학교 산학협력교육센터 주관 PBL(Project-Based Learning) 프로젝트로 (주)팜킷과 협업했습니다. "
            "이커머스 전략, TableOCR 연계 식품 챗봇 프로세스, 식품 데이터 마이닝과 데이터 라벨링 알고리즘을 개발해 "
            "우수상을 수상했습니다.",
            "Collaborated with FarmKit Co., Ltd. through the PBL (Project-Based Learning) project organized by the "
            "Korea University Center for Industry-Academia Education. Won the Excellence Award for developing "
            "e-commerce strategies, a TableOCR-integrated food chatbot process, food data mining and data labeling "
            "algorithms.",
        ),
        "2024 KUS-TUDY|최우수상": (
            "고려대학교 세종 교육혁신원 주관 KUS-TUDY 프로그램에 참여해, '파이썬을 활용한 Business Data Analytics' "
            "과목에서 우수한 학업 성과와 높은 평가를 받은 최종 보고서로 최우수상을 수상했습니다.",
            "Participated in the KUS-TUDY Program organized by the Korea University Sejong Institute for Educational "
            "Innovation, and received the Top Excellence Award for outstanding performance and a highly evaluated "
            "final report in 'Business Data Analytics Using Python'.",
        ),
        "2024 세종시 기업분석 경진대회|최우수상": (
            "세종 경력개발센터 주관 '2024 세종시 기업분석 경진대회'에서 주식회사 서북에 대한 종합 기업 분석으로 "
            "최우수상을 수상했습니다.",
            "Conducted a comprehensive corporate analysis of Seobuk Co., Ltd., earning the Top Excellence Award at "
            "the 2024 Sejong City Corporate Analysis Competition organized by the Sejong Career Development Center.",
        ),
        "2024 청년 일경험 프로그램 성과공유회|우수상": (
            "고려대학교 세종산학협력단 주관 '2024 청년 일경험 프로그램' 성과공유회에서, (주)팜킷 근무 중 개발한 "
            "이커머스 전략과 TableOCR 연계 식품 챗봇 프로세스로 우수상을 수상했습니다.",
            "Won the Excellence Award at the project showcase of the 2024 Youth Work Experience Program (Korea "
            "University Sejong Research and Business Foundation) for the e-commerce strategies and TableOCR-integrated "
            "food chatbot process developed at FarmKit Co., Ltd.",
        ),
        "2024 산학협력친화형 PBL 수강 후기 공모전|은상": (
            "고려대학교 산학협력교육센터 주관 수기 공모전에서 '데이터분석과 인공지능을 통해 선한 영향력을 끼치는 "
            "개발자에 다가가다'로 은상을 수상했습니다.",
            "Won the Silver Award in an essay contest hosted by the Korea University Center for Industry-Academia "
            "Education with the essay 'Becoming a Developer Who Creates a Positive Impact Through Data Analysis and AI'.",
        ),
        "2024 T-SUM 데이터분석/인공지능 경진대회|대상 및 우수멘토상": (
            "킥보드 주행 영상 분석을 통한 객체 탐지 AI 모델을 개발해, 고려대학교 산학협력교육센터 주관 T-SUM "
            "데이터분석·인공지능 경진대회에서 대상과 우수멘토상을 수상했습니다.",
            "Developed an object detection AI model by analyzing e-scooter driving footage, winning the Grand Prize "
            "and the Outstanding Mentor Award at the T-SUM Data Analysis & AI Competition organized by the Korea "
            "University Center for Industry-Academia Education.",
        ),
        "창업경진대회|우수상": (
            "캐릭터 브랜드 'JOOINJANG'을 창업해 브랜딩, 굿즈 제작, 사업화 전 과정을 운영했습니다. 주요 백화점으로 "
            "판로를 확장하고 공식 NGO와 협업해 사회적 가치를 창출한 브랜딩 사업으로 우수상을 수상했습니다.",
            "Founded and developed the character brand 'JOOINJANG', managing the full cycle of branding, merchandise "
            "production and commercialization. Won the Excellence Award for a branding business that expanded to "
            "major department stores and created social impact with official NGOs.",
        ),
        "충청권 ICT이노베이션스퀘어 인공지능 중급과정 프로젝트 발표회|은상": (
            "'공공데이터를 활용한 고급 머신러닝·딥러닝 과정'(충청권 ICT이노베이션스퀘어 확산사업) 프로젝트 발표회에서, "
            "객체 탐지 알고리즘으로 도로 노면 상태를 분석해 교통사고를 예방하는 기술을 개발해 은상을 수상했습니다.",
            "Won the Silver Award for a traffic accident prevention technology that analyzes road surface conditions "
            "with object detection, at the project exhibition of the Intermediate AI Course (KU): Advanced Machine "
            "Learning & Deep Learning with Public Data (Chungcheong ICT Innovation Square Expansion Project).",
        ),
        "충청권 ICT이노베이션스퀘어 인공지능 중급과정 프로젝트 발표회|동상": (
            "'공공데이터를 활용한 고급 머신러닝·딥러닝 과정'(충청권 ICT이노베이션스퀘어 확산사업) 프로젝트 발표회에서, "
            "객체 탐지 알고리즘으로 CCTV 영상을 분석해 응급상황과 위급환자를 식별하는 AI 시스템을 개발해 동상을 수상했습니다.",
            "Won the Bronze Award for an AI system that uses object detection to analyze CCTV footage and identify "
            "emergency situations and critical patients, at the project exhibition of the Intermediate AI Course "
            "(KU): Advanced Machine Learning & Deep Learning with Public Data (Chungcheong ICT Innovation Square).",
        ),
    },

    # ── experience (key: KR title) ─────────────────────────────────────────
    'current_activities': {
        "제38대 총학생회 '비범' 부총학생회장": (
            "고려대학교 세종캠퍼스 제38대 총학생회 부총학생회장으로서 대학 본부와 적극적으로 소통·협상하며 학생 복지와 "
            "교육 환경 개선에 힘쓰고 있습니다. 주요 위원회와 리더십 역할을 맡아 대학 행정과 학생자치 전반에 기여하고 있습니다.\n"
            "[주요 역할]\n"
            "- 2026.08 · 2026년 1·2분기 예산결산특별위원회 위원\n"
            "- 2026.07 · 2027 새내기배움터 준비위원회 위원장\n"
            "- 2026.07 · 총학생회칙 개정 준비위원회 위원\n"
            "- 2026.04 · 2025년 3·4분기 예산결산특별위원회 위원장\n"
            "- 2026.03 · 2026년 3월 보궐선거 선거관리위원회 위원\n"
            "- 2026.02 · 2026 대동제 준비위원회 기획홍보 총괄\n"
            "- 2026.01 · 2026 새내기배움터 기획·안전 총괄\n"
            "- 2026.01 · 제38대 총학생회 시설 TF 팀장\n"
            "- 2025.12 · 2026학년도 등록금심의위원회 학생위원",
            "Serving as Vice President of the 38th Student Council at Korea University Sejong Campus, dedicated to "
            "enhancing student welfare and educational environments by actively communicating and negotiating with "
            "the university administration, and contributing to university administration and student governance "
            "through key leadership and committee roles.\n"
            "[Key Responsibilities & Roles]\n"
            "- 2026.08 · Member, Special Committee on Budget and Accounts (1st/2nd Quarters, 2026)\n"
            "- 2026.07 · Chairperson, Preparation Committee for the 2027 Freshman Orientation\n"
            "- 2026.07 · Member, Student Council Bylaws Revision Preparation Committee\n"
            "- 2026.04 · Chairperson, Special Committee on Budget and Accounts (3rd/4th Quarters, 2025)\n"
            "- 2026.03 · Member, Election Management Committee for the March 2026 By-election\n"
            "- 2026.02 · Head of Planning & PR, 2026 Festival Preparation Committee\n"
            "- 2026.01 · Head of Planning & Safety, 2026 Freshman Orientation\n"
            "- 2026.01 · Head of the Facilities Task Force, 38th Student Council\n"
            "- 2025.12 · Student Representative, 2026 Tuition Fee Review Committee",
        ),
    },
    'past_activities': {
        "2026학년도 등록금심의위원회 학생위원": (
            "고려대학교 세종캠퍼스 등록금심의위원회에 학생위원으로 위촉되어 등록금 협상에 참여하고 대학 예산 편성을 검토했습니다.",
            "Served as an appointed student representative on the Tuition Fee Review Committee at Korea University "
            "Sejong Campus, participating in tuition fee negotiations and reviewing university budget allocations.",
        ),
        "JOOINJANG CTO": (
            "캐릭터 브랜드 'JOOINJANG'의 사업자를 등록하고 브랜딩, 굿즈 제작, 사업화 전 과정을 운영했습니다. "
            "신세계·현대·롯데백화점 등 주요 유통 채널에 입점하고 COEX·KINTEX 등 대형 일러스트 페어에 참가했으며, "
            "초록우산 어린이재단과의 공식 협업으로 사회공헌 활동을 이끌었습니다.\n"
            "[브랜드 런칭 & 사회공헌]\n"
            "- 2023.06 · 브랜드 런칭 및 공식 인스타그램 개설\n"
            "- 2023.09 · 초록우산 어린이재단 자립준비청년 지원 사업 참여\n"
            "- 2024.01 · JOOINJANG 공식 온라인몰 오픈\n"
            "- 2024.06 · 초록우산 어린이재단 인플루언서 및 초록빛클럽 멤버 선정\n"
            "- 2024.07 · 텀블벅 크라우드펀딩 오픈\n"
            "[입점 (온라인 · 오프라인)]\n"
            "- 2023.08 · O-ROUNG MD 활동 및 온라인 입점\n"
            "- 2023.09 · MAPPLE# 온라인 입점\n"
            "- 2023.12 · AMUAMU MD 활동\n"
            "- 2024.03 · 세인즈(성신여대), 연다굿즈(수지), 신세계백화점 본점\n"
            "- 2024.04 · 현대백화점 중동점, 오마이라라(경주 황리단길), 성수연방(성수)\n"
            "- 2024.07 · 아이파크몰 용산점, 롯데백화점 잠실점, 코엑스 파르나스몰, AK플라자 홍대점\n"
            "- 2024.08 · 롯데백화점 영등포점, 스파크랜드(대구 동성로)\n"
            "[팝업 & 페어]\n"
            "- 2023.10 · 코믹월드 문구페어 (수원메쎄)\n"
            "- 2023.12 · 코믹월드 문구페어 (일산 KINTEX)\n"
            "- 2024.01 · 굿즈 아울렛 페어 (성수 BINCAN)\n"
            "- 2024.03 · 코믹월드 문구페어 (양재 aT센터), 굿즈이즈굿 페어 (서울 SETEC)\n"
            "- 2024.04 · 사곰찜 페어 (홍대), 다꾸빌리지 페스타 (DDP)\n"
            "- 2024.05 · 서울일러스트레이션페어 (서울 COEX)\n"
            "- 2024.06 · 서대문구 청년잡화점\n"
            "- 2024.07 · 코믹월드 문구페어 (일산 KINTEX)",
            "Registered a business to launch and grow the character brand 'JOOINJANG', managing branding, "
            "merchandise production and commercialization. Secured placements in major retailers (Shinsegae, Hyundai, "
            "Lotte department stores), exhibited at large-scale illustration fairs (COEX, KINTEX), and led social "
            "impact initiatives through official collaborations with ChildFund Korea.\n"
            "[Brand Launch & Social Impact]\n"
            "- 2023.06 · Brand launch & official Instagram opened\n"
            "- 2023.09 · Joined ChildFund Korea's project supporting youth transitioning out of care\n"
            "- 2024.01 · Opened the official JOOINJANG online mall\n"
            "- 2024.06 · Selected as a ChildFund Korea Influencer & Chorobit Club member\n"
            "- 2024.07 · Launched a Tumblbug crowdfunding campaign\n"
            "[Retail Placements (Online & Offline)]\n"
            "- 2023.08 · O-ROUNG MD activity & online placement\n"
            "- 2023.09 · MAPPLE# online placement\n"
            "- 2023.12 · AMUAMU MD activity\n"
            "- 2024.03 · Seins (Sungshin Women's Univ.), Yeonda Goods (Suji), Shinsegae Department Store (Main Branch)\n"
            "- 2024.04 · Hyundai Department Store (Jungdong), Oh My Lala (Gyeongju Hwangridan-gil), Seongsuyeonbang (Seongsu)\n"
            "- 2024.07 · IPARK Mall (Yongsan), Lotte Department Store (Jamsil), COEX Parnas Mall, AK Plaza (Hongdae)\n"
            "- 2024.08 · Lotte Department Store (Yeongdeungpo), Sparkland (Daegu Dongseong-ro)\n"
            "[Pop-up Stores & Fairs]\n"
            "- 2023.10 · Comic World Stationery Fair (Suwon Messe)\n"
            "- 2023.12 · Comic World Stationery Fair (Ilsan KINTEX)\n"
            "- 2024.01 · Goods Outlet Fair (Seongsu BINCAN)\n"
            "- 2024.03 · Comic World Stationery Fair (Yangjae aT Center) & Goods is Good Fair (Seoul SETEC)\n"
            "- 2024.04 · Sagomjjit Fair (Hongdae) & Dakku Village Festa (DDP)\n"
            "- 2024.05 · Seoul Illustration Korea (Seoul COEX)\n"
            "- 2024.06 · Youth General Store hosted by Seodaemun-gu\n"
            "- 2024.07 · Comic World Stationery Fair (Ilsan KINTEX)",
        ),
        "(주)팜킷 AI Developer 인턴": (
            "(주)팜킷에서 AI 개발자 인턴으로 근무하며 이커머스 전략과 TableOCR 연계 식품 챗봇 프로세스를 개발했습니다.\n"
            "- TableOCR 연계 식품 챗봇 프로세스 구축\n"
            "- 식품 데이터 마이닝 및 데이터 라벨링 알고리즘 설계\n"
            "- 이커머스 전략 수립\n"
            "- 성과: 기업기술혁신 PBL 우수상, 2024 청년 일경험 프로그램 성과공유회 우수상",
            "Worked as an AI Developer Intern at FarmKit Co., Ltd., developing e-commerce strategies and a "
            "TableOCR-integrated food chatbot process.\n"
            "- Built a TableOCR-integrated food chatbot process\n"
            "- Designed food data mining and data labeling algorithms\n"
            "- Developed e-commerce strategies\n"
            "- Recognition: Excellence Award (Corporate Technology Innovation PBL) and Excellence Award (2024 Youth "
            "Work Experience Program)",
        ),
        "데이터분석 및 인공지능 학회 'PRISM' 창립 및 1기 학회장": (
            "고려대학교 세종캠퍼스 크림슨브레인 소속 데이터분석 및 인공지능 학회 'PRISM'을 창립하고 이끌었습니다. "
            "20~30명 규모 학회의 조직 운영, 프로젝트 일정 관리, 예산 집행, 행사 기획을 총괄했습니다.\n"
            "또한 데이터분석·AI 기초 강의의 강사로 활동하고 학회원들의 외부 학술대회 참여를 이끌었으며, "
            "각종 공모전과 산학 R&SD 프로젝트를 주도해 의미 있는 성과를 거두었습니다.",
            "Founded and directed PRISM, a Data Analysis and Artificial Intelligence Academic Society affiliated with "
            "Crimson Brain at Korea University Sejong Campus, overseeing organizational management, project "
            "scheduling, budget execution and event planning for 20–30 members.\n"
            "Also served as an instructor for foundational data analytics and AI lectures, facilitated member "
            "participation in external conferences, and led various competitions and industry–academia R&SD projects.",
        ),
        "중앙동아리 AD-ZONE 총무": (
            "고려대학교 세종캠퍼스 중앙 광고·마케팅 동아리 AD-ZONE의 총무로서 동아리 예산을 관리·집행하고 결산 보고를 진행했습니다.",
            "As Treasurer of AD-ZONE, the university-wide advertising & marketing club at Korea University Sejong "
            "Campus, managed and executed the club budget and prepared financial settlement reports.",
        ),
        "중앙동아리 AD-ZONE 부회장": (
            "AD-ZONE 부회장으로서 프로젝트 운영 전반, 인사 관리, 예산 집행을 총괄하며 동아리를 이끌었습니다.",
            "As Vice President of AD-ZONE, led the club by overseeing project operations, managing human resources "
            "and executing the budget.",
        ),
        "중앙동아리 AD-ZONE 기획팀장": (
            "AD-ZONE 기획팀장으로서 예산을 조율하고 운영을 실행하며 전체 행사를 기획했습니다.",
            "As Planning Team Lead for AD-ZONE, coordinated the budget, executed operations and planned overall events.",
        ),
        "제45대 총동아리연합회 '파란' 기획국장": (
            "고려대학교 세종캠퍼스 제45대 총동아리연합회 '파란'의 기획국장으로서 내부 인력을 관리하고 사업 전반의 "
            "기획부터 실행까지를 총괄했습니다.",
            "As Head of the Planning Department of the 45th General Student Club Association 'Paran', directed "
            "internal human resources and managed overall project lifecycles.",
        ),
        "제44대 총동아리연합회 '동심' 홍보국원": (
            "제44대 총동아리연합회 '동심' 홍보국원으로서 공식 홍보물을 디자인하고 연합회 행사를 운영했습니다.",
            "As a member of the Public Relations Department of the 44th General Student Club Association 'Dongsim', "
            "designed official publications and executed organizational events.",
        ),
    },
}


def detail_key(table, row):
    if table == 'academic_items':
        return f"{row.get('name', '')}|{row.get('category', '')}"
    if table == 'awards':
        return f"{row.get('name', '')}|{row.get('award_result', '')}"
    return row.get('title') or row.get('name') or ''


def apply_details(seed):
    for table, rows in seed.items():
        if table not in DETAILS:
            continue
        mapping = DETAILS[table]
        for row in rows:
            ko, en = mapping.get(detail_key(table, row), ('', ''))
            row.setdefault('details', ko)
            row.setdefault('details_en', en)
    return seed
