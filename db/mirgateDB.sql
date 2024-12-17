INSERT INTO OpenBank_ver02.users (id, username, FIO, balance, is_banned, is_org)
SELECT id, username, FIO, balance, is_banned, is_org
FROM OpenBank_ver01.users;

-- Миграция данных transactions
INSERT INTO OpenBank_ver02.transactions (id, sender_id, recipient_id, transaction_datetime, amount)
SELECT id, sender_id, recipient_id, transaction_datetime, amount
FROM OpenBank_ver01.transactions;

-- Миграция данных credit_requests
INSERT INTO OpenBank_ver02.credit_requests (id, user_id, purpose, status, amount)
SELECT id, user_id, purpose, status, amount
FROM OpenBank_ver01.creditRequests;

-- Миграция данных taxes
INSERT INTO OpenBank_ver02.taxes (id, name, due_datetime, amount)
SELECT id, name, due_datetime, amount
FROM OpenBank_ver01.taxes;

-- Миграция данных tax_payments
INSERT INTO OpenBank_ver02.tax_payments (id, user_id, tax_id, payment_datetime, amount)
SELECT id, user_id, tax_id, payment_datetime, amount
FROM OpenBank_ver01.taxesPayments;