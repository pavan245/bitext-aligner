-- MySQL Script generated by MySQL Workbench
-- Wed Jan 22 11:08:37 2020
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bitext_aligner
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `bitext_aligner` ;

-- -----------------------------------------------------
-- Schema bitext_aligner
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bitext_aligner` DEFAULT CHARACTER SET utf8;
USE `bitext_aligner` ;

-- -----------------------------------------------------
-- Table `bitext_aligner`.`dim_author`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bitext_aligner`.`dim_author` ;

CREATE TABLE IF NOT EXISTS `bitext_aligner`.`dim_author` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(90) NOT NULL,
  `total_books` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bitext_aligner`.`dim_book`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bitext_aligner`.`dim_book` ;

CREATE TABLE IF NOT EXISTS `bitext_aligner`.`dim_book` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(90) NOT NULL,
  `added_at` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bitext_aligner`.`dim_book_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bitext_aligner`.`dim_book_info` ;

CREATE TABLE IF NOT EXISTS `bitext_aligner`.`dim_book_info` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(90) NOT NULL,
  `description` VARCHAR(500) NULL,
  `lang` VARCHAR(5) NOT NULL,
  `source` VARCHAR(90) NOT NULL,
  `is_translation` TINYINT NOT NULL,
  `total_chapters` INT UNSIGNED NOT NULL,
  `isbn` VARCHAR(80) NULL,
  `book` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `book_fk_idx` (`book` ASC),
  UNIQUE INDEX `book_UNIQUE` (`book` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `info_book_fk`
    FOREIGN KEY (`book`)
    REFERENCES `bitext_aligner`.`dim_book` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bitext_aligner`.`dim_book_content`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bitext_aligner`.`dim_book_content` ;

CREATE TABLE IF NOT EXISTS `bitext_aligner`.`dim_book_content` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `book` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `book_fk_idx` (`book` ASC),
  UNIQUE INDEX `book_UNIQUE` (`book` ASC),
  CONSTRAINT `content_book_fk`
    FOREIGN KEY (`book`)
    REFERENCES `bitext_aligner`.`dim_book` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bitext_aligner`.`dim_book_chapter`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bitext_aligner`.`dim_book_chapter` ;

CREATE TABLE IF NOT EXISTS `bitext_aligner`.`dim_book_chapter` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `c_num` INT UNSIGNED NOT NULL,
  `name` VARCHAR(90) NULL,
  `book_content` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `content_fk_idx` (`book_content` ASC),
  CONSTRAINT `ch_content_fk`
    FOREIGN KEY (`book_content`)
    REFERENCES `bitext_aligner`.`dim_book_content` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bitext_aligner`.`dim_book_sentence`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bitext_aligner`.`dim_book_sentence` ;

CREATE TABLE IF NOT EXISTS `bitext_aligner`.`dim_book_sentence` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `s_num` INT UNSIGNED NOT NULL,
  `text` VARCHAR(1499) NOT NULL,
  `chapter` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `chapter_fk_idx` (`chapter` ASC),
  CONSTRAINT `sen_chapter_fk`
    FOREIGN KEY (`chapter`)
    REFERENCES `bitext_aligner`.`dim_book_chapter` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bitext_aligner`.`map_book_author`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bitext_aligner`.`map_book_author` ;

CREATE TABLE IF NOT EXISTS `bitext_aligner`.`map_book_author` (
  `author` INT NOT NULL,
  `book` INT NOT NULL,
  `translator` TINYINT NOT NULL,
  INDEX `book_fk_idx` (`book` ASC) ,
  INDEX `author_fk_idx` (`author` ASC),
  CONSTRAINT `map_book_fk`
    FOREIGN KEY (`book`)
    REFERENCES `bitext_aligner`.`dim_book_info` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `map_author_fk`
    FOREIGN KEY (`author`)
    REFERENCES `bitext_aligner`.`dim_author` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
