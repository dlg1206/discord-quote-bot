-- Create the quotes table
CREATE TABLE IF NOT EXISTS quote
(
    time        TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ROWID       INTEGER PRIMARY KEY                 NOT NULL, -- use sqlite rowid as pk instead of redundant auto inc
    quote       TEXT                                NOT NULL,
    quotee      TEXT                                NOT NULL,
    contributor TEXT                                NOT NULL,
    FOREIGN KEY (quotee) REFERENCES quotee (name),
    FOREIGN KEY (contributor) REFERENCES contributor (name)
);