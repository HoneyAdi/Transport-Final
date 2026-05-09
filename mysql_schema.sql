-- MySQL Schema for Transport Management System
-- Generated: May 9, 2026
-- Database: transport_db

-- Transport Bills Table (with gr_date column)
CREATE TABLE IF NOT EXISTS transport_bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT,
    name VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Versioning fields
    parent_id INT,
    version_number INT DEFAULT 1,
    is_original TINYINT(1) DEFAULT 1,
    modification_reason TEXT,
    
    -- Essential fields
    gr_number VARCHAR(50),
    gr_date DATE,
    `date` DATE DEFAULT (CURRENT_DATE),
    challan_number VARCHAR(50),
    party_information VARCHAR(100),
    location_id INT,
    rate INT DEFAULT 0,
    delivery_type_id INT,
    vehicle_id INT,
    status VARCHAR(30) DEFAULT 'booked',
    
    -- Extended data (JSON stored as TEXT)
    extended_data TEXT,
    
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_parent_id (parent_id),
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_location_id (location_id),
    INDEX idx_status (status),
    INDEX idx_gr_number (gr_number),
    INDEX idx_date (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Migration: Add gr_date column if it doesn't exist (for existing databases)
SET @col_exists = (
    SELECT COUNT(*) FROM information_schema.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'transport_bills' 
    AND COLUMN_NAME = 'gr_date'
);

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE transport_bills ADD COLUMN gr_date DATE AFTER gr_number', 
    'SELECT "gr_date column already exists" as message'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
