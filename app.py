from flask import (Flask, render_template, abort, request, redirect, url_for, session,
                   jsonify, flash, Response, send_from_directory)
import os
import copy
import json
import base64
import logging
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

from content_seed import SEED
from i18n import LANGS, UI, PROFILE, LINKS

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change')

SUPABASE_URL = os.environ.get('SUPABASE_URL', '').strip()
if SUPABASE_URL and not SUPABASE_URL.endswith('/'):
    SUPABASE_URL = SUPABASE_URL + '/'
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '').strip()
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin1234')

CV_DIR = os.path.join(app.root_path, 'static', 'files')
CV_FILENAME = 'SeonGyu_Jang_CV.pdf'

supabase = None
_supabase_error = None

if not SUPABASE_URL:
    logger.error("SUPABASE_URL environment variable is not set or empty")
elif not SUPABASE_KEY:
    logger.error("SUPABASE_KEY environment variable is not set or empty")
else:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        supabase.table('current_activities').select('id').limit(1).execute()
        logger.info("Supabase connection established successfully")
    except Exception as e:
        _supabase_error = str(e)
        logger.error(f"Supabase connection error: {e}")


# ── content model ──────────────────────────────────────────────────────────
# One definition per table drives both the public site and the admin CRUD UI.
# `legacy` marks columns that exist in the original schema; the rest are added
# by supabase_migration_v2.sql. Writes fall back to legacy columns if the
# migration has not been run yet.

def F(name, label, type='text', legacy=False, required=False, options=None, placeholder='', wide=False):
    return {'name': name, 'label': label, 'type': type, 'legacy': legacy, 'required': required,
            'options': options or [], 'placeholder': placeholder, 'wide': wide}


