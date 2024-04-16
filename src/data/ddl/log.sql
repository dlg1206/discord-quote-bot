-- Create log table
CREATE TABLE IF NOT EXISTS log
(
    time            TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id              INTEGER AUTO INCREMENT PRIMARY KEY   NOT NULL,
    user            TEXT                                NOT NULL,
    action          VARCHAR(100)                        NOT NULL,
    status          VARCHAR(50)                         NOT NULL,
    additional_info TEXT
)