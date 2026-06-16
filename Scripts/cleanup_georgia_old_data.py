import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

# Old 2022 candidates to DELETE
old_candidates = [
    'b084bf28-d0a6-4d32-a11e-2606bfcb164a',  # Herschel Walker (2022 Senate)
    'fe7fb12d-65cb-435d-96a6-c88abfa93690',  # Brian Kemp (2022 Governor)
    '03b8e4a3-4219-4785-b5a9-77230cd4a392',  # Stacey Abrams (2022 Governor)
    'b9e817e2-4a69-4020-bea3-f1c95d733d3d',  # Jon Ossoff (2022 Senate)
    '43b729d0-1b85-4926-a993-8f1a9e54d790',  # Burt Jones (duplicate)
    'd3c6c2ec-93ac-4a45-874f-785cc6af4059',  # Brad Raffensperger (2022)
    '32df3cde-53eb-4c8e-88f9-9e250a4730c5',  # Andre Dickens (2021 Mayor)
    'b5bc18bc-7804-4bc2-9aa1-05db2e0b4b28',  # Antonio Brown (2021 Mayor)
    'b9ad8702-0751-4c86-b5d3-f5fb54da536d',  # Courtney English (2021 Mayor)
    '07f668dc-e13e-4b1e-a133-8115006258be',  # Sharon Gay (2021 Mayor)
    'cc57eac4-cea4-4ad5-a7de-7f2156580741',  # khalid kamau (2021 Mayor)
    '9898b694-fcc0-484f-a7e0-b0147b7d6048',  # Alicia Johnson (2022 PSC)
    '89b09e8d-c1ad-432c-a8fe-06a7656a7bfe',  # Fitz Johnson (2022 PSC)
    '08386702-3767-4192-97fd-0cdfaa07d5c0',  # Jason Shaw (2022 PSC)
    'a154e503-1132-43b0-b42f-d06767eb4681',  # Peter Hubbard (2022 PSC)
    '4db19192-a21b-4475-8872-c76a2cf4ed59',  # Lauren McDonald (2022 PSC)
    '97a22568-5d07-42d3-85bc-9c6abd6a67ab',  # Tim Echols (2022 PSC)
    '2cb9fff8-3fad-49cd-a87d-e78b1a4101a1',  # Karin Faulkner (2022 BOE)
    '885a2ab0-5a4c-4683-94e6-4f991bbf75f5',  # Rich McCormick (2022 House)
    'dfc12e42-bd1a-47f9-9678-8ca86b12c8ec',  # Andrew Clyde (2022 House)
    'herschel-walker-ga-sen-2026',  # Herschel Walker duplicate
    'stacey-abrams-ga-gov-2026',  # Stacey Abrams (not running 2026)
]

print(f"Deleting {len(old_candidates)} old 2022 candidates...\n")

for candidate_id in old_candidates:
    try:
        candidates_table.delete_item(Key={'candidate_id': candidate_id})
        print(f"Deleted: {candidate_id}")
    except Exception as e:
        print(f"Error deleting {candidate_id}: {e}")

print(f"\nCleanup complete! Deleted {len(old_candidates)} old candidates")
