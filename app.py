from flask import Flask, render_template, abort, request, redirect, url_for, session, jsonify
import os
import json
import logging
import uuid
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change')

SUPABASE_URL = os.environ.get('SUPABASE_URL', '').strip()
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '').strip()
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin1234')

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
        # Verify connection with a lightweight query
        supabase.table('current_activities').select('id').limit(1).execute()
        logger.info("Supabase connection established successfully")
    except Exception as e:
        _supabase_error = str(e)
        logger.error(f"Supabase connection error: {e}")


# ── helpers ────────────────────────────────────────────────────────────────

def db_fetch(table, order_col='sort_order', ascending=True):
    if not supabase:
        return []
    try:
        res = supabase.table(table).select('*').order(order_col, desc=not ascending).execute()
        return res.data or []
    except Exception as e:
        print(f"DB fetch error ({table}): {e}")
        return []

def db_insert(table, data):
    if not supabase:
        return None, "Supabase not configured"
    try:
        res = supabase.table(table).insert(data).execute()
        return res.data, None
    except Exception as e:
        return None, str(e)

def db_update(table, row_id, data):
    if not supabase:
        return None, "Supabase not configured"
    try:
        res = supabase.table(table).update(data).eq('id', row_id).execute()
        return res.data, None
    except Exception as e:
        return None, str(e)

def db_delete(table, row_id):
    if not supabase:
        return False, "Supabase not configured"
    try:
        supabase.table(table).delete().eq('id', row_id).execute()
        return True, None
    except Exception as e:
        return False, str(e)


def get_last_updated():
    """Return the stored last-updated date string (YYYY.MM.DD)."""
    if not supabase:
        return '2025.12.21'
    try:
        res = supabase.table('site_settings').select('value').eq('key', 'last_updated').execute()
        if res.data:
            return res.data[0]['value']
    except Exception:
        pass
    return '2025.12.21'


def update_last_updated():
    """Upsert today's date into site_settings whenever any data changes."""
    if not supabase:
        return
    today = datetime.now().strftime('%Y.%m.%d')
    try:
        supabase.table('site_settings').upsert(
            {'key': 'last_updated', 'value': today, 'updated_at': 'now()'}
        ).execute()
    except Exception as e:
        logger.warning(f"update_last_updated failed: {e}")


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


def get_static_activities():
    """Scan template folders for static HTML activity files (legacy)."""
    activities = []
    categories = ['Paper', 'Book', 'School', 'Study', 'reading']
    icon_map = {
        'paper': 'fas fa-file-alt', 'book': 'fas fa-book',
        'school': 'fas fa-university', 'study': 'fas fa-code',
        'reading': 'fas fa-book-open'
    }
    base_dir = os.path.join(app.root_path, 'templates')
    for cat in categories:
        cat_dir = os.path.join(base_dir, cat)
        if os.path.exists(cat_dir):
            for fname in os.listdir(cat_dir):
                if fname.endswith('.html'):
                    activities.append({
                        'id': None,
                        'source': 'static',
                        'category': cat.lower(),
                        'filename': fname,
                        'title': fname.replace('.html', '').replace('_', ' '),
                        'icon': icon_map.get(cat.lower(), 'fas fa-star'),
                        'date_text': '',
                        'tags': [],
                    })
    return activities


# ── public routes ──────────────────────────────────────────────────────────

@app.route('/')
def index():
    db_logs = db_fetch('activity_logs', order_col='created_at', ascending=False)
    static_acts = get_static_activities()
    data = {
        'current_activities': db_fetch('current_activities'),
        'past_activities': db_fetch('past_activities'),
        'tech_stacks': db_fetch('tech_stacks'),
        'projects': db_fetch('projects'),
        'awards': db_fetch('awards'),
        'academic_items': db_fetch('academic_items'),
        'certificates': db_fetch('certificates'),
        'activity_logs': db_logs,
        'static_activities': static_acts,
        'supabase_ready': supabase is not None,
        'last_updated': get_last_updated(),
    }
    return render_template('index.html', **data)


@app.route('/activity/log/<log_id>')
def activity_log_view(log_id):
    if not supabase:
        abort(404)
    try:
        res = supabase.table('activity_logs').select('*').eq('id', log_id).execute()
        if not res.data:
            abort(404)
        log = res.data[0]
        blocks = log.get('blocks', [])
        if isinstance(blocks, str):
            blocks = json.loads(blocks)
        return render_template('activity_log_view.html', log=log, blocks=blocks)
    except Exception:
        abort(404)


@app.route('/activity/<category>/<filename>')
def activity_detail(category, filename):
    if category not in ['paper', 'book', 'school', 'study', 'reading']:
        abort(404)
    folder_mapping = {
        'paper': 'Paper', 'book': 'Book', 'school': 'School',
        'study': 'Study', 'reading': 'reading'
    }
    real_folder = folder_mapping.get(category, category)
    try:
        return render_template(f'{real_folder}/{filename}')
    except Exception:
        abort(404)


