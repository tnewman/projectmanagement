/* File: postgresqlschema.sql
 * Description: Queries used to create the Project Management application 
 *              database schema for a PostgreSQL database.
 * Date: 2014/04/27
 * Programmer: Thomas Newman
 */

CREATE TABLE project (
  id SERIAL,
  name VARCHAR(50) NOT NULL,
  brief_description VARCHAR(50) NOT NULL,
  description VARCHAR(1000) NOT NULL,
  PRIMARY KEY (id));

CREATE TABLE task (
  id SERIAL,
  project_id INTEGER NOT NULL,
  name VARCHAR(50) NOT NULL,
  brief_description VARCHAR(50) NOT NULL,
  description VARCHAR(1000) NOT NULL,
  complexity VARCHAR(50) NOT NULL,
  due_date TIMESTAMP NOT NULL,
  status VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_task_project
    FOREIGN KEY (project_id)
    REFERENCES project (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE login (
  id SERIAL,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(50) NOT NULL,
  PRIMARY KEY (id));