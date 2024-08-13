-- Drop the 'description' column from the 'locations' table
ALTER TABLE location
DROP COLUMN description;

-- Drop the 'test' table if it exists
DROP TABLE IF EXISTS test;

-- Drop the 'working_hours' column from the 'locations' table
ALTER TABLE location
DROP COLUMN working_hours;

-- Add 'working_hours_start' and 'working_hours_end' columns to the 'locations' table
ALTER TABLE location
ADD COLUMN working_hours_start VARCHAR(5) NOT NULL,
ADD COLUMN working_hours_end VARCHAR(5) NOT NULL;
