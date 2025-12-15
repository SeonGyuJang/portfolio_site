from flask import Flask, render_template, abort
import os

app = Flask(__name__)

# 템플릿 폴더 내의 파일들을 스캔하여 활동 목록을 반환하는 함수
def get_activities():
    activities = []
    # Match template directory names (case-insensitive mapping to category keys)
    categories = ['Paper', 'Book', 'School', 'Study', 'reading']
    base_dir = os.path.join(app.root_path, 'templates')
    
    for category in categories:
        category_dir = os.path.join(base_dir, category)
        if os.path.exists(category_dir):
            for filename in os.listdir(category_dir):
                if filename.endswith('.html'):
                    # 파일명에서 확장자 제거 및 언더바를 공백으로 변경하여 제목으로 사용
                    title = filename.replace('.html', '').replace('_', ' ')
                    activities.append({
                        'category': category.lower(),
                        'filename': filename,
                        'title': title,
                        # 각 카테고리별 아이콘 및 설명 매핑 (필요시 수정)
                        'icon': get_icon_for_category(category.lower()),
                        'date': '2025.11' # 임시 날짜, 필요시 파일 메타데이터 등 활용 가능
                    })
    return activities

def get_icon_for_category(category):
    icons = {
        'paper': 'fas fa-file-alt',
        'book': 'fas fa-book',
        'school': 'fas fa-university',
        'study': 'fas fa-code',
        'reading': 'fas fa-book-open'
    }
    return icons.get(category, 'fas fa-star')

@app.route('/')
def index():
    activities = get_activities()
    return render_template('index.html', activities=activities)

# Activity 상세 페이지 라우트
@app.route('/activity/<category>/<filename>')
def activity_detail(category, filename):
    # 경로 조작 방지를 위한 간단한 검증
    if category not in ['paper', 'book', 'school', 'study', 'reading']:
        abort(404)
    
    try:
        return render_template(f'{category}/{filename}')
    except:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, port='4444')