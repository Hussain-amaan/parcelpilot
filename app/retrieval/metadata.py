from pathlib import Path


DOCUMENT_METADATA = {
    "01_Support_Policy_v3_CURRENT.pdf": {
        "document_type": "support_policy",
        "status": "CURRENT",
        "account_id": None,
        "priority": 2
    },

    "02_Support_Policy_v2_DEPRECATED.pdf": {
        "document_type": "support_policy",
        "status": "DEPRECATED",
        "account_id": None,
        "priority": 4
    },

    "03_Cancellation_and_Service_Credit_SOP_v4.pdf": {
        "document_type": "cancellation_service_credit_sop",
        "status": "CURRENT",
        "account_id": None,
        "priority": 2
    },

    "04_Product_Operations_Guide_and_Known_Issues.pdf": {
        "document_type": "product_operations",
        "status": "CURRENT",
        "account_id": None,
        "priority": 3
    },

    "05_Northstar_Logistics_Enterprise_Agreement.pdf": {
        "document_type": "customer_agreement",
        "status": "ACTIVE",
        "account_id": "ACCT-001",
        "priority": 1
    },

    "06_LumenWorks_Service_Agreement.pdf": {
        "document_type": "customer_agreement",
        "status": "ACTIVE",
        "account_id": "ACCT-002",
        "priority": 1
    }
}


def get_metadata(filename):
    return DOCUMENT_METADATA.get(filename)