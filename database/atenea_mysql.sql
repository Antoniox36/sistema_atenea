-- ============================================================================
-- SISTEMA ATENEA - BASE DE DATOS RELACIONAL MYSQL (LABORATORIO 2)
-- ============================================================================

CREATE DATABASE IF NOT EXISTS sistema_atenea
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE sistema_atenea;

-- ----------------------------------------------------------------------------
-- 1. USUARIOS REMOTOS DE MYSQL PARA EL EQUIPO (RADMIN VPN)
-- ----------------------------------------------------------------------------
CREATE USER IF NOT EXISTS 'antonio'@'%' IDENTIFIED BY 'antonio1234';
CREATE USER IF NOT EXISTS 'gabriel'@'%' IDENTIFIED BY 'gabriel1234';
CREATE USER IF NOT EXISTS 'pablo'@'%'   IDENTIFIED BY 'pablo1234';
CREATE USER IF NOT EXISTS 'samuel'@'%'  IDENTIFIED BY 'samuel1234';
CREATE USER IF NOT EXISTS 'fredy'@'%'   IDENTIFIED BY 'fredy1234';

GRANT ALL PRIVILEGES ON sistema_atenea.* TO 'antonio'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON sistema_atenea.* TO 'gabriel'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON sistema_atenea.* TO 'pablo'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON sistema_atenea.* TO 'samuel'@'%';
GRANT SELECT ON sistema_atenea.* TO 'fredy'@'%';
FLUSH PRIVILEGES;

-- ----------------------------------------------------------------------------
-- 2. LIMPIEZA DE TABLAS PREVIAS (ORDEN POR LLAVES FORÁNEAS)
-- ----------------------------------------------------------------------------
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS edictos;
DROP TABLE IF EXISTS asistencias;
DROP TABLE IF EXISTS entregas_desafios;
DROP TABLE IF EXISTS desafios;
DROP TABLE IF EXISTS inscripciones_agora;
DROP TABLE IF EXISTS agoras;
DROP TABLE IF EXISTS pupilos;
DROP TABLE IF EXISTS tutores;
DROP TABLE IF EXISTS materias;
DROP TABLE IF EXISTS usuarios;
SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------------------------------------------------------
-- 3. ESTRUCTURA DE TABLAS
-- ----------------------------------------------------------------------------

-- Control de acceso y roles de la aplicación ('tutor' o 'pupilo')
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash CHAR(64) NOT NULL,
    rol ENUM('tutor', 'pupilo') NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Catálogo transversal de materias que reciben tutoría
CREATE TABLE materias (
    id_materia INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    area VARCHAR(80) NOT NULL
);

