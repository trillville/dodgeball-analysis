from utils import (
    haversine_distance,
    timestamp_difference,
    exact_match,
    age_difference,
    generate_match_score,
    edit_distance,
)


class VisitorAttributeCompare:
    """
    Given a visitor profile and a set of previous candidate visitor profiles,
    identify whether or not they likely belong to the same individual
    """

    def __init__(self, prev_vs=[], new_v=None, weights=None):
        self.prev_vs = prev_vs  # all previous visitors to compare
        self.new_v = new_v  # new visitor (occurred later)
        self.weights = weights  # optional dictionary indicating weights for similarity attributes
        self.MAX_PLAUSIBLE_SPEED = 0.35  # passenger jet cruising speed (in km/s) + 20%

    def match_telemetry(self):
        """
        Match visitors telemetry fields
        :return score: calculated telemetry score based on all attributes
        :return ip_timing_red_flag: True if IP timing/geographic location values indicate it can't
                                    be the same person
        """
        ip_timing_red_flag = False
        match_scores = []
        for prev_v in self.prev_vs:
            distance_scores, ip_matches = [], []
            for previous_ip_data in prev_v["ips"]:
                for new_ip_data in self.new_v["ips"]:
                    distance = haversine_distance(previous_ip_data["props"], new_ip_data["props"])
                    time_delta = timestamp_difference(
                        previous_ip_data["updated_at"], new_ip_data["updated_at"]
                    )
                    ip_matches.append(exact_match(previous_ip_data["ip"], new_ip_data["ip"]))
                    if distance > 10 and (distance / time_delta) > self.MAX_PLAUSIBLE_SPEED:
                        ip_timing_red_flag = True
                    elif distance < 10:
                        distance_scores.append(1)
                    else:
                        distance_scores.append(min(1000, distance) / 1000)

            results = {
                "ip_match": max(ip_matches),
                "geographic_proximity": 1
                - (sum(distance_scores) / len(distance_scores)),  # average distance score
                "creation_time_proximity": 1
                - min(
                    1,
                    timestamp_difference(
                        prev_v["visitors"]["createdAt"], self.new_v["visitors"]["createdAt"]
                    )
                    / 86400,  # seconds in a day
                ),
                "visitor_age_proximity": 1
                - age_difference(
                    prev_v["visitors"]["createdAt"], self.new_v["visitors"]["createdAt"]
                ),
            }

            match_scores.append(generate_match_score(results, self.weights["telemetry"]))

        return {"score": max(match_scores), "ip_timing_red_flag": ip_timing_red_flag}

    def match_payment(self):
        """
        Match visitors payment fields. If both visitors have globally unique payment
        fingerprints, just compare those. Otherwise, match all fields (including fingerprint)
        :return score: calculated payment similarity score based on all attributes
        """
        match_scores = []
        new_payment = self.new_v["payment_methods"]
        for prev_v in self.prev_vs:
            prev_payment = prev_v["payment_methods"]
            if (
                prev_payment["fingerprint"]
                and new_payment["fingerprint"]
                and prev_payment["global_unique_fingerprint"]
                and new_payment["global_unique_fingerprint"]
            ):
                match_scores.append(
                    exact_match(prev_payment["fingerprint"], new_payment["fingerprint"])
                )
                break
            else:
                for field in ["brand", "expMonth", "expYear", "last4", "country"]:
                    if (
                        not prev_payment[field]
                        or not new_payment[field]
                        or not (prev_payment[field] == new_payment[field])
                    ):
                        match_scores.append(0)
                        break
                if prev_payment["fingerprint"] and new_payment["fingerprint"]:
                    match_scores.append(
                        exact_match(prev_payment["fingerprint"], new_payment["fingerprint"])
                    )
        return max(match_scores) * self.weights["payment_methods"]

    def match_address(self):
        """
        Match visitors address fields.
        :return score: calculated address similarity score based on all attributes
        """
        new_address = self.new_v["visitor_addresses"]
        match_scores = []
        for prev_v in self.prev_vs:
            prev_address = prev_v["visitor_addresses"]
            results = {
                "Line1": 1.0 - edit_distance(prev_address["Line1"], new_address["Line1"]),
                "Line2": 1.0 - edit_distance(prev_address["Line2"], new_address["Line2"]),
                "City": exact_match(prev_address["City"], new_address["City"]),
                "Country": exact_match(prev_address["Country"], new_address["Country"]),
                "Postal_code": exact_match(prev_address["Postal_code"], new_address["Postal_code"]),
                "State": exact_match(prev_address["State"], new_address["State"]),
            }

            match_scores.append(generate_match_score(results, self.weights["visitor_addresses"]))

        return max(match_scores)

    def match_identity_information(self):
        """
        Match visitors identification fields.
        :return score: calculated address similarity score based on all attributes
        """
        new_id = self.new_v["visitor_users"]
        match_scores = []
        for prev_v in self.prev_vs:
            prev_id = prev_v["visitor_users"]
            results = {
                "email": exact_match(new_id["email"], prev_id["email"]),
                "Phone": exact_match(new_id["Phone"], prev_id["Phone"]),
                "First_name": exact_match(new_id["First_name"], prev_id["First_name"]),
                "Last_name": exact_match(new_id["Last_name"], prev_id["Last_name"]),
                "username": exact_match(new_id["username"], prev_id["username"]),
            }

            match_scores.append(generate_match_score(results, self.weights["visitor_users"]))

        return max(match_scores)

    def estimate_visitor_match(self):
        """
        Return overall match score, return the IP timing red flag as a separate field
        to be used in downstream logic
        :return score: Overall visitor similarity score based on attributes they entered
        :return ip_timing_red_flag: True if IP timing/geographic location values indicate it can't
                                    be the same person
        """
        all_results = {
            "telemetry": self.match_telemetry(),
            "payment_methods": self.match_payment(),
            "visitor_users": self.match_identity_information(),
            "visitor_addresses": self.match_address(),
        }
        score = (
            all_results["telemetry"]["score"]
            + all_results["payment_methods"]
            + all_results["visitor_users"]
            + all_results["visitor_addresses"]
        )

        return {
            "score": min(100, score),
            "ip_timing_red_flag": all_results["telemetry"]["ip_timing_red_flag"],
        }
