-- Run this in your Supabase SQL editor

create table if not exists analyses (
    id uuid primary key default gen_random_uuid(),
    ticker text not null,
    created_at timestamptz default now(),
    feasibility_score int,
    payload jsonb not null,
    ic_memo_path text,
    lbo_excel_path text
);

create index if not exists idx_analyses_ticker on analyses(ticker);
create index if not exists idx_analyses_created on analyses(created_at desc);
