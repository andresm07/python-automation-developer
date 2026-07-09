# --- EXPERIAN SIMULATED MESSY INPUT ---
# Problem 1: Name contains "MojÃ­ca" instead of "Mojíca" due to a UTF-8/Latin-1 mismatch.
# Problem 2: SSN has accidental spaces and a trailing tab '\t'.
raw_credit_input = (
    "   \t  Alejandro Moj\u00c3\u00adca  |  555 - 01 - 9999   \t"
)

# --- STEP 1: Normalize the Encoding & Split Data ---
# Extracting the raw chunks first by splitting on the pipe '|'
information = raw_credit_input.split("|")

raw_name = information[0]
raw_ssn = information[1]

# Fix the encoding artifact in the name ("MojÃ­ca" -> "Mojíca")
fixed_name = raw_name.encode("latin1").decode("utf-8")

# --- STEP 2: Clean Leading/Trailing Whitespace & Formatting ---
# Strip the edges of the name
clean_name = fixed_name.strip()

# Strip the SSN, and remove internal spaces to standardize the format
clean_ssn = raw_ssn.strip().replace(" ", "")

# --- STEP 3: Format into Standard Experian Bureau Output ---
# We mask the first 5 digits of the SSN for data security (FCRA compliance)
masked_ssn = f"XXX-XX-{clean_ssn[-4:]}"
account_status = "verified"

bureau_fstring_record = f"STATUS: [{account_status.upper()}] | consumer: {clean_name} | SSN: {masked_ssn}"

# --- VERIFY THE BUREAU DATA ---
print("--- Experian Data Ingestion Process ---")
print(f"Raw Input:      {raw_credit_input}")
print(f"Bureau Record:  {bureau_fstring_record}")

"""
EXPECTED OUTCOME:

--- Experian Data Ingestion Process ---
Raw Input:         	  Alejandro MojÃ­ca  |  555 - 01 - 9999   	
Bureau Record:  STATUS: [VERIFIED] | consumer: Alejandro Mojíca | SSN: XXX-XX-9999
"""