TABLE_DEFS = {
    'current_activities': {
        'slug': 'current-activities', 'label': '현재 활동', 'icon': 'fas fa-rocket',
        'fields': [
            F('title', '제목 (KR)', legacy=True, required=True),
            F('title_en', 'Title (EN)'),
            F('description', '설명 (KR)', 'textarea', legacy=True),
            F('description_en', 'Description (EN)', 'textarea'),
            F('date_start', '시작', legacy=True, placeholder='2025.12'),
            F('date_end', '종료', legacy=True, placeholder='비워두면 진행 중'),
            F('is_ongoing', '진행 중', 'checkbox', legacy=True),
            F('sort_order', '정렬 순서 (작을수록 위)', 'number', legacy=True),
        ],
        'columns': ['title', 'title_en', 'date_start'], 'en_check': 'title_en',
    },
    'past_activities': {
        'slug': 'past-activities', 'label': '이전 활동', 'icon': 'fas fa-flag-checkered',
        'fields': [
            F('title', '제목 (KR)', legacy=True, required=True),
            F('title_en', 'Title (EN)'),
            F('description', '설명 (KR)', 'textarea', legacy=True),
            F('description_en', 'Description (EN)', 'textarea'),
            F('date_start', '시작', legacy=True, placeholder='2024.03'),
            F('date_end', '종료', legacy=True, placeholder='2024.12'),
            F('sort_order', '정렬 순서 (작을수록 위)', 'number', legacy=True),
        ],
        'columns': ['title', 'title_en', 'date_start'], 'en_check': 'title_en',
    },
    'projects': {
        'slug': 'projects', 'label': '프로젝트', 'icon': 'fas fa-folder-open',
        'fields': [
            F('title', '제목 (KR)', legacy=True, required=True),
            F('title_en', 'Title (EN)'),
            F('description', '설명 (KR)', 'textarea', legacy=True),
            F('description_en', 'Description (EN)', 'textarea'),
            F('category', '구분', 'select', options=[('software', '소프트웨어'), ('research', '연구')]),
            F('link', '링크', legacy=True, placeholder='https://...'),
            F('date_start', '시작', legacy=True, placeholder='2024.11'),
            F('date_end', '종료', legacy=True),
            F('is_ongoing', '진행 중', 'checkbox', legacy=True),
            F('sort_order', '정렬 순서 (작을수록 위)', 'number', legacy=True),
            F('images', '이미지', 'images', wide=True),
        ],
        'columns': ['title', 'category', 'date_start'], 'en_check': 'title_en',
    },
    'awards': {
        'slug': 'awards', 'label': '수상', 'icon': 'fas fa-trophy',
        'fields': [
            F('name', '대회/수상명 (KR)', legacy=True, required=True),
            F('name_en', 'Award / Event (EN)'),
            F('award_result', '결과 (KR)', legacy=True, placeholder='최우수상'),
            F('award_result_en', 'Result (EN)', placeholder='Top Excellence Award'),
            F('subject', '주제 (KR)', legacy=True),
            F('subject_en', 'Subject (EN)'),
            F('organization', '주관 기관 (KR)', legacy=True),
            F('organization_en', 'Organization (EN)'),
            F('description', '상세 설명 (KR)', 'textarea', legacy=True),
            F('description_en', 'Description (EN)', 'textarea'),
            F('date_text', '날짜', legacy=True, placeholder='2024.12'),
            F('sort_order', '정렬 순서 (작을수록 위)', 'number', legacy=True),
            F('images', '증빙 이미지', 'images', legacy=True, wide=True),
        ],
        'columns': ['name', 'award_result', 'date_text'], 'en_check': 'name_en',
    },
    'academic_items': {
        'slug': 'academic', 'label': '논문 · 학술', 'icon': 'fas fa-graduation-cap',
        'fields': [
            F('name', '제목 (KR 또는 원제)', legacy=True, required=True),
            F('name_en', 'Title (EN, 원제와 같으면 비움)'),
            F('category', '구분', 'select',
              options=[('journal', '학술지 논문'), ('presentation', '학술대회 발표'), ('conference', '학술대회 참가')]),
            F('authors', '저자', placeholder='SeonGyu Jang, ...'),
            F('venue', '게재처/학회 (KR)'),
            F('venue_en', 'Venue (EN)'),
            F('description', '요약 (KR)', 'textarea', legacy=True),
            F('description_en', 'Summary (EN)', 'textarea'),
            F('date_text', '날짜', legacy=True, placeholder='2025.12'),
            F('paper_link', '논문 링크', legacy=True, placeholder='https://doi.org/...'),
            F('sort_order', '정렬 순서 (작을수록 위)', 'number', legacy=True),
            F('images', '이미지', 'images', legacy=True, wide=True),
        ],
        'columns': ['name', 'category', 'date_text'], 'en_check': 'venue_en',
    },
    'certificates': {
        'slug': 'certificates', 'label': '자격증', 'icon': 'fas fa-certificate',
        'fields': [
            F('name', '자격증명 (KR)', legacy=True, required=True),
            F('name_en', 'Certificate (EN)'),
            F('issuer', '발급 기관 (KR)', legacy=True),
            F('issuer_en', 'Issuer (EN)'),
            F('date_text', '취득일', legacy=True, placeholder='2024.03'),
            F('sort_order', '정렬 순서 (작을수록 위)', 'number', legacy=True),
            F('image', '증명서 이미지', 'image', legacy=True, wide=True),
        ],
        'columns': ['name', 'issuer', 'date_text'], 'en_check': 'name_en',
    },
}
SLUG_TO_TABLE = {d['slug']: t for t, d in TABLE_DEFS.items()}
LEGACY_COLS = {t: {f['name'] for f in d['fields'] if f['legacy']} | {'icon_class'}
               for t, d in TABLE_DEFS.items()}
NEW_COLS = {t: [f['name'] for f in d['fields'] if not f['legacy']] for t, d in TABLE_DEFS.items()}


# ── db helpers ─────────────────────────────────────────────────────────────

def db_fetch(table):
    """Rows ordered for display, or None if the database is unavailable."""
    if not supabase:
        return None
    try:
        res = (supabase.table(table).select('*')
               .order('sort_order').order('created_at').execute())
        return res.data or []
    except Exception as e:
        logger.error(f"DB fetch error ({table}): {e}")
        return None


def seed_rows(table):
    rows = copy.deepcopy(SEED.get(table, []))
    return sorted(rows, key=lambda r: r.get('sort_order', 0))


def load_content():
    """Load every table from one place so the site and admin always agree.

    Returns (content, source) where source is 'db' or 'seed' (fallback).
    """
    content, source = {}, 'db'
    for table in TABLE_DEFS:
        rows = db_fetch(table)
        if rows is None:
            rows, source = seed_rows(table), 'seed'
        content[table] = rows
    return content, source


def _missing_column(err):
    msg = (err or '').lower()
    return 'pgrst204' in msg or ('column' in msg and ('not find' in msg or 'does not exist' in msg))


