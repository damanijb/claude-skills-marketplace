#!/usr/bin/env python3
"""
PII Scrubber — Presidio Engine with Treasury Recognizers
ML-powered PII detection using Microsoft Presidio (spaCy NER + patterns).
Adds treasury-specific patterns: ABA routing, CUSIP, SWIFT, wire refs.

Usage: echo "text with PII" | python3 scrub-presidio.py
Returns: JSON {"scrubbed": "...", "types": [...]} or exits 0 on no PII.
"""

import sys
import json

def get_engines():
    from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
    from presidio_anonymizer import AnonymizerEngine

    analyzer = AnalyzerEngine()

    # Treasury-specific recognizers
    treasury_recognizers = [
        PatternRecognizer(
            supported_entity="US_SSN",
            name="ssn_dash",
            patterns=[Pattern("SSN_DASH", r"\b\d{3}-\d{2}-\d{4}\b", 0.85)],
        ),
        PatternRecognizer(
            supported_entity="ABA_ROUTING",
            name="aba_routing",
            patterns=[Pattern("ABA", r"\b(0[1-9]|[12]\d|3[0-2])\d{7}\b", 0.6)],
        ),
        PatternRecognizer(
            supported_entity="CUSIP",
            name="cusip",
            patterns=[Pattern("CUSIP", r"(?i)cusip[:\s]*[A-Za-z0-9]{9}", 0.85)],
        ),
        PatternRecognizer(
            supported_entity="SWIFT_BIC",
            name="swift_bic",
            patterns=[Pattern("SWIFT", r"(?i)(swift|bic)[:\s]*[A-Z]{6}[A-Z0-9]{2,5}", 0.7)],
        ),
        PatternRecognizer(
            supported_entity="WIRE_REF",
            name="wire_ref",
            patterns=[Pattern("WIRE", r"(?i)(wire|transfer|ref)[#:\s.-]*[A-Z0-9]{10,20}", 0.6)],
        ),
        PatternRecognizer(
            supported_entity="BANK_ACCOUNT",
            name="bank_acct",
            patterns=[Pattern("ACCT", r"(?i)(account|acct)[#:\s.-]*\d{6,17}", 0.8)],
        ),
    ]

    for r in treasury_recognizers:
        analyzer.registry.add_recognizer(r)

    anonymizer = AnonymizerEngine()
    return analyzer, anonymizer


def main():
    text = sys.stdin.read().strip()
    if not text:
        sys.exit(0)

    analyzer, anonymizer = get_engines()

    results = analyzer.analyze(
        text=text,
        language="en",
        score_threshold=0.35,
    )

    if not results:
        sys.exit(0)

    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    detected_types = sorted(set(r.entity_type for r in results))

    json.dump({
        "scrubbed": anonymized.text,
        "types": detected_types,
    }, sys.stdout)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
