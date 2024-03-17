CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'clientpw';
GRANT ALL PRIVILEGES ON goodreads.* TO 'appadmin'@'localhost';
GRANT SELECT ON goodreads.* TO 'appclient'@'localhost';
FLUSH PRIVILEGES;
