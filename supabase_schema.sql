-- ============================================================
-- Supabase Schema for SeonGyu Jang Portfolio Admin System
-- Run this in the Supabase SQL Editor
-- ============================================================

-- Current Activities
CREATE TABLE IF NOT EXISTS current_activities (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  title text NOT NULL,
  description text,
  date_start text,
  date_end text,
  is_ongoing boolean DEFAULT true,
  sort_order integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Past Activities
CREATE TABLE IF NOT EXISTS past_activities (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  title text NOT NULL,
  description text,
  date_start text,
  date_end text,
  sort_order integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Tech Stacks
CREATE TABLE IF NOT EXISTS tech_stacks (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  category text NOT NULL,
  category_icon text DEFAULT '⚙️',
  name text NOT NULL,
  icon_class text DEFAULT 'fas fa-circle',
  level integer DEFAULT 80,
  sort_order integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Projects
CREATE TABLE IF NOT EXISTS projects (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  title text NOT NULL,
  description text,
  icon_class text DEFAULT 'fas fa-code',
  date_start text,
  date_end text,
  is_ongoing boolean DEFAULT true,
  link text,
  sort_order integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Awards
CREATE TABLE IF NOT EXISTS awards (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name text NOT NULL,
  subject text,
  award_result text,
  date_text text,
  organization text,
  description text,
  images jsonb DEFAULT '[]'::jsonb,
  icon_class text DEFAULT 'fas fa-trophy',
  sort_order integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Academic Items (학회/논문)
CREATE TABLE IF NOT EXISTS academic_items (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name text NOT NULL,
  description text,
  date_text text,
  paper_link text,
  images jsonb DEFAULT '[]'::jsonb,
  sort_order integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Certificates (자격증)
CREATE TABLE IF NOT EXISTS certificates (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name text NOT NULL,
  issuer text,
  date_text text,
  image text,
  sort_order integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Activity Logs (Notion-style)
CREATE TABLE IF NOT EXISTS activity_logs (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  title text NOT NULL,
  category text NOT NULL DEFAULT 'study',
  date_text text,
  icon text DEFAULT '📄',
  cover_image text,
  tags jsonb DEFAULT '[]'::jsonb,
  blocks jsonb DEFAULT '[]'::jsonb,
  sort_order integer DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Enable RLS (Row Level Security) - allow all for authenticated users
ALTER TABLE current_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE past_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE tech_stacks ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE awards ENABLE ROW LEVEL SECURITY;
ALTER TABLE academic_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE certificates ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;

-- Public read policy (anon can read)
CREATE POLICY "Public read" ON current_activities FOR SELECT USING (true);
CREATE POLICY "Public read" ON past_activities FOR SELECT USING (true);
CREATE POLICY "Public read" ON tech_stacks FOR SELECT USING (true);
CREATE POLICY "Public read" ON projects FOR SELECT USING (true);
CREATE POLICY "Public read" ON awards FOR SELECT USING (true);
CREATE POLICY "Public read" ON academic_items FOR SELECT USING (true);
CREATE POLICY "Public read" ON certificates FOR SELECT USING (true);
CREATE POLICY "Public read" ON activity_logs FOR SELECT USING (true);

-- Full access for service_role (used by admin panel with service_role key)
-- Or if using anon key, allow all operations:
CREATE POLICY "Anon full access" ON current_activities FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Anon full access" ON past_activities FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Anon full access" ON tech_stacks FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Anon full access" ON projects FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Anon full access" ON awards FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Anon full access" ON academic_items FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Anon full access" ON certificates FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Anon full access" ON activity_logs FOR ALL USING (true) WITH CHECK (true);

-- Storage bucket for images (run in Supabase dashboard Storage section)
-- Create a bucket named 'portfolio-images' and set it to public
