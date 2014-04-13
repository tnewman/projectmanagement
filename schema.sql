CREATE TABLE project (
  id SERIAL,
  name VARCHAR(50) NOT NULL UNIQUE,
  brief_description VARCHAR(45) NOT NULL,
  description VARCHAR(1000) NOT NULL,
  PRIMARY KEY (id));

CREATE TABLE task (
  id SERIAL,
  project_id INTEGER NOT NULL,
  name VARCHAR(45) NOT NULL UNIQUE,
  brief_description VARCHAR(45) NOT NULL,
  description VARCHAR(45) NOT NULL,
  complexity VARCHAR(45) NOT NULL,
  due_date TIMESTAMP WITH TIME ZONE NOT NULL,
  status VARCHAR(45) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_task_project
    FOREIGN KEY (project_id)
    REFERENCES project (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE login (
  id SERIAL,
  username VARCHAR(45) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL,
  PRIMARY KEY (id));