-- Tutores / Mentores académicos (acceso a El Partenón)
CREATE TABLE tutores (
    id_tutor INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNIQUE NULL,
    codigo_tutor VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    especialidad VARCHAR(120) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    CONSTRAINT fk_tutor_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- Pupilos / Estudiantes de diversas carreras y ciclos (acceso al Ágora)
CREATE TABLE pupilos (
    id_pupilo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNIQUE NULL,
    carnet VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    carrera VARCHAR(120) NOT NULL,
    ciclo INT NOT NULL,
    correo VARCHAR(120) NULL,
    CONSTRAINT fk_pupilo_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- Ágoras: Círculos de tutoría donde un tutor imparte una materia
CREATE TABLE agoras (
    id_agora INT AUTO_INCREMENT PRIMARY KEY,
    nombre_agora VARCHAR(120) NOT NULL,
    id_tutor INT NOT NULL,
    id_materia INT NOT NULL,
    horario VARCHAR(100) NOT NULL,
    cupo_maximo INT NOT NULL DEFAULT 30,
    activa TINYINT(1) NOT NULL DEFAULT 1,
    CONSTRAINT fk_agora_tutor FOREIGN KEY (id_tutor)
        REFERENCES tutores(id_tutor) ON DELETE CASCADE,
    CONSTRAINT fk_agora_materia FOREIGN KEY (id_materia)
        REFERENCES materias(id_materia) ON DELETE CASCADE
);

-- Inscripción N:M de pupilos en diferentes Ágoras
CREATE TABLE inscripciones_agora (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_agora INT NOT NULL,
    id_pupilo INT NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    UNIQUE KEY uq_agora_pupilo (id_agora, id_pupilo),
    CONSTRAINT fk_insc_agora FOREIGN KEY (id_agora)
        REFERENCES agoras(id_agora) ON DELETE CASCADE,
    CONSTRAINT fk_insc_pupilo FOREIGN KEY (id_pupilo)
        REFERENCES pupilos(id_pupilo) ON DELETE CASCADE
);

-- Desafíos (Tareas) y control de Buzón habilitado/cerrado por el tutor
CREATE TABLE desafios (
    id_desafio INT AUTO_INCREMENT PRIMARY KEY,
    id_agora INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_limite DATETIME NOT NULL,
    buzon_abierto TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_desafio_agora FOREIGN KEY (id_agora)
        REFERENCES agoras(id_agora) ON DELETE CASCADE
);

-- Entregas enviadas por los pupilos en el buzón del desafío
CREATE TABLE entregas_desafios (
    id_entrega INT AUTO_INCREMENT PRIMARY KEY,
    id_desafio INT NOT NULL,
    id_pupilo INT NOT NULL,
    contenido_entrega TEXT NOT NULL,
    enlace_recurso VARCHAR(255) NULL,
    fecha_entrega TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calificacion DECIMAL(4,2) NULL,
    retroalimentacion VARCHAR(255) NULL,
    UNIQUE KEY uq_desafio_pupilo (id_desafio, id_pupilo),
    CONSTRAINT fk_entrega_desafio FOREIGN KEY (id_desafio)
        REFERENCES desafios(id_desafio) ON DELETE CASCADE,
    CONSTRAINT fk_entrega_pupilo FOREIGN KEY (id_pupilo)
        REFERENCES pupilos(id_pupilo) ON DELETE CASCADE
);

-- Registro de asistencia por sesión de tutoría
CREATE TABLE asistencias (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_agora INT NOT NULL,
    id_pupilo INT NOT NULL,
    fecha_sesion DATE NOT NULL,
    estado ENUM('Presente', 'Ausente', 'Tardanza') NOT NULL DEFAULT 'Presente',
    observacion VARCHAR(200) NULL,
    UNIQUE KEY uq_asistencia_sesion (id_agora, id_pupilo, fecha_sesion),
    CONSTRAINT fk_asist_agora FOREIGN KEY (id_agora)
        REFERENCES agoras(id_agora) ON DELETE CASCADE,
    CONSTRAINT fk_asist_pupilo FOREIGN KEY (id_pupilo)
        REFERENCES pupilos(id_pupilo) ON DELETE CASCADE
);

-- Edictos (Comunicados publicados por el tutor para su Ágora)
CREATE TABLE edictos (
    id_edicto INT AUTO_INCREMENT PRIMARY KEY,
    id_agora INT NOT NULL,
    id_tutor INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_edicto_agora FOREIGN KEY (id_agora)
        REFERENCES agoras(id_agora) ON DELETE CASCADE,
    CONSTRAINT fk_edicto_tutor FOREIGN KEY (id_tutor)
        REFERENCES tutores(id_tutor) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 4. DATOS INICIALES (HASH SHA-256 DE '1234' = 03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4)
-- ----------------------------------------------------------------------------

-- Usuarios de prueba listos para iniciar sesión en ambos roles (clave: 1234)
INSERT INTO usuarios (id_usuario, username, password_hash, rol) VALUES
(1, 'admin',     '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'tutor'),
(2, 'antonio',   '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'tutor'),
(3, 'gabriel',   '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'tutor'),
(4, 'pablo',     '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'tutor'),
(5, 'samuel',    '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'tutor'),
(6, 'fredy',     '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'tutor'),
(7, 'pupilo',    '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'pupilo'),
(8, '20250001',  '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'pupilo'),
(9, '20250002',  '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'pupilo'),
(10,'20250003',  '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'pupilo');

-- Materias transversales de tutoría
INSERT INTO materias (id_materia, codigo, nombre, area) VALUES
(1,  'MAT-101', 'Cálculo Diferencial e Integral', 'Ciencias Exactas'),
(2,  'PRG-201', 'Programación Orientada a Objetos', 'Tecnología'),
(3,  'FIS-102', 'Física Mecánica y Electromagnetismo', 'Ciencias Exactas'),
(4,  'EST-204', 'Estadística y Probabilidad Aplicada', 'Análisis Cuantitativo'),
(5,  'BDD-301', 'Diseño y Administración de Bases de Datos', 'Tecnología'),
(6,  'QUI-105', 'Química General y Bioquímica Básica', 'Ciencias de la Salud'),
(7,  'ANA-110', 'Anatomía y Fisiología Humana I', 'Ciencias de la Salud'),
(8,  'CON-202', 'Contabilidad Financiera y Costos', 'Ciencias Económicas'),
(9,  'DER-108', 'Derecho Constitucional y Teoría del Estado', 'Ciencias Jurídicas'),
(10, 'ING-103', 'Inglés Técnico y Redacción Académica', 'Humanidades');

-- Tutores / Mentores
INSERT INTO tutores (id_tutor, id_usuario, codigo_tutor, nombre, especialidad, correo) VALUES
(1, 2, 'TUT-001', 'Oscar Antonio Ramos Carbajal', 'Matemática Aplicada y Bases de Datos', 'antonio.tutor@atenea.edu.sv'),
(2, 3, 'TUT-002', 'Gabriel Alejandro Ramírez Segovia', 'Desarrollo de Interfaces y Algoritmos', 'gabriel.tutor@atenea.edu.sv'),
(3, 4, 'TUT-003', 'Pedro Pablo Trejo Guevara', 'Lógica de Programación y Arquitectura', 'pablo.tutor@atenea.edu.sv'),
(4, 5, 'TUT-004', 'Samuel Alexander Aguilar Salamanca', 'Seguridad Informática y Redes', 'samuel.tutor@atenea.edu.sv'),
(5, 6, 'TUT-005', 'Fredy Alexander Rivas Loza', 'Estadística y Ciencia de Datos', 'fredy.tutor@atenea.edu.sv'),
(6, 1, 'TUT-006', 'Dra. Elena Sofía Valenzuela', 'Ciencias Biomédicas y Química', 'elena.valenzuela@atenea.edu.sv');

-- 100 Pupilos de 12 carreras diferentes y ciclos variados (1 al 9)
INSERT INTO pupilos (id_pupilo, id_usuario, carnet, nombre, carrera, ciclo, correo) VALUES
(1,   7, '20250001', 'Valeria Alejandra Mendoza Cruz', 'Ingeniería en Sistemas y Redes Informáticas', 3, '20250001@ugb.edu.sv'),
(2,   9, '20250002', 'Carlos Eduardo Hernández López', 'Ingeniería Civil', 4, '20250002@ugb.edu.sv'),
(3,  10, '20250003', 'Sofía Beatriz Martínez Alvarado', 'Licenciatura en Enfermería', 2, '20250003@ugb.edu.sv'),
(4,  NULL, '20250004', 'Diego Fernando Castillo Rivas', 'Ingeniería Mecatrónica', 5, '20250004@ugb.edu.sv'),
(5,  NULL, '20250005', 'Camila Andrea Flores Gómez', 'Licenciatura en Psicología', 3, '20250005@ugb.edu.sv'),
(6,  NULL, '20250006', 'José Manuel Rodríguez Pineda', 'Doctorado en Medicina', 4, '20250006@ugb.edu.sv'),
(7,  NULL, '20250007', 'Natalia Gabriela Portillo Díaz', 'Inteligencia de Negocios', 2, '20250007@ugb.edu.sv'),
(8,  NULL, '20250008', 'Luis Ángel Morales Benítez', 'Ingeniería Industrial', 6, '20250008@ugb.edu.sv'),
(9,  NULL, '20250009', 'Daniela Paola Chávez Zelaya', 'Licenciatura en Ciencias Jurídicas', 3, '20250009@ugb.edu.sv'),
(10, NULL, '20250010', 'Fernando José Orellana Mejía', 'Arquitectura', 5, '20250010@ugb.edu.sv'),
(11, NULL, '20250011', 'Andrea Michelle Escobar Coreas', 'Contaduría Pública', 4, '20250011@ugb.edu.sv'),
(12, NULL, '20250012', 'Kevin Alexander Sorto Guzmán', 'Licenciatura en Administración de Empresas', 2, '20250012@ugb.edu.sv'),
(13, NULL, '20250013', 'María José Amaya Villalta', 'Ingeniería en Sistemas y Redes Informáticas', 1, '20250013@ugb.edu.sv'),
(14, NULL, '20250014', 'Bryan Steven Turcios Campos', 'Ingeniería Civil', 3, '20250014@ugb.edu.sv'),
(15, NULL, '20250015', 'Karla Vanessa Quinteros Bonilla', 'Licenciatura en Enfermería', 5, '20250015@ugb.edu.sv'),
(16, NULL, '20250016', 'Héctor Mauricio Granados Reyes', 'Ingeniería Mecatrónica', 4, '20250016@ugb.edu.sv'),
(17, NULL, '20250017', 'Paola Stefany Argueta Saravia', 'Licenciatura en Psicología', 6, '20250017@ugb.edu.sv'),
(18, NULL, '20250018', 'Rodrigo Alejandro Ventura Lemus', 'Doctorado en Medicina', 2, '20250018@ugb.edu.sv'),
(19, NULL, '20250019', 'Fátima Guadalupe Serrano Perla', 'Inteligencia de Negocios', 4, '20250019@ugb.edu.sv'),
(20, NULL, '20250020', 'Cristian David Aparicio Méndez', 'Ingeniería Industrial', 3, '20250020@ugb.edu.sv'),
(21, NULL, '20250021', 'Genesis Abigail Romero Fuentes', 'Licenciatura en Ciencias Jurídicas', 5, '20250021@ugb.edu.sv'),
(22, NULL, '20250022', 'Óscar René Guevara Palacios', 'Arquitectura', 2, '20250022@ugb.edu.sv'),
(23, NULL, '20250023', 'Brenda Lisseth Ulloa Canales', 'Contaduría Pública', 6, '20250023@ugb.edu.sv'),
(24, NULL, '20250024', 'Jonathan Isaías Alfaro Cornejo', 'Licenciatura en Administración de Empresas', 3, '20250024@ugb.edu.sv'),
(25, NULL, '20250025', 'Melany Nicole Cabrera Salgado', 'Ingeniería en Sistemas y Redes Informáticas', 4, '20250025@ugb.edu.sv'),
(26, NULL, '20250026', 'Edwin Geovanny Vásquez Blanco', 'Ingeniería Civil', 7, '20250026@ugb.edu.sv'),
(27, NULL, '20250027', 'Jocelyn Marisol Iraheta Ortiz', 'Licenciatura en Enfermería', 1, '20250027@ugb.edu.sv'),
(28, NULL, '20250028', 'dennis Javier Maldonado Ruiz', 'Ingeniería Mecatrónica', 2, '20250028@ugb.edu.sv'),
(29, NULL, '20250029', 'Tatiana Elizabeth Monge Bernal', 'Licenciatura en Psicología', 4, '20250029@ugb.edu.sv'),
(30, NULL, '20250030', 'Guillermo Enrique Barahona Sosa', 'Doctorado en Medicina', 6, '20250030@ugb.edu.sv'),
(31, NULL, '20250031', 'Astrid Carolina Sandoval Torres', 'Inteligencia de Negocios', 3, '20250031@ugb.edu.sv'),
(32, NULL, '20250032', 'Marvin Adonay Lazo Velásquez', 'Ingeniería Industrial', 5, '20250032@ugb.edu.sv'),
(33, NULL, '20250033', 'Katherine Rocío Guardado Peña', 'Licenciatura en Ciencias Jurídicas', 2, '20250033@ugb.edu.sv'),
(34, NULL, '20250034', 'César Augusto Miranda Valladares', 'Arquitectura', 4, '20250034@ugb.edu.sv'),
(35, NULL, '20250035', 'Wendy Yesenia Cruzado Melgar', 'Contaduría Pública', 3, '20250035@ugb.edu.sv'),
(36, NULL, '20250036', 'Rafael Antonio Zamora Cisneros', 'Licenciatura en Administración de Empresas', 5, '20250036@ugb.edu.sv'),
(37, NULL, '20250037', 'Estefanía Raquel Rivas Paniagua', 'Ingeniería en Sistemas y Redes Informáticas', 2, '20250037@ugb.edu.sv'),
(38, NULL, '20250038', 'Douglas Ernesto Menjívar Solís', 'Ingeniería Civil', 5, '20250038@ugb.edu.sv'),
(39, NULL, '20250039', 'Laura Patricia Cartagena Díaz', 'Licenciatura en Enfermería', 3, '20250039@ugb.edu.sv'),
(40, NULL, '20250040', 'Jorge Alberto Pacheco Lozano', 'Ingeniería Mecatrónica', 6, '20250040@ugb.edu.sv'),
(41, NULL, '20250041', 'Diana Marcela Escobar Acosta', 'Licenciatura en Psicología', 1, '20250041@ugb.edu.sv'),
(42, NULL, '20250042', 'Sebastián Andrés Campos Rivera', 'Doctorado en Medicina', 3, '20250042@ugb.edu.sv'),
(43, NULL, '20250043', 'Ximena Alejandra Toledo Najarro', 'Inteligencia de Negocios', 5, '20250043@ugb.edu.sv'),
(44, NULL, '20250044', 'Nelson Omar Berríos Quintanilla', 'Ingeniería Industrial', 2, '20250044@ugb.edu.sv'),
(45, NULL, '20250045', 'Adriana Sofía Márquez Galdámez', 'Licenciatura en Ciencias Jurídicas', 4, '20250045@ugb.edu.sv'),
(46, NULL, '20250046', 'Ricardo Vladimir Molina Chávez', 'Arquitectura', 6, '20250046@ugb.edu.sv'),
(47, NULL, '20250047', 'Claudia Lorena Sibrián Zepeda', 'Contaduría Pública', 2, '20250047@ugb.edu.sv'),
(48, NULL, '20250048', 'erick Josué Monterrosa Paredes', 'Licenciatura en Administración de Empresas', 4, '20250048@ugb.edu.sv'),
(49, NULL, '20250049', 'Lucía Fernanda Domínguez Ayala', 'Ingeniería en Sistemas y Redes Informáticas', 5, '20250049@ugb.edu.sv'),
(50, NULL, '20250050', 'Mario Roberto Santamaría Cruz', 'Ingeniería Civil', 2, '20250050@ugb.edu.sv'),
(51, NULL, '20250051', 'Rebeca Noemí Guevara Hernández', 'Licenciatura en Enfermería', 4, '20250051@ugb.edu.sv'),
(52, NULL, '20250052', 'Ángel Gabriel Salmerón Rosales', 'Ingeniería Mecatrónica', 3, '20250052@ugb.edu.sv'),
(53, NULL, '20250053', 'Mónica Isabel Alvarado Peraza', 'Licenciatura en Psicología', 5, '20250053@ugb.edu.sv'),
(54, NULL, '20250054', 'Francisco Javier Córdova Reyes', 'Doctorado en Medicina', 5, '20250054@ugb.edu.sv'),
(55, NULL, '20250055', 'Jimena Victoria Larios Pineda', 'Inteligencia de Negocios', 1, '20250055@ugb.edu.sv'),
(56, NULL, '20250056', 'Víctor Manuel Interiano Gómez', 'Ingeniería Industrial', 4, '20250056@ugb.edu.sv'),
(57, NULL, '20250057', 'Sonia Maricela Zelaya Escobar', 'Licenciatura en Ciencias Jurídicas', 6, '20250057@ugb.edu.sv'),
(58, NULL, '20250058', 'Hugo Leonardo Castellanos Pérez', 'Arquitectura', 3, '20250058@ugb.edu.sv'),
(59, NULL, '20250059', 'Verónica Lisbeth Marroquín Soto', 'Contaduría Pública', 5, '20250059@ugb.edu.sv'),
(60, NULL, '20250060', 'Sergio Armando Aguilar Romero', 'Licenciatura en Administración de Empresas', 1, '20250060@ugb.edu.sv'),
(61, NULL, '20250061', 'Camila Sofía Benítez Calderón', 'Ingeniería en Sistemas y Redes Informáticas', 6, '20250061@ugb.edu.sv'),
(62, NULL, '20250062', 'Alexis Eduardo Portillo Guzmán', 'Ingeniería Civil', 1, '20250062@ugb.edu.sv'),
(63, NULL, '20250063', 'Yolanda Beatriz Ochoa Morales', 'Licenciatura en Enfermería', 6, '20250063@ugb.edu.sv'),
(64, NULL, '20250064', 'Iván Alejandro Majano Flores', 'Ingeniería Mecatrónica', 1, '20250064@ugb.edu.sv'),
(65, NULL, '20250065', 'Priscila Abigail Navarro Mena', 'Licenciatura en Psicología', 2, '20250065@ugb.edu.sv'),
(66, NULL, '20250066', 'Mauricio Enrique Delgado Rivas', 'Doctorado en Medicina', 1, '20250066@ugb.edu.sv'),
(67, NULL, '20250067', 'Gabriela Alejandra Rivas Tobar', 'Inteligencia de Negocios', 6, '20250067@ugb.edu.sv'),
(68, NULL, '20250068', 'Wilber Stanley Corea Martínez', 'Ingeniería Industrial', 1, '20250068@ugb.edu.sv'),
(69, NULL, '20250069', 'Cecilia Guadalupe Alas Serrano', 'Licenciatura en Ciencias Jurídicas', 1, '20250069@ugb.edu.sv'),
(70, NULL, '20250070', 'Gerardo Antonio Flamenco López', 'Arquitectura', 1, '20250070@ugb.edu.sv'),
(71, NULL, '20250071', 'Silvia Roxana Cáceres Díaz', 'Contaduría Pública', 1, '20250071@ugb.edu.sv'),
(72, NULL, '20250072', 'Roberto Carlos Segovia Ortiz', 'Licenciatura en Administración de Empresas', 6, '20250072@ugb.edu.sv'),
(73, NULL, '20250073', 'Daniela Alejandra Trejo Blanco', 'Ingeniería en Sistemas y Redes Informáticas', 3, '20250073@ugb.edu.sv'),
(74, NULL, '20250074', 'Henry Oswaldo Meza Cardoza', 'Ingeniería Civil', 6, '20250074@ugb.edu.sv'),
(75, NULL, '20250075', 'Evelyn Johana Saravia Fuentes', 'Licenciatura en Enfermería', 2, '20250075@ugb.edu.sv'),
(76, NULL, '20250076', 'Alonso Rafael Henríquez Castro', 'Ingeniería Mecatrónica', 4, '20250076@ugb.edu.sv'),
(77, NULL, '20250077', 'Irene Patricia Villalobos Cruz', 'Licenciatura en Psicología', 3, '20250077@ugb.edu.sv'),
(78, NULL, '20250078', 'Saúl Ernesto Cornejo Amaya', 'Doctorado en Medicina', 7, '20250078@ugb.edu.sv'),
(79, NULL, '20250079', 'Mariana Celeste Pineda Guevara', 'Inteligencia de Negocios', 2, '20250079@ugb.edu.sv'),
(80, NULL, '20250080', 'Salvador Antonio Ramos Velásquez', 'Ingeniería Industrial', 7, '20250080@ugb.edu.sv'),
(81, NULL, '20250081', 'Elena Victoria Gallegos Bonilla', 'Licenciatura en Ciencias Jurídicas', 7, '20250081@ugb.edu.sv'),
(82, NULL, '20250082', 'Armando José Granados Lemus', 'Arquitectura', 7, '20250082@ugb.edu.sv'),
(83, NULL, '20250083', 'Norma Beatriz Sorto Méndez', 'Contaduría Pública', 7, '20250083@ugb.edu.sv'),
(84, NULL, '20250084', 'Julio César Orellana Campos', 'Licenciatura en Administración de Empresas', 7, '20250084@ugb.edu.sv'),
(85, NULL, '20250085', 'Stephany Michelle Ayala Turcios', 'Ingeniería en Sistemas y Redes Informáticas', 4, '20250085@ugb.edu.sv'),
(86, NULL, '20250086', 'Ronald Alexis Quintanilla Solís', 'Ingeniería Civil', 4, '20250086@ugb.edu.sv'),
(87, NULL, '20250087', 'Miriam Raquel Bermúdez Chávez', 'Licenciatura en Enfermería', 4, '20250087@ugb.edu.sv'),
(88, NULL, '20250088', 'Leonel Ernesto Escobar Paniagua', 'Ingeniería Mecatrónica', 5, '20250088@ugb.edu.sv'),
(89, NULL, '20250089', 'Vanessa Carolina Umanzor Díaz', 'Licenciatura en Psicología', 4, '20250089@ugb.edu.sv'),
(90, NULL, '20250090', 'Andrés Felipe Lovato Perla', 'Doctorado en Medicina', 4, '20250090@ugb.edu.sv'),
(91, NULL, '20250091', 'Karla Yamileth Meléndez Flores', 'Inteligencia de Negocios', 3, '20250091@ugb.edu.sv'),
(92, NULL, '20250092', 'René Mauricio Cañas Hernández', 'Ingeniería Industrial', 3, '20250092@ugb.edu.sv'),
(93, NULL, '20250093', 'Alejandra María Soriano López', 'Licenciatura en Ciencias Jurídicas', 3, '20250093@ugb.edu.sv'),
(94, NULL, '20250094', 'David Alejandro Parada Rivera', 'Arquitectura', 5, '20250094@ugb.edu.sv'),
(95, NULL, '20250095', 'Gloria Estefanía Renderos Sosa', 'Contaduría Pública', 4, '20250095@ugb.edu.sv'),
(96, NULL, '20250096', 'Josué Daniel Avilés Calderón', 'Licenciatura en Administración de Empresas', 2, '20250096@ugb.edu.sv'),
(97, NULL, '20250097', 'Valeria Nicolle Marín Torres', 'Ingeniería en Sistemas y Redes Informáticas', 2, '20250097@ugb.edu.sv'),
(98, NULL, '20250098', 'Cristopher Aaron Girón Peña', 'Ingeniería Civil', 3, '20250098@ugb.edu.sv'),
(99, NULL, '20250099', 'Doris Maribel Fuentes Acosta', 'Licenciatura en Enfermería', 5, '20250099@ugb.edu.sv'),
(100,NULL, '20250100', 'Emerson Javier Zepeda Morales', 'Ingeniería Mecatrónica', 3, '20250100@ugb.edu.sv');

-- Ágoras (Círculos de tutoría asignados a tutores y materias)
INSERT INTO agoras (id_agora, nombre_agora, id_tutor, id_materia, horario, cupo_maximo) VALUES
(1, 'Ágora de Pitágoras — Cálculo I', 1, 1, 'Lunes y Miércoles 14:00 - 16:00', 35),
(2, 'Ágora de Delfos — Bases de Datos Relacionales', 1, 5, 'Viernes 10:00 - 12:00', 30),
(3, 'Ágora de Apolo — Programación Orientada a Objetos', 2, 2, 'Martes y Jueves 15:00 - 17:00', 30),
(4, 'Ágora de Hefesto — Arquitectura y Lógica', 3, 2, 'Miércoles 09:00 - 11:00', 25),
(5, 'Ágora de Hermes — Seguridad y Redes', 4, 5, 'Jueves 13:00 - 15:00', 25),
(6, 'Ágora del Oráculo — Estadística Aplicada', 5, 4, 'Martes 10:00 - 12:00', 35),
(7, 'Ágora de Asclepio — Anatomía y Fisiología', 6, 7, 'Lunes y Jueves 08:00 - 10:00', 30),
(8, 'Ágora de Hipócrates — Química Biomédica', 6, 6, 'Viernes 14:00 - 16:00', 30);

-- Inscripciones de pupilos en Ágoras
INSERT INTO inscripciones_agora (id_agora, id_pupilo, fecha_inscripcion) VALUES
(1, 1, '2026-11-16'), (1, 2, '2026-11-16'), (1, 4, '2026-11-16'), (1, 8, '2026-11-16'),
(1, 10, '2026-11-16'), (1, 14, '2026-11-16'), (1, 16, '2026-11-16'), (1, 20, '2026-11-16'),
(2, 1, '2026-11-16'), (2, 7, '2026-11-16'), (2, 13, '2026-11-16'), (2, 19, '2026-11-16'),
(2, 25, '2026-11-16'), (2, 37, '2026-11-16'), (2, 49, '2026-11-16'), (2, 61, '2026-11-16'),
(3, 1, '2026-11-17'), (3, 13, '2026-11-17'), (3, 25, '2026-11-17'), (3, 37, '2026-11-17'),
(6, 5, '2026-11-17'), (6, 7, '2026-11-17'), (6, 11, '2026-11-17'), (6, 12, '2026-11-17'),
(6, 17, '2026-11-17'), (6, 19, '2026-11-17'), (6, 23, '2026-11-17'), (6, 24, '2026-11-17'),
(7, 3, '2026-11-17'), (7, 6, '2026-11-17'), (7, 15, '2026-11-17'), (7, 18, '2026-11-17'),
(7, 27, '2026-11-17'), (7, 30, '2026-11-17'), (7, 39, '2026-11-17'), (7, 42, '2026-11-17');

-- Desafíos (Tareas con buzón activo o cerrado)
INSERT INTO desafios (id_desafio, id_agora, titulo, descripcion, fecha_limite, buzon_abierto) VALUES
(1, 1, 'Desafío I: Límites y Derivadas por Definición', 'Resolver los 10 ejercicios de la guía de apoyo sobre límites indeterminados y reglas de derivación.', '2026-11-30 23:59:00', 1),
(2, 2, 'Desafío II: Normalización hasta 3FN y Modelo ER', 'Diseñar el diagrama entidad-relación de una biblioteca universitaria y normalizar sus tablas.', '2026-12-01 23:59:00', 1),
(3, 3, 'Desafío III: Encapsulamiento y Herencia en Python', 'Implementar una jerarquía de clases para figuras geométricas con métodos polimórficos.', '2026-11-29 23:59:00', 1),
(4, 6, 'Desafío IV: Distribución Normal y Muestreo', 'Calcular intervalos de confianza sobre el dataset de rendimiento académico entregado en sesión.', '2026-12-02 23:59:00', 1),
(5, 7, 'Desafío V: Sistema Osteomuscular', 'Completar el mapa conceptual de articulaciones sinoviales y principales grupos musculares.', '2026-11-24 23:59:00', 0);

-- Entregas de prueba en los buzones
INSERT INTO entregas_desafios (id_desafio, id_pupilo, contenido_entrega, enlace_recurso, calificacion, retroalimentacion) VALUES
(1, 1, 'Guía resuelta paso a paso verificando derivadas por regla de la cadena.', 'https://drive.google.com/ejemplo-calculo-valeria', 9.50, 'Excelente procedimiento y orden.'),
(1, 2, 'Ejercicios del 1 al 10 resueltos en formato PDF.', 'https://drive.google.com/ejemplo-calculo-carlos', 8.80, 'Revisar el signo en el ejercicio 7.'),
(2, 1, 'Script SQL y diagrama normalizado en 3FN adjunto.', 'https://github.com/ejemplo/bd-normalizacion', 10.00, 'Esquema limpio y sin redundancias.'),
(2, 7, 'Modelo entidad-relación y diccionario de datos.', 'https://drive.google.com/ejemplo-bd-natalia', 9.00, 'Buen manejo de llaves foráneas.'),
(5, 3, 'Mapa conceptual completo del sistema locomotor.', 'https://drive.google.com/ejemplo-anatomia-sofia', 9.20, 'Muy buena síntesis.');

-- Registros de asistencia
INSERT INTO asistencias (id_agora, id_pupilo, fecha_sesion, estado, observacion) VALUES
(1, 1, '2026-11-18', 'Presente', 'Participó resolviendo ejercicios en pizarra'),
(1, 2, '2026-11-18', 'Presente', NULL),
(1, 4, '2026-11-18', 'Tardanza', 'Ingresó 10 minutos tarde'),
(1, 8, '2026-11-18', 'Ausente', 'Justificó cruce con laboratorio'),
(2, 1, '2026-11-20', 'Presente', NULL),
(2, 7, '2026-11-20', 'Presente', NULL),
(2, 13, '2026-11-20', 'Presente', NULL),
(7, 3, '2026-11-19', 'Presente', NULL),
(7, 6, '2026-11-19', 'Ausente', NULL);

-- Edictos (Comunicados publicados por los tutores)
INSERT INTO edictos (id_agora, id_tutor, titulo, mensaje) VALUES
(1, 1, 'Bienvenida al Ágora de Pitágoras', 'Iniciados: recuerden traer su guía de derivadas impresa o digital para la sesión de refuerzo previa al parcial.'),
(2, 1, 'Habilitación de Buzón — Normalización SQL', 'Ya se encuentra abierto el buzón del Desafío II. Suban el enlace a su script SQL antes de la fecha límite.'),
(7, 6, 'Cierre de Buzón — Sistema Osteomuscular', 'El buzón del Desafío V ha cerrado. Revisen su retroalimentación en el panel.');