-- ============================================================
-- Portfolio v2 migration: English (EN) fields + categories
-- Run once in the Supabase SQL Editor. Safe to run again.
-- ============================================================

ALTER TABLE current_activities ADD COLUMN IF NOT EXISTS title_en text;
ALTER TABLE current_activities ADD COLUMN IF NOT EXISTS description_en text;

ALTER TABLE past_activities ADD COLUMN IF NOT EXISTS title_en text;
ALTER TABLE past_activities ADD COLUMN IF NOT EXISTS description_en text;

ALTER TABLE projects ADD COLUMN IF NOT EXISTS title_en text;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS description_en text;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS category text DEFAULT 'software';
ALTER TABLE projects ADD COLUMN IF NOT EXISTS images jsonb DEFAULT '[]'::jsonb;

ALTER TABLE awards ADD COLUMN IF NOT EXISTS name_en text;
ALTER TABLE awards ADD COLUMN IF NOT EXISTS subject_en text;
ALTER TABLE awards ADD COLUMN IF NOT EXISTS award_result_en text;
ALTER TABLE awards ADD COLUMN IF NOT EXISTS organization_en text;
ALTER TABLE awards ADD COLUMN IF NOT EXISTS description_en text;

ALTER TABLE academic_items ADD COLUMN IF NOT EXISTS name_en text;
ALTER TABLE academic_items ADD COLUMN IF NOT EXISTS description_en text;
ALTER TABLE academic_items ADD COLUMN IF NOT EXISTS category text DEFAULT 'presentation';
ALTER TABLE academic_items ADD COLUMN IF NOT EXISTS authors text;
ALTER TABLE academic_items ADD COLUMN IF NOT EXISTS venue text;
ALTER TABLE academic_items ADD COLUMN IF NOT EXISTS venue_en text;

ALTER TABLE certificates ADD COLUMN IF NOT EXISTS name_en text;
ALTER TABLE certificates ADD COLUMN IF NOT EXISTS issuer_en text;

-- Key-value settings (last updated date). Created here too in case it is missing.
CREATE TABLE IF NOT EXISTS site_settings (
  key text PRIMARY KEY,
  value text NOT NULL,
  updated_at timestamptz DEFAULT now()
);
ALTER TABLE site_settings ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Public read" ON site_settings;
DROP POLICY IF EXISTS "Anon full access" ON site_settings;
CREATE POLICY "Public read" ON site_settings FOR SELECT USING (true);
CREATE POLICY "Anon full access" ON site_settings FOR ALL USING (true) WITH CHECK (true);

-- Refresh the PostgREST schema cache so the new columns are usable immediately
NOTIFY pgrst, 'reload schema';