# ── admin auth ──────────────────────────────────────────────────────────────

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


# ── admin dashboard ─────────────────────────────────────────────────────────

@app.route('/admin')
@require_admin
def admin_dashboard():
    stats = {}
    for t in ['current_activities','past_activities','tech_stacks','projects',
              'awards','academic_items','certificates','activity_logs']:
        rows = db_fetch(t)
        stats[t] = len(rows)
    return render_template('admin/dashboard.html', stats=stats, supabase_ready=supabase is not None)


# ── current activities ───────────────────────────────────────────────────────

@app.route('/admin/current-activities')
@require_admin
def admin_current_activities():
    items = db_fetch('current_activities')
    return render_template('admin/current_activities.html', items=items)

@app.route('/admin/current-activities/save', methods=['POST'])
@require_admin
def admin_current_activities_save():
    row_id = request.form.get('id', '').strip()
    data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip(),
        'date_start': request.form.get('date_start', '').strip(),
        'date_end': request.form.get('date_end', '').strip(),
        'is_ongoing': request.form.get('is_ongoing') == 'on',
        'sort_order': int(request.form.get('sort_order', 0) or 0),
    }
    if row_id:
        db_update('current_activities', row_id, data)
    else:
        db_insert('current_activities', data)
    update_last_updated()
    return redirect(url_for('admin_current_activities'))

@app.route('/admin/current-activities/delete/<row_id>', methods=['POST'])
@require_admin
def admin_current_activities_delete(row_id):
    db_delete('current_activities', row_id)
    update_last_updated()
    return redirect(url_for('admin_current_activities'))


# ── past activities ──────────────────────────────────────────────────────────

@app.route('/admin/past-activities')
@require_admin
def admin_past_activities():
    items = db_fetch('past_activities')
    return render_template('admin/past_activities.html', items=items)

@app.route('/admin/past-activities/save', methods=['POST'])
@require_admin
def admin_past_activities_save():
    row_id = request.form.get('id', '').strip()
    data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip(),
        'date_start': request.form.get('date_start', '').strip(),
        'date_end': request.form.get('date_end', '').strip(),
        'sort_order': int(request.form.get('sort_order', 0) or 0),
    }
    if row_id:
        db_update('past_activities', row_id, data)
    else:
        db_insert('past_activities', data)
    update_last_updated()
    return redirect(url_for('admin_past_activities'))

@app.route('/admin/past-activities/delete/<row_id>', methods=['POST'])
@require_admin
def admin_past_activities_delete(row_id):
    db_delete('past_activities', row_id)
    update_last_updated()
    return redirect(url_for('admin_past_activities'))


# ── tech stacks ──────────────────────────────────────────────────────────────

@app.route('/admin/tech-stacks')
@require_admin
def admin_tech_stacks():
    items = db_fetch('tech_stacks')
    return render_template('admin/tech_stacks.html', items=items)

@app.route('/admin/tech-stacks/save', methods=['POST'])
@require_admin
def admin_tech_stacks_save():
    row_id = request.form.get('id', '').strip()
    data = {
        'category': request.form.get('category', '').strip(),
        'category_icon': request.form.get('category_icon', '').strip(),
        'name': request.form.get('name', '').strip(),
        'icon_class': request.form.get('icon_class', '').strip(),
        'level': int(request.form.get('level', 50) or 50),
        'sort_order': int(request.form.get('sort_order', 0) or 0),
    }
    if row_id:
        db_update('tech_stacks', row_id, data)
    else:
        db_insert('tech_stacks', data)
    update_last_updated()
    return redirect(url_for('admin_tech_stacks'))

@app.route('/admin/tech-stacks/delete/<row_id>', methods=['POST'])
@require_admin
def admin_tech_stacks_delete(row_id):
    db_delete('tech_stacks', row_id)
    update_last_updated()
    return redirect(url_for('admin_tech_stacks'))


# ── projects ──────────────────────────────────────────────────────────────────

@app.route('/admin/projects')
@require_admin
def admin_projects():
    items = db_fetch('projects')
    return render_template('admin/projects.html', items=items)

@app.route('/admin/projects/save', methods=['POST'])
@require_admin
def admin_projects_save():
    row_id = request.form.get('id', '').strip()
    data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip(),
        'icon_class': request.form.get('icon_class', 'fas fa-code').strip(),
        'date_start': request.form.get('date_start', '').strip(),
        'date_end': request.form.get('date_end', '').strip(),
        'is_ongoing': request.form.get('is_ongoing') == 'on',
        'link': request.form.get('link', '').strip(),
        'sort_order': int(request.form.get('sort_order', 0) or 0),
    }
    if row_id:
        db_update('projects', row_id, data)
    else:
        db_insert('projects', data)
    update_last_updated()
    return redirect(url_for('admin_projects'))

