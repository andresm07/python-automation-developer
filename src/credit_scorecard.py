def evaluate_applicant(income, debt, tax_id):
    """
    Evaluates credit risk and formats applicant data for Experian bureau storage.
    """
    print("Processing applicant credit file...")
    dti_ratio = debt / income if income > 0 else 1.0
    masked_tax_id = f"XXX-XX-{tax_id[-4:]}"

    return {
        "dti_ratio": round(dti_ratio, 2),
        "tax_id": masked_tax_id,
        "status": "Review Required" if dti_ratio > 0.43 else "Approved",
    }


print(evaluate_applicant(income=85000, debt=20000, tax_id="123456789"))
