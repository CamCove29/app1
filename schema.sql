CREATE DATABASE biblioteca;

USE biblioteca;

CREATE TABLE Autor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    fecha_nacimiento DATE,
    nacionalidad VARCHAR(50),
    biografia TEXT
);

CREATE TABLE Libro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100),
    id_autor INT,
    isbn VARCHAR(20),
    genero VARCHAR(50),
    fecha_publicacion DATE,
    paginas INT,
    editorial VARCHAR(100),
    idioma VARCHAR(50),
    resumen TEXT,
    disponibilidad BOOLEAN,
    FOREIGN KEY (id_autor) REFERENCES Autor(id)
);

-- Datos de ejemplo:
INSERT INTO Autor (id, nombre, fecha_nacimiento, nacionalidad, biografia)
VALUES (1, 'Gabriel García Márquez', '1927-03-06', 'Colombiana', 'Gabriel García Márquez fue un escritor, novelista, cuentista, guionista y periodista colombiano.');

INSERT INTO Libro (id_autor, titulo, isbn, genero, fecha_publicacion, paginas, editorial, idioma, resumen, disponibilidad)
VALUES (1, 'Cien Años de Soledad', '978-3-16-148410-0', 'Realismo Mágico', '1967-05-30', 417, 'Sudamericana', 'Español', 'Una historia épica de la familia Buendía en la mítica ciudad de Macondo.', TRUE);
