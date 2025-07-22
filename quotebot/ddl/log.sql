-- Create log table
CREATE TABLE IF NOT EXISTS log
(
    time            TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ROWID           INTEGER PRIMARY KEY                 NOT NULL, -- use sqlite rowid as pk instead of redundant auto inc
    user            TEXT                                NOT NULL,
    action          VARCHAR(100)                        NOT NULL,
    status          VARCHAR(50)                         NOT NULL,
    additional_info TEXT
)