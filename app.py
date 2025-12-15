from flask import Flask, render_template, abort
import os

app = Flask(__name__)

# 템플릿 폴더 내의 파일들을 스캔하여 활동 목록을 반환하는 함수
def get_activities():
    activities = []
    # 실제 폴더 이름 (대소문자 주의)
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
                        # URL에는 소문자로 내보냄 (예: Paper -> paper)
                        'category': category.lower(),
                        'filename': filename,
                        'title': title,
                        'icon': get_icon_for_category(category.lower()),
                        'date': '2025.11' # 임시 날짜
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
    
    # [중요 수정] URL의 소문자 카테고리를 실제 폴더명(대소문자 포함)으로 매핑
    # 리눅스(Heroku)는 대소문자를 구분하므로 이 과정이 필수입니다.
    folder_mapping = {
        'paper': 'Paper',
        'book': 'Book',
        'school': 'School',
        'study': 'Study',
        'reading': 'reading'
    }
    
    real_folder_name = folder_mapping.get(category, category)
    
    try:
        # 실제 폴더명을 사용하여 템플릿 렌더링
        return render_template(f'{real_folder_name}/{filename}')
    except:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, port='4444')