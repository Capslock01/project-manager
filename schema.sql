CREATE TABLE account (
        id SERIAL NOT NULL, 
        name VARCHAR(128), 
        password VARCHAR(128), 
        PRIMARY KEY (id)
);

CREATE TABLE work_type (
        id SERIAL NOT NULL, 
        name VARCHAR(128), 
        rounding INTERVAL MINUTE, 
        minimum INTERVAL MINUTE, 
        price NUMERIC, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
-- work_type altered to use INTERVAL instead of NUMERIC in rounding and minimum with following command:
-- ALTER TABLE work_type ALTER COLUMN rounding TYPE INTERVAL MINUTE USING rounding*'1 minute'::interval minute, ALTER COLUMN minimum TYPE INTERVAL MINUTE USING minimum*'1 minute'::interval minute

CREATE TABLE company (
        id SERIAL NOT NULL, 
        name VARCHAR(128), 
        user_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES account (id) ON DELETE CASCADE
);
-- user_id binds company to the user who created it, so that companies are kept private
-- company.name unique constraint removed to allow different users to create same name company using command:
-- ALTER TABLE company DROP CONSTRAINT company_name_key;

CREATE TABLE project (
        id SERIAL NOT NULL, 
        state INTEGER, 
        name VARCHAR(256), 
        user_id INTEGER, 
        company_id INTEGER, 
        type_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES account (id) ON DELETE CASCADE, 
        FOREIGN KEY(company_id) REFERENCES company (id) ON DELETE CASCADE, 
        FOREIGN KEY(type_id) REFERENCES work_type (id)
);

CREATE TABLE entry (
        id SERIAL NOT NULL, 
        project_id INTEGER, 
        start TIMESTAMP(0) WITHOUT TIME ZONE, 
        "end" TIMESTAMP(0) WITHOUT TIME ZONE, 
        comment VARCHAR(256), 
        PRIMARY KEY (id), 
        FOREIGN KEY(project_id) REFERENCES project (id) ON DELETE CASCADE
);
-- entry altered from TIMESTAMP to TIMESTAMP(0) to use rounding to seconds using following command:
-- ALTER TABLE entry ALTER COLUMN start TYPE TIMESTAMP(0) WITHOUT TIME ZONE, ALTER COLUMN "end" TYPE TIMESTAMP(0) WITHOUT TIME ZONE;