import sqlite3
import logging

logger = logging.getLogger('db interface-')


def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cases (
            user_id TEXT PRIMARY KEY,
            case_status TEXT,
            case_details TEXT,
            documents TEXT
        )
        """
    )
    sample_data = [
        ("stargazer94", "Open", "Property transfer in progress", "contract.pdf"),
        ("pulsar342", "Closed", "Case resolved successfully", "closure_report.pdf"),
        ("martianspider876", "Pending", "Awaiting client documents", ""),
        ("nebulaRider99", "Open", "Mortgage approval in progress", "mortgage_details.pdf"),
        ("cosmicTrail88", "Closed", "Property sale completed", "sale_deed.pdf"),
        ("quasarHunter777", "Pending", "Verification of ownership documents", "ownership_proof.pdf"),
        ("solarFlare123", "Open", "Land registry in progress", "land_registry.pdf"),
        ("galaxySeeker47", "Closed", "Case resolved with compensation", "compensation_details.pdf"),
        ("orbitWatcher56", "Pending", "Awaiting payment confirmation", "payment_receipt.pdf"),
        ("starForge22", "Open", "Title deed processing", "title_deed.pdf"),
        ("lunarEcho789", "Closed", "Property dispute resolved", "dispute_resolution.pdf"),
        ("planetSurfer101", "Pending", "Client response required", "client_request.pdf"),
        ("cometChaser333", "Open", "Legal review ongoing", "legal_review.pdf"),
        ("asteroidHopper66", "Closed", "Conveyancing completed successfully", "completion_certificate.pdf"),
        ("cosmosNavigator55", "Pending", "Approval from authorities required", "authority_approval.pdf")
    ]
    cursor.executemany("INSERT OR IGNORE INTO cases (user_id, case_status, case_details, documents) VALUES (?, ?, ?, ?)", sample_data)
    conn.commit()
    conn.close()

def display_all_data():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases")
    rows = cursor.fetchall()
    conn.close()
    if rows:
        print("User ID\t\tCase Status\tCase Details\t\tDocuments")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
    else:
        print("No data found in the database.")

def fetch_case_information(user_id):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        logger.info("Results success.")
        return result
    else:
        result = "No case updates found for this user ID."
        logger.warning(result)
        return result