def db_write(table, row_id, data):
    """Insert/update a row. Returns (error, partial) — partial=True means only
    legacy columns were saved because the v2 migration has not been run."""
    if not supabase:
        return 'Supabase가 연결되어 있지 않습니다.', False

    def run(payload):
        try:
            q = supabase.table(table)
            if row_id:
                q.update(payload).eq('id', row_id).execute()
            else:
                q.insert(payload).execute()
            return None
        except Exception as e:
            return str(e)

    err = run(data)
    if err and _missing_column(err):
        legacy = {k: v for k, v in data.items() if k in LEGACY_COLS[table]}
        err2 = run(legacy)
        return err2, err2 is None
    return err, False


def db_delete(table, row_id):
    if not supabase:
        return 'Supabase가 연결되어 있지 않습니다.'
    try:
        supabase.table(table).delete().eq('id', row_id).execute()
        return None
    except Exception as e:
        return str(e)


def schema_missing_tables():
    """Tables that still lack the v2 (English / category) columns."""
    if not supabase:
        return []
    missing = []
    for table, cols in NEW_COLS.items():
        try:
            supabase.table(table).select(','.join(cols)).limit(1).execute()
        except Exception:
            missing.append(table)
    return missing


def sync_seed(tables):
    """Replace the given tables with the CV-based default content."""
    missing = set(schema_missing_tables())
    errors = []
    for table in tables:
        rows = seed_rows(table)
        if table in missing:
            rows = [{k: v for k, v in r.items() if k in LEGACY_COLS[table]} for r in rows]
        try:
            supabase.table(table).delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            if rows:
                supabase.table(table).insert(rows).execute()
        except Exception as e:
            errors.append(f'{table}: {e}')
    return errors


def get_last_updated():
    if supabase:
        try:
            res = supabase.table('site_settings').select('value').eq('key', 'last_updated').execute()
            if res.data:
                return res.data[0]['value']
        except Exception:
            pass
    return datetime.now().strftime('%Y.%m.%d')


def update_last_updated():
    if not supabase:
        return
    today = datetime.now().strftime('%Y.%m.%d')
    try:
        supabase.table('site_settings').upsert(
            {'key': 'last_updated', 'value': today, 'updated_at': 'now()'}
        ).execute()
    except Exception as e:
        logger.warning(f"update_last_updated failed: {e}")


def decode_blob(value):
    """portfolio_images.image_data holds base64 text; a bytea column returns it hex-escaped."""
    if isinstance(value, str) and value.startswith('\\x'):
        value = bytes.fromhex(value[2:]).decode('ascii')
    return base64.b64decode(value)


def get_uploaded_cv(with_data=False):
    if not supabase:
        return None
    cols = 'id,filename,created_at' + (',image_data,mime_type' if with_data else '')
    try:
        res = (supabase.table('portfolio_images').select(cols).eq('item_type', 'cv')
               .order('created_at', desc=True).limit(1).execute())
        return res.data[0] if res.data else None
    except Exception as e:
        logger.warning(f"CV lookup failed: {e}")
        return None


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


@app.after_request
def no_cache(resp):
    # Always serve fresh data on the site and admin pages (no stale browser cache).
    if request.path.startswith('/admin') or request.path in ('/', '/en'):
        resp.headers['Cache-Control'] = 'no-store, max-age=0'
    return resp


# ── template helpers ───────────────────────────────────────────────────────

def asset(url):
    if not url:
        return ''
    if url.startswith(('http://', 'https://', '/', 'data:')):
        return url
    return '/' + url


def make_helpers(lang):
    ui = UI[lang]

    def t(key):
        return ui.get(key, key)

    def L(item, field):
        if lang == 'en':
            return item.get(f'{field}_en') or item.get(field) or ''
        return item.get(field) or ''

    def period(start, end=None, ongoing=False):
        start, end = (start or '').strip(), (end or '').strip()
        if ongoing and not end:
            return f'{start} – {ui["present"]}' if start else ui['present']
        if end and end != start:
            return f'{start} – {end}' if start else end
        return start

    return {'t': t, 'L': L, 'period': period}


app.jinja_env.globals['asset'] = asset
app.jinja_env.filters['asset'] = asset


# ── public routes ──────────────────────────────────────────────────────────

def render_site(lang):
    content, source = load_content()
    projects = content['projects']
    academic = content['academic_items']
    ctx = {
        'lang': lang,
        'other_lang_url': url_for('index_en') if lang == 'ko' else url_for('index'),
        'profile': PROFILE[lang],
        'links': LINKS,
        'current_activities': content['current_activities'],
        'past_activities': content['past_activities'],
        'research_projects': [p for p in projects if (p.get('category') or 'software') == 'research'],
        'software_projects': [p for p in projects if (p.get('category') or 'software') != 'research'],
        'journals': [a for a in academic if a.get('category') == 'journal'],
        'presentations': [a for a in academic if (a.get('category') or 'presentation') == 'presentation'],
        'conferences': [a for a in academic if a.get('category') == 'conference'],
        'awards': content['awards'],
        'certificates': content['certificates'],
        'last_updated': get_last_updated(),
        **make_helpers(lang),
    }
    return render_template('index.html', **ctx)


