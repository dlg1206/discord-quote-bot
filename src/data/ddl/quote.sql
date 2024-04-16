-- Create the quotes table
CREATE TABLE IF NOT EXISTS quote
(
    time        TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    qid         INTEGER AUTO INCREMENT PRIMARY KEY,
    quote       TEXT                                NOT NULL,
    quotee      TEXT                                NOT NULL,
    contributor TEXT                                NOT NULL,
    FOREIGN KEY (quotee) REFERENCES quotee (name),
    FOREIGN KEY (contributor) REFERENCES contributor (name)
);