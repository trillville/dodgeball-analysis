from utils import exact_match, asymmetric_match, match_set, less_than_or_equal


class FingerprintCompare:
    """
    Given a browser fingerprint hashse and a set of previous candidate fingerprints,
    identify whether or not they likely belong to the same individual
    """

    def __init__(self, prev_fps=[], new_fingerprint=None, weights=None):
        self.prev_fps = prev_fps  # all previous fingerprints to compare
        self.new_fp = new_fingerprint  # second fingerprint (occurred later)
        self.weights = weights  # optional dictionary indicating weights for similarity attributes

    def estimate_fingerprint_match(self, results):
        """
        Given the results and an optional dictionary of weights, return whether or not
        it is likely that they match
        :return: Float indicating fingerprint similarity
        """
        if self.weights:
            results = [self.weights[key] * int(results[key]) for key in results.keys()]
            similarity = sum(results) / sum(self.weights.values())
        else:
            results = [int(results[key]) for key in results.keys()]
            similarity = sum(results) / len(results)

        return similarity

    def identify_top_fingerprint_match(self):
        """
        Iterate through all potential fingerprint matches, return the score of the
        fingerprint that matches the new fingerprint most closely
        """
        max_similarity = 0.0
        for prev_fp in self.prev_fps:
            results = {
                "browserVersion": less_than_or_equal(prev_fp["browserVersion"], self.new_fp["browserVersion"]),
                "browserMajorVersion": less_than_or_equal(prev_fp["browserMajorVersion"], self.new_fp["browserMajorVersion"]),
                "isIE": exact_match(prev_fp["isIE"], self.new_fp["isIE"]),
                "isChrome": exact_match(prev_fp["isChrome"], self.new_fp["isChrome"]),
                "isFirefox": exact_match(prev_fp["isFirefox"], self.new_fp["isFirefox"]),
                "isSafari": exact_match(prev_fp["isSafari"], self.new_fp["isSafari"]),
                "isOpera": exact_match(prev_fp["isOpera"], self.new_fp["isOpera"]),
                "engine": exact_match(prev_fp["engine"], self.new_fp["engine"]),
                "engineVersion": less_than_or_equal(prev_fp["engineVersion"], self.new_fp["engineVersion"]),
                "osVersion": less_than_or_equal(prev_fp["osVersion"], self.new_fp["osVersion"]),
                "isWindows": exact_match(prev_fp["isWindows"], self.new_fp["isWindows"]),
                "isMac": exact_match(prev_fp["isMac"], self.new_fp["isMac"]),
                "isLinux": exact_match(prev_fp["isLinux"], self.new_fp["isLinux"]),
                "isUbuntu": exact_match(prev_fp["isUbuntu"], self.new_fp["isUbuntu"]),
                "isSolaris": exact_match(prev_fp["isSolaris"], self.new_fp["isSolaris"]),
                "IsMobile": exact_match(prev_fp["IsMobile"], self.new_fp["IsMobile"]),
                "isMobileMajor": exact_match(prev_fp["isMobileMajor"], self.new_fp["isMobileMajor"]),
                "isMobileAndroid": exact_match(prev_fp["isMobileAndroid"], self.new_fp["isMobileAndroid"]),
                "isMobileOpera": exact_match(prev_fp["isMobileOpera"], self.new_fp["isMobileOpera"]),
                "isMobileWindows": exact_match(prev_fp["isMobileWindows"], self.new_fp["isMobileWindows"]),
                "isMobileBlackBerry": exact_match(prev_fp["isMobileBlackBerry"], self.new_fp["isMobileBlackBerry"],),
                "isMobileIOS": exact_match(prev_fp["isMobileIOS"], self.new_fp["isMobileIOS"]),
                "isIphone": exact_match(prev_fp["isIphone"], self.new_fp["isIphone"]),
                "isIpad": exact_match(prev_fp["isIpad"], self.new_fp["isIpad"]),
                "isIpod": exact_match(prev_fp["isIpod"], self.new_fp["isIpod"]),
                "colorDepth": less_than_or_equal(prev_fp["colorDepth"], self.new_fp["colorDepth"]),
                "currentResolution": exact_match(prev_fp["currentResolution"], self.new_fp["currentResolution"],),
                "plugins": match_set(prev_fp["plugins"], self.new_fp["plugins"]),
                "isJava": asymmetric_match(prev_fp["isJava"], self.new_fp["isJava"]),
                "isFlash": asymmetric_match(prev_fp["isFlash"], self.new_fp["isFlash"]),
                "isSilverlight": asymmetric_match(prev_fp["isSilverlight"], self.new_fp["isSilverlight"]),
                "mimeTypes": match_set(prev_fp["mimeTypes"], self.new_fp["mimeTypes"]),
                "isMimeTypes": asymmetric_match(prev_fp["isMimeTypes"], self.new_fp["isMimeTypes"]),
                "fonts": match_set(prev_fp["fonts"], self.new_fp["fonts"]),
                "isLocalStorage": asymmetric_match(prev_fp["isLocalStorage"], self.new_fp["isLocalStorage"]),
                "isSessionStorage": asymmetric_match(prev_fp["isSessionStorage"], self.new_fp["isSessionStorage"],),
                "isCookie": asymmetric_match(prev_fp["isCookie"], self.new_fp["isCookie"]),
                "timeZone": exact_match(prev_fp["timeZone"], self.new_fp["timeZone"]),
                "language": exact_match(prev_fp["language"], self.new_fp["language"]),
                "systemLanguage": exact_match(prev_fp["systemLanguage"], self.new_fp["systemLanguage"]),
                "isCanvas": asymmetric_match(prev_fp["isCanvas"], self.new_fp["isCanvas"]),
            }
            similarity = self.estimate_fingerprint_match(results)
            if similarity == 1.0:
                return similarity, results
            elif similarity >= max_similarity:
                max_similarity, max_results = similarity, results
            return max_similarity, max_results
