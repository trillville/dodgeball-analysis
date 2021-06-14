from visitor_attribute_compare import VisitorAttributeCompare


def lambda_handler(event, context):
    weights = event.get("weights") or None
    comparer = VisitorAttributeCompare(event["previous_visitors"], event["new_visitor"], weights)
    results = comparer.estimate_visitor_match()

    return {
        "statusCode": 200,
        "body": {
            "match_score": results["score"],
            "ip_timing_red_flag": results["ip_timing_red_flag"],
        },
    }
