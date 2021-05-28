from fingerprint_compare import FingerprintCompare


def lambda_handler(event, context):
    weights = event.get("weights") or None
    comparer = FingerprintCompare(event["previous_fingerprints"], event["new_fingerprint"], weights)
    similarity, results = comparer.identify_top_fingerprint_match()

    return {
        "statusCode": 200,
        "body": {"match_results": results, "match_score": 100 * round(similarity, 4)},
    }
