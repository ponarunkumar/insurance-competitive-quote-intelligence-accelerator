-- ============================================================================
-- Insurance Competitive Quote Intelligence — Azure SQL Seed Script
-- ============================================================================
-- Run this against the Azure SQL database after provisioning
-- Creates the operational data store schema and loads sample data
-- ============================================================================

-- Rate History (for pricing variance calculations)
CREATE TABLE rate_history (
    id INT IDENTITY(1,1) PRIMARY KEY,
    product_type NVARCHAR(100) NOT NULL,
    territory NVARCHAR(50) NOT NULL,
    period_year INT NOT NULL,
    period_quarter INT NOT NULL,
    avg_premium DECIMAL(12,2),
    median_premium DECIMAL(12,2),
    loss_ratio DECIMAL(5,4),
    target_rate DECIMAL(12,2),
    sample_size INT,
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Competitor Quotes (stored after collection)
CREATE TABLE competitor_quotes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    submission_id NVARCHAR(50) NOT NULL,
    carrier NVARCHAR(100) NOT NULL,
    annual_premium_gross DECIMAL(12,2),
    annual_premium_net DECIMAL(12,2),
    commission_percent DECIMAL(5,2),
    per_occurrence_limit DECIMAL(15,2),
    aggregate_limit DECIMAL(15,2),
    deductible DECIMAL(12,2),
    coverage_form NVARCHAR(50),
    collected_at DATETIME2 DEFAULT GETDATE()
);

-- Advisor Performance (for coaching reports)
CREATE TABLE advisor_performance (
    id INT IDENTITY(1,1) PRIMARY KEY,
    advisor_id NVARCHAR(50) NOT NULL,
    period NVARCHAR(20) NOT NULL,
    policies_written INT DEFAULT 0,
    premium DECIMAL(12,2) DEFAULT 0,
    quality_score DECIMAL(5,2) DEFAULT 0,
    conversion_rate DECIMAL(5,4) DEFAULT 0,
    avg_handle_time_seconds INT DEFAULT 0,
    calls_handled INT DEFAULT 0,
    recorded_at DATETIME2 DEFAULT GETDATE()
);

-- Call Analytics (from speech processing)
CREATE TABLE call_analytics (
    id INT IDENTITY(1,1) PRIMARY KEY,
    advisor_id NVARCHAR(50) NOT NULL,
    call_id NVARCHAR(100),
    call_date DATETIME2 NOT NULL,
    quality_score DECIMAL(5,2),
    sentiment_avg DECIMAL(3,2),
    insights NVARCHAR(MAX),
    compliance_flags NVARCHAR(MAX),
    handle_time_seconds INT,
    created_at DATETIME2 DEFAULT GETDATE()
);

-- HITL Approvals Audit Log
CREATE TABLE approval_audit (
    id INT IDENTITY(1,1) PRIMARY KEY,
    submission_id NVARCHAR(50) NOT NULL,
    recommendation_type NVARCHAR(20) NOT NULL,
    adjustment_percent DECIMAL(5,2),
    approver_id NVARCHAR(50),
    decision NVARCHAR(20) NOT NULL,  -- APPROVED, REJECTED, MODIFIED
    decision_timestamp DATETIME2 DEFAULT GETDATE(),
    rationale NVARCHAR(MAX),
    compliance_checks_passed BIT DEFAULT 1
);

-- ============================================================================
-- SEED DATA
-- ============================================================================

-- Sample rate history
INSERT INTO rate_history (product_type, territory, period_year, period_quarter, avg_premium, median_premium, loss_ratio, target_rate, sample_size) VALUES
('commercial_general_liability', 'UK', 2025, 4, 8750.00, 8500.00, 0.5200, 9000.00, 150),
('commercial_general_liability', 'UK', 2026, 1, 8900.00, 8600.00, 0.5100, 9100.00, 165),
('commercial_general_liability', 'UK', 2026, 2, 9100.00, 8800.00, 0.4900, 9200.00, 172);

-- Sample advisor performance
INSERT INTO advisor_performance (advisor_id, period, policies_written, premium, quality_score, conversion_rate, avg_handle_time_seconds, calls_handled) VALUES
('ADV-001', 'this_week', 12, 45000.00, 82.5, 0.3200, 480, 38),
('ADV-002', 'this_week', 8, 32000.00, 91.0, 0.2800, 420, 29),
('ADV-003', 'this_week', 15, 58000.00, 78.0, 0.3500, 540, 43),
('ADV-004', 'this_week', 6, 21000.00, 88.5, 0.2200, 390, 27);
