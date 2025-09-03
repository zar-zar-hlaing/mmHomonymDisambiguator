import os
import pytest

from mmHomonymDisambiguator import HomonymDisambiguationSystem


def test_initialization():
    """System initializes correctly with corpus and homonym files."""
    system = HomonymDisambiguationSystem()
    assert isinstance(system.homo_file, str)
    assert os.path.exists(system.homo_file)


def test_process_input_tokenization():
    """Tokenization should return syllable-segmented text and homonyms list."""
    system = HomonymDisambiguationSystem()
    text = "လူတိုင်းသည် တူညီ လွတ်လပ်သော ဂုဏ်သိက္ခာဖြင့်"
    tokenized, homonyms = system.process_input(text)

    assert isinstance(tokenized, str)
    assert isinstance(homonyms, list)


def test_disambiguation_runs():
    """Disambiguation should return a non-empty string."""
    system = HomonymDisambiguationSystem()
    text = "လူတိုင်းသည် တူညီ လွတ်လပ်သော ဂုဏ်သိက္ခာဖြင့်"
    system.process_input(text)

    result = system.disambiguate_homonyms()
    assert isinstance(result, str)
    assert result != ""


def test_bigram_trigram_probabilities():
    """Check probability calculations don’t crash and return floats."""
    system = HomonymDisambiguationSystem()

    prob_bigram = system.calculate_token_probability("လူ", "တိုင်း")
    prob_trigram = system.calculate_trigram_probability("လူ", "တိုင်း", "သည်")

    assert isinstance(prob_bigram, float)
    assert isinstance(prob_trigram, float)


def test_zg2uni_and_uni2zg_roundtrip():
    """Check Zawgyi ↔ Unicode conversion produces strings."""
    system = HomonymDisambiguationSystem()

    # Sample Burmese in Unicode
    unicode_text = "မြန်မာစာ"   # "Myanmar language" in Unicode
    # Sample Burmese in Zawgyi (visually same, different encoding)
    zawgyi_text = "ျမန္မာစာ"   

    uni_converted = system.zg2uni(zawgyi_text)
    zg_converted = system.uni2zg(unicode_text)

    assert isinstance(uni_converted, str)
    assert isinstance(zg_converted, str)

    # At least ensure conversion doesn’t return the same exact encoding
    assert uni_converted != zawgyi_text
    assert zg_converted != unicode_text