@app.route('/admin/projects/delete/<row_id>', methods=['POST'])
@require_admin
def admin_projects_delete(row_id):
    db_delete('projects', row_id)
    update_last_updated()
    return redirect(url_for('admin_projects'))


# ── awards ────────────────────────────────────────────────────────────────────

@app.route('/admin/awards')
@require_admin
def admin_awards():
    items = db_fetch('awards')
    return render_template('admin/awards.html', items=items)

@app.route('/admin/awards/save', methods=['POST'])
@require_admin
def admin_awards_save():
    row_id = request.form.get('id', '').strip()
    images_raw = request.form.get('images', '[]').strip()
    try:
        images = json.loads(images_raw) if images_raw else []
    except Exception:
        images = [u.strip() for u in images_raw.split('\n') if u.strip()]
    data = {
        'name': request.form.get('name', '').strip(),
        'subject': request.form.get('subject', '').strip(),
        'award_result': request.form.get('award_result', '').strip(),
        'date_text': request.form.get('date_text', '').strip(),
        'organization': request.form.get('organization', '').strip(),
        'description': request.form.get('description', '').strip(),
        'images': images,
        'icon_class': request.form.get('icon_class', 'fas fa-trophy').strip(),
        'sort_order': int(request.form.get('sort_order', 0) or 0),
    }
    if row_id:
        db_update('awards', row_id, data)
    else:
        db_insert('awards', data)
    update_last_updated()
    return redirect(url_for('admin_awards'))

@app.route('/admin/awards/delete/<row_id>', methods=['POST'])
@require_admin
def admin_awards_delete(row_id):
    db_delete('awards', row_id)
    update_last_updated()
    return redirect(url_for('admin_awards'))


# ── academic items ────────────────────────────────────────────────────────────

@app.route('/admin/academic')
@require_admin
def admin_academic():
    items = db_fetch('academic_items')
    return render_template('admin/academic.html', items=items)

@app.route('/admin/academic/save', methods=['POST'])
@require_admin
def admin_academic_save():
    row_id = request.form.get('id', '').strip()
    images_raw = request.form.get('images', '[]').strip()
    try:
        images = json.loads(images_raw) if images_raw else []
    except Exception:
        images = [u.strip() for u in images_raw.split('\n') if u.strip()]
    data = {
        'name': request.form.get('name', '').strip(),
        'description': request.form.get('description', '').strip(),
        'date_text': request.form.get('date_text', '').strip(),
        'paper_link': request.form.get('paper_link', '').strip(),
        'images': images,
        'sort_order': int(request.form.get('sort_order', 0) or 0),
    }
    if row_id:
        db_update('academic_items', row_id, data)
    else:
        db_insert('academic_items', data)
    update_last_updated()
    return redirect(url_for('admin_academic'))

@app.route('/admin/academic/delete/<row_id>', methods=['POST'])
@require_admin
def admin_academic_delete(row_id):
    db_delete('academic_items', row_id)
    update_last_updated()
    return redirect(url_for('admin_academic'))


# ── certificates ──────────────────────────────────────────────────────────────

@app.route('/admin/certificates')
@require_admin
def admin_certificates():
    items = db_fetch('certificates')
    return render_template('admin/certificates.html', items=items)

@app.route('/admin/certificates/save', methods=['POST'])
@require_admin
def admin_certificates_save():
    row_id = request.form.get('id', '').strip()
    data = {
        'name': request.form.get('name', '').strip(),
        'issuer': request.form.get('issuer', '').strip(),
        'date_text': request.form.get('date_text', '').strip(),
        'image': request.form.get('image', '').strip(),
        'sort_order': int(request.form.get('sort_order', 0) or 0),
    }
    if row_id:
        db_update('certificates', row_id, data)
    else:
        db_insert('certificates', data)
    update_last_updated()
    return redirect(url_for('admin_certificates'))

@app.route('/admin/certificates/delete/<row_id>', methods=['POST'])
@require_admin
def admin_certificates_delete(row_id):
    db_delete('certificates', row_id)
    update_last_updated()
    return redirect(url_for('admin_certificates'))


# ── activity logs ─────────────────────────────────────────────────────────────

@app.route('/admin/activity-logs')
@require_admin
def admin_activity_logs():
    items = db_fetch('activity_logs', order_col='created_at', ascending=False)
    return render_template('admin/activity_logs.html', items=items)

@app.route('/admin/activity-logs/new')
@require_admin
def admin_activity_log_new():
    return render_template('admin/activity_log_editor.html', log=None)