@app.route('/')
def index():
    if request.args.get('lang') == 'en':
        return redirect(url_for('index_en'))
    return render_site('ko')


@app.route('/en')
def index_en():
    return render_site('en')


@app.route('/ko')
def index_ko():
    return redirect(url_for('index'))


@app.route('/cv')
def download_cv():
    cv = get_uploaded_cv(with_data=True)
    if cv:
        try:
            data = decode_blob(cv['image_data'])
            return Response(data, mimetype=cv.get('mime_type') or 'application/pdf', headers={
                'Content-Disposition': f'attachment; filename="{CV_FILENAME}"',
                'Cache-Control': 'no-store',
            })
        except Exception as e:
            logger.error(f"CV decode failed: {e}")
    return send_from_directory(CV_DIR, CV_FILENAME, as_attachment=True,
                               download_name=CV_FILENAME, max_age=0)


@app.route('/api/images/<image_id>')
def get_image(image_id):
    if not supabase:
        return "Image not available", 404
    try:
        result = supabase.table('portfolio_images').select('*').eq('id', image_id).execute()
        if result.data:
            img = result.data[0]
            return decode_blob(img['image_data']), 200, {
                'Content-Type': img.get('mime_type', 'image/jpeg'),
                'Cache-Control': 'public, max-age=86400',
            }
        return "Image not found", 404
    except Exception as e:
        logger.error(f"Get image error: {e}")
        return "Error loading image", 500


# ── admin auth ─────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        error = '비밀번호가 올바르지 않습니다.'
    return render_template('admin/login.html', error=error)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


@app.context_processor
def admin_globals():
    return {'TABLE_DEFS': TABLE_DEFS}


# ── admin dashboard ────────────────────────────────────────────────────────

@app.route('/admin')
@require_admin
def admin_dashboard():
    content, source = load_content()
    return render_template(
        'admin/dashboard.html',
        stats={t: len(rows) for t, rows in content.items()},
        source=source,
        supabase_ready=supabase is not None,
        supabase_error=_supabase_error,
        missing_tables=schema_missing_tables(),
        cv=get_uploaded_cv(),
        last_updated=get_last_updated(),
    )


@app.route('/admin/sync-seed', methods=['POST'])
@require_admin
def admin_sync_seed():
    if not supabase:
        flash('Supabase가 연결되어 있지 않아 불러올 수 없습니다.', 'error')
        return redirect(url_for('admin_dashboard'))
    table = request.form.get('table', '')
    tables = [table] if table in TABLE_DEFS else list(TABLE_DEFS)
    errors = sync_seed(tables)
    update_last_updated()
    if errors:
        flash('일부 테이블을 불러오지 못했습니다: ' + ' / '.join(errors), 'error')
    else:
        flash('CV 기준 데이터로 교체했습니다.', 'success')
    back = request.form.get('next')
    return redirect(back if back and back.startswith('/admin') else url_for('admin_dashboard'))


@app.route('/admin/export.json')
@require_admin
def admin_export():
    content, _ = load_content()
    body = json.dumps(content, ensure_ascii=False, indent=2, default=str)
    stamp = datetime.now().strftime('%Y%m%d_%H%M')
    return Response(body, mimetype='application/json', headers={
        'Content-Disposition': f'attachment; filename="portfolio_backup_{stamp}.json"'})


@app.route('/admin/<name>.sql')
@require_admin
def admin_sql(name):
    files = {'schema': 'supabase_schema.sql', 'migration': 'supabase_migration_v2.sql'}
    if name not in files:
        abort(404)
    return send_from_directory(app.root_path, files[name], as_attachment=True, mimetype='text/plain')


# ── admin: CV ──────────────────────────────────────────────────────────────

