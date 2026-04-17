Metadata DB (SQL):
- 谁拥有哪个 KB     users 1 -> N knowledge_bases
- 哪些文件属于哪个 KB         knowledge_bases 1 -> N documents 
- 每个文件当前处理到什么状态       documents 1 -> N ingestion_jobs
- 一个 chunk / vector 最终来自哪个文档版本       document 1 -> N chunks

create table users (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    password_hash text not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table documents (
    id uuid primary key default gen_random_uuid(),
    kb_id uuid not null references knowledge_bases(id) on delete cascade,
    user_id uuid not null references users(id) on delete cascade,
    filename text not null,
    normalized_filename text not null,
    file_type text not null,
    mime_type text,
    storage_bucket text not null,
    storage_key text not null,
    file_size_bytes bigint,
    checksum text,
    status text not null default 'uploaded',
    embedding_model text,
    chunk_count integer,
    token_count integer,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    deleted_at timestamptz,
    unique (kb_id, normalized_filename)
);

create index idx_documents_kb_id on documents(kb_id);
create index idx_documents_user_id on documents(user_id);
create index idx_documents_status on documents(status);


create table knowledge_bases (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    name text not null,
    description text,
    status text not null default 'active',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index idx_kbs_user_id on knowledge_bases(user_id);

create table ingestion_jobs (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    kb_id uuid not null references knowledge_bases(id) on delete cascade,
    document_id uuid not null references documents(id) on delete cascade,
    job_type text not null default 'ingest',
    status text not null default 'queued',
    started_at timestamptz,
    finished_at timestamptz,
);

create index idx_ingestion_jobs_document_id on ingestion_jobs(document_id);
create index idx_ingestion_jobs_status on ingestion_jobs(status);

create table chunks (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users(id) on delete cascade,
    kb_id uuid not null references knowledge_bases(id) on delete cascade,
    document_id uuid not null references documents(id) on delete cascade,
    chunk_index integer not null,
    vector_id text not null,
    text_preview text,
    created_at timestamptz not null default now(),
    unique (document_id, chunk_index),
    unique (vector_id)
);

create index idx_chunks_user_kb on chunks(user_id, kb_id);
create index idx_chunks_document_id on chunks(document_id);