@app.route('/admin/activity-logs/edit/<log_id>')
@require_admin
def admin_activity_log_edit(log_id):
    if not supabase:
        return redirect(url_for('admin_activity_logs'))
    try:
        res = supabase.table('activity_logs').select('*').eq('id', log_id).execute()
        log = res.data[0] if res.data else None
    except Exception:
        log = None
    if not log:
        return redirect(url_for('admin_activity_logs'))
    return render_template('admin/activity_log_editor.html', log=log)

@app.route('/admin/activity-logs/save', methods=['POST'])
@require_admin
def admin_activity_log_save():
    row_id = request.form.get('id', '').strip()
    blocks_raw = request.form.get('blocks', '[]')
    try:
        blocks = json.loads(blocks_raw)
    except Exception:
        blocks = []
    tags_raw = request.form.get('tags', '')
    tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
    data = {
        'title': request.form.get('title', '').strip(),
        'category': request.form.get('category', 'study').strip(),
        'date_text': request.form.get('date_text', '').strip(),
        'icon': request.form.get('icon', '📄').strip(),
        'cover_image': request.form.get('cover_image', '').strip(),
        'tags': tags,
        'blocks': blocks,
        'sort_order': int(request.form.get('sort_order', 0) or 0),
    }
    if row_id:
        data['updated_at'] = datetime.utcnow().isoformat()
        db_update('activity_logs', row_id, data)
    else:
        db_insert('activity_logs', data)
    update_last_updated()
    return redirect(url_for('admin_activity_logs'))

@app.route('/admin/activity-logs/delete/<log_id>', methods=['POST'])
@require_admin
def admin_activity_log_delete(log_id):
    db_delete('activity_logs', log_id)
    update_last_updated()
    return redirect(url_for('admin_activity_logs'))


# ── API for admin (JSON) ──────────────────────────────────────────────────────

@app.route('/admin/api/upload-image', methods=['POST'])
@require_admin
def admin_upload_image():
    """Upload image to Supabase Storage and return public URL."""
    if not supabase:
        return jsonify({'error': 'Supabase not configured'}), 400
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    bucket = 'portfolio-images'
    _, ext = os.path.splitext(file.filename or 'image.jpg')
    if not ext:
        ext = '.jpg'
    filename = f"activity-logs/{uuid.uuid4().hex}{ext.lower()}"
    try:
        content = file.read()
        supabase.storage.from_(bucket).upload(
            filename, content,
            file_options={'content-type': file.content_type or 'image/jpeg', 'upsert': 'true'}
        )
        url = supabase.storage.from_(bucket).get_public_url(filename)
        return jsonify({'url': url, 'path': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/admin/api/images')
@require_admin
def admin_list_images():
    """List images from Supabase Storage activity-logs folder."""
    if not supabase:
        return jsonify({'images': []})
    try:
        files = supabase.storage.from_('portfolio-images').list(
            'activity-logs',
            {'sortBy': {'column': 'created_at', 'order': 'desc'}}
        )
        images = []
        for f in (files or []):
            name = f.get('name', '')
            if name and not name.startswith('.'):
                path = f"activity-logs/{name}"
                url = supabase.storage.from_('portfolio-images').get_public_url(path)
                images.append({
                    'path': path,
                    'url': url,
                    'name': name,
                    'size': f.get('metadata', {}).get('size', 0) if f.get('metadata') else 0,
                })
        return jsonify({'images': images})
    except Exception as e:
        logger.error(f"admin_list_images error: {e}")
        return jsonify({'images': [], 'error': str(e)})


@app.route('/admin/api/images/delete', methods=['POST'])
@require_admin
def admin_delete_image():
    """Delete an image from Supabase Storage."""
    if not supabase:
        return jsonify({'error': 'Supabase not configured'}), 400
    data = request.get_json(silent=True) or {}
    path = data.get('path', '')
    if not path or not path.startswith('activity-logs/'):
        return jsonify({'error': 'Invalid path'}), 400
    try:
        supabase.storage.from_('portfolio-images').remove([path])
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    url_set = bool(SUPABASE_URL)
    key_set = bool(SUPABASE_KEY)
    connected = supabase is not None

    status = {
        'supabase_url_set': url_set,
        'supabase_key_set': key_set,
        'supabase_url_prefix': SUPABASE_URL[:30] + '...' if url_set else None,
        'supabase_key_prefix': SUPABASE_KEY[:20] + '...' if key_set else None,
        'supabase_key_length': len(SUPABASE_KEY) if key_set else 0,
        'supabase_connected': connected,
        'supabase_error': _supabase_error,
    }
    http_status = 200 if connected else 503
    return jsonify(status), http_status


if __name__ == '__main__':
    app.run(debug=True, port=4444)
