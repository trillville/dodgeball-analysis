## Manual Fraud Model

Given a set of visitor attributes, predict the likelihood that it's a human committing fraudulent behavior. 

Example input: 
```
{
  "hasShiftingLocation": 1,
  "hasSuspiciousEmail": 1,
  "hasCardIssuerBankBillingLocationMismatch": 1,
  "hasCardIssuerBankIPLocationMismatch": 1,
  "hasTooManyCardFingerprints": 1,
  "hasSuspiciousIP": 1,
  "hasUnusualTimingCharacteristics": 1,
  "hasUntrustedCountry": 1,
  "hasDubiousHTTPHeaderReferrer": 1,
  "hasTooManySimilarEvents": 1,
  "hasUnusualSessionTimeLength": 1,
  "hasUnusualVisitTime": 1,
  "hasCardIssuerBankShippingLocationMismatch": 1,
  "hasShortVisitorLife": 1,
  "hasInsufficientRiskBudget": 1,
  "hasUnusualLocation": 1,
  "hasBillingToShippingCountryMismatch": 1,
  "hasLargePurchaseSize": 0
}
```
Example output:
```
{
  "statusCode": 200,
  "body": {
    "prediction_type": "manual_fraud",
    "fruad_probability": 0.5189
  }
}
```