@app.route('/admin/cv/upload', methods=['POST'])
@require_admin
def admin_cv_upload():
    file = request.files.get('file')
    if not supabase:
        flash('Supabase가 연결되어 있지 않습니다. static/files/ 의 PDF를 교체해 주세요.', 'error')
    elif not file or not file.filename.lower().endswith('.pdf'):
        flash('PDF 파일을 선택해 주세요.', 'error')
    else:
        try:
            content = file.read()
            supabase.table('portfolio_images').insert({
                'filename': file.filename,
                'mime_type': 'application/pdf',
                'image_data': base64.b64encode(content).decode('utf-8'),
                'item_type': 'cv',
            }).execute()
            latest = get_uploaded_cv()
            if latest:
                supabase.table('portfolio_images').delete().eq('item_type', 'cv').neq('id', latest['id']).execute()
            update_last_updated()
            flash(f'CV를 업로드했습니다: {file.filename}', 'success')
        except Exception as e:
            flash(f'CV 업로드 실패: {e}', 'error')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/cv/reset', methods=['POST'])
@require_admin
def admin_cv_reset():
    if supabase:
        try:
            supabase.table('portfolio_images').delete().eq('item_type', 'cv').execute()
            flash('기본 CV 파일로 되돌렸습니다.', 'success')
        except Exception as e:
            flash(f'실패: {e}', 'error')
    return redirect(url_for('admin_dashboard'))


# ── admin: generic CRUD ────────────────────────────────────────────────────

def table_for_slug(slug):
    table = SLUG_TO_TABLE.get(slug)
    if not table:
        abort(404)
    return table


def parse_form(table):
    data = {}
    for f in TABLE_DEFS[table]['fields']:
        raw = request.form.get(f['name'], '')
        if f['type'] == 'checkbox':
            data[f['name']] = request.form.get(f['name']) == 'on'
        elif f['type'] == 'number':
            try:
                data[f['name']] = int(raw or 0)
            except ValueError:
                data[f['name']] = 0
        elif f['type'] == 'images':
            try:
                images = json.loads(raw) if raw.strip() else []
            except ValueError:
                images = [u.strip() for u in raw.splitlines() if u.strip()]
            data[f['name']] = [u for u in images if isinstance(u, str) and u.strip()]
        else:
            data[f['name']] = raw.strip()
    return data


@app.route('/admin/<slug>')
@require_admin
def admin_table(slug):
    table = table_for_slug(slug)
    content, source = load_content()
    return render_template('admin/table.html', table=table, slug=slug, spec=TABLE_DEFS[table],
                           items=content[table], source=source,
                           missing=table in schema_missing_tables())


@app.route('/admin/<slug>/save', methods=['POST'])
@require_admin
def admin_table_save(slug):
    table = table_for_slug(slug)
    row_id = request.form.get('id', '').strip()
    err, partial = db_write(table, row_id, parse_form(table))
    if err:
        flash(f'저장 실패: {err}', 'error')
    else:
        update_last_updated()
        if partial:
            flash('저장했지만 영어(EN)·구분 항목은 저장되지 않았습니다. 대시보드의 안내에 따라 '
                  'DB 마이그레이션 SQL을 먼저 실행해 주세요.', 'warning')
        else:
            flash('저장했습니다.', 'success')
    return redirect(url_for('admin_table', slug=slug))


@app.route('/admin/<slug>/delete/<row_id>', methods=['POST'])
@require_admin
def admin_table_delete(slug, row_id):
    table = table_for_slug(slug)
    err = db_delete(table, row_id)
    if err:
        flash(f'삭제 실패: {err}', 'error')
    else:
        update_last_updated()
        flash('삭제했습니다.', 'success')
    return redirect(url_for('admin_table', slug=slug))


@app.route('/admin/api/upload-image', methods=['POST'])
@require_admin
def admin_upload_image():
    if not supabase:
        return jsonify({'error': 'Supabase not configured'}), 400
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    try:
        content = file.read()
        result = supabase.table('portfolio_images').insert({
            'filename': file.filename or 'image.jpg',
            'mime_type': file.content_type or 'image/jpeg',
            'image_data': base64.b64encode(content).decode('utf-8'),
            'item_type': (request.form.get('item_type') or 'portfolio')[:40],
        }).execute()
        if result.data:
            image_id = result.data[0]['id']
            return jsonify({'url': f'/api/images/{image_id}', 'image_id': image_id})
        return jsonify({'error': 'Failed to save image'}), 500
    except Exception as e:
        logger.error(f"Image upload error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    connected = supabase is not None
    return jsonify({
        'supabase_url_set': bool(SUPABASE_URL),
        'supabase_key_set': bool(SUPABASE_KEY),
        'supabase_connected': connected,
        'supabase_error': _supabase_error,
    }), 200 if connected else 503


if __name__ == '__main__':
    app.run(debug=True, port=4444)
