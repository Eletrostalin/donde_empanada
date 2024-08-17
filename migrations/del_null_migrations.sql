-- Удаление ограничения NOT NULL для поля rating
ALTER TABLE review ALTER COLUMN rating DROP NOT NULL;

-- Удаление ограничения NOT NULL для поля comment
ALTER TABLE review ALTER COLUMN comment DROP NOT NULL;

-- Изменение типа данных для поля comment на TEXT с ограничением в 5000 символов
ALTER TABLE review ALTER COLUMN comment TYPE TEXT USING comment::TEXT;