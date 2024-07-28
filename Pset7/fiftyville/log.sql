-- Keep a log of any SQL queries you execute as you solve the mystery.
-- While my queries may seem repetitive, I have made sure to do a step by step process to ensure long multiple inner join queries work through each addition to my process. Hope you keep this in mind
-- when grading me on design.


-- Reason: To learn basic information about the crime.
SELECT description FROM crime_scene_reports
    WHERE day = 28 AND month = 7
    AND street = 'Humphrey Street';
-- Learning: Theft at 10:15am at Bakery. Interviews of 3 witnesses mention bakery.


-- Reason: To read witness statements.
SELECT name, transcript FROM interviews
    WHERE transcript LIKE '%Bakery%';
-- Learning:
-- 1. Thief fled in a car between 10:15 - 10:25am. Car was parked at the bakery parking lot.
-- 2. Earlier that morning (28 July), thief withdrew cash from ATM at Leggett Street.
-- 3. After theft, thief called acomplice on phone for about a minute. thief asked acomplice to buy earliest flight out of fiftyville for next day (29 July).

-- Reason: Identify owner of thief's car using license plate
SELECT license_plate FROM bakery_security_logs
    WHERE day = 28 AND month = 7
    AND hour = 10
    AND minute BETWEEN 15 AND 25;
-- Learning: List of suspect license plates now available to us

-- Reason: Identify thief through atm transaction
SELECT account_number FROM atm_transactions
    WHERE month = 7 AND day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw';
-- Learning: List of suspect account numbers now available to us


-- Reason: Compare suspect account numbers and license plates
SELECT people.id FROM people
    INNER JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate
        AND bakery_security_logs.day = 28 AND bakery_security_logs.month = 7
        AND bakery_security_logs.hour = 10
        AND bakery_security_logs.minute BETWEEN 15 AND 25

    INNER JOIN bank_accounts, atm_transactions
    ON bank_accounts.person_id = people.id AND bank_accounts.account_number = atm_transactions.account_number
        AND atm_transactions.month = 7 AND atm_transactions.day = 28
        AND atm_transactions.atm_location = 'Leggett Street'
        AND atm_transactions.transaction_type = 'withdraw';
-- Learning: Final suspects list for thief now available to us



-- Reason: Identify thief through phone records and thief suspect list
SELECT people.id, people.name FROM people
        INNER JOIN bakery_security_logs
        ON people.license_plate = bakery_security_logs.license_plate
            AND bakery_security_logs.day = 28 AND bakery_security_logs.month = 7
            AND bakery_security_logs.hour = 10
            AND bakery_security_logs.minute BETWEEN 15 AND 25

        INNER JOIN bank_accounts, atm_transactions
        ON people.id = bank_accounts.person_id AND bank_accounts.account_number = atm_transactions.account_number
            AND atm_transactions.month = 7 AND atm_transactions.day = 28
            AND atm_transactions.atm_location = 'Leggett Street'
            AND atm_transactions.transaction_type = 'withdraw'

        INNER JOIN phone_calls
        ON people.phone_number = phone_calls.caller
            AND phone_calls.duration <= 60
            AND phone_calls.day = 28
            AND phone_calls.month = 7;
-- Learning: Thief narrowed down to two suspects


-- Reason: Identify theif through flight
SELECT people.id, people.name FROM people
        INNER JOIN bakery_security_logs
        ON people.license_plate = bakery_security_logs.license_plate
            AND bakery_security_logs.day = 28 AND bakery_security_logs.month = 7
            AND bakery_security_logs.hour = 10
            AND bakery_security_logs.minute BETWEEN 15 AND 25

        INNER JOIN bank_accounts, atm_transactions
        ON people.id = bank_accounts.person_id AND bank_accounts.account_number = atm_transactions.account_number
            AND atm_transactions.month = 7 AND atm_transactions.day = 28
            AND atm_transactions.atm_location = 'Leggett Street'
            AND atm_transactions.transaction_type = 'withdraw'

        INNER JOIN phone_calls
        ON people.phone_number = phone_calls.caller
            AND phone_calls.duration <= 60
            AND phone_calls.day = 28
            AND phone_calls.month = 7

        INNER JOIN passengers, flights
        ON passengers.passport_number = people.passport_number
            AND flights.id = passengers.flight_id
            AND flights.day = 29 AND flights.month = 7
            AND flights.origin_airport_id = 8
            ORDER BY flights.hour, flights.minute
            LIMIT 1;
-- Learning: Thief concluded to be Bruce (ID: 686048)


-- Reason: Identify acomplice through thief and phone call
SELECT people.id, people.name FROM people
    INNER JOIN people as thief
    ON thief.id = 686048

    INNER JOIN phone_calls
        ON people.phone_number = phone_calls.receiver
            AND phone_calls.duration <= 60
            AND phone_calls.day = 28
            AND phone_calls.month = 7
            AND phone_calls.caller = thief.phone_number;
-- Learning: Acomplice concluded to be Robin (ID: 864400)


-- Reason: Finding city thief escaped to
SELECT airports.city FROM airports
       INNER JOIN flights
        ON flights.destination_airport_id = airports.id
            AND flights.day = 29 AND flights.month = 7
            AND flights.origin_airport_id = 8

            ORDER BY flights.hour, flights.minute
            LIMIT 1;
-- Learning: Escaped city confirmed as New York City




