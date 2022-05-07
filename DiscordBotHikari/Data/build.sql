CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer primary key,
    Prefix TEXT DEFAULT "$$"
);

CREATE TABLE IF NOT EXISTS errors (
    err_id TEXT PRIMARY KEY,
    err_time NUMERIC DEFAULT CURRENT_TIMESTAMP,
    err_cmd TEXT,
    err_text TEXT
);