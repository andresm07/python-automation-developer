from credit_scorecard import evaluate_applicant


def test_success_evaluate_applicant():
    assert evaluate_applicant(85000, 30000, "123456789") == {
        "dti_ratio": 0.35,
        "tax_id": "XXX-XX-6789",
        "status": "Approved",
    }
    assert evaluate_applicant(85000, 20000, "123456789") == {
        "dti_ratio": 0.24,
        "tax_id": "XXX-XX-6789",
        "status": "Approved",
    }


def test_failed_evaluate_applicant():
    assert evaluate_applicant(85000, 20000, "123456789") != {
        "dti_ratio": 0.35,
        "tax_id": "XXX-XX-6789",
        "status": "Approved",
    }
