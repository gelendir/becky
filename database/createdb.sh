#!/bin/bash
sqlite3 db.sqlite <<EOF
CREATE TABLE calls (
    number TEXT NOT NULL,
    started_at DATETIME NOT NULL
);
EOF
