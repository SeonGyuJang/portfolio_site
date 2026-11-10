#!/usr/bin/env python3
"""
CV 기준 기본 데이터(content_seed.py)를 Supabase에 채워 넣는 스크립트.
관리자 대시보드의 "CV 기준 데이터 불러오기" 버튼과 같은 동작입니다.

사용법: python migrate_to_supabase.py              (전체 테이블 교체)
       python migrate_to_supabase.py awards       (특정 테이블만)
       python migrate_to_supabase.py --dry-run    (저장 없이 확인만)
"""
import sys

from content_seed import SEED

DRY_RUN = '--dry-run' in sys.argv
targets = [a for a in sys.argv[1:] if not a.startswith('--')] or list(SEED)

unknown = [t for t in targets if t not in SEED]
if unknown:
    sys.exit(f"알 수 없는 테이블: {', '.join(unknown)} (가능: {', '.join(SEED)})")

if DRY_RUN:
    for t in targets:
        print(f"[DRY RUN] {t}: {len(SEED[t])}개 행")
    sys.exit(0)

import app  # noqa: E402  (connects to Supabase using .env)

if not app.supabase:
    sys.exit("❌ Supabase 연결 실패: SUPABASE_URL / SUPABASE_KEY 를 확인하세요.")

missing = app.schema_missing_tables()
if missing:
    print(f"⚠️  EN 컬럼이 없는 테이블: {', '.join(missing)} → 국문 내용만 저장됩니다. "
          "supabase_migration_v2.sql 을 먼저 실행하세요.")

errors = app.sync_seed(targets)
app.update_last_updated()
for t in targets:
    print(("❌ " if any(e.startswith(t + ':') for e in errors) else "✅ ") + f"{t}: {len(SEED[t])}개")
for e in errors:
    print("   ", e)
sys.exit(1 if errors else 0)
