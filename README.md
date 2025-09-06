# mmHomonymDisambiguator

**mmHomonymDisambiguator** is a Python library for detecting and disambiguating Myanmar (Burmese) homonyms. It provides **homonym detection** and **context-based disambiguation** to improve the accuracy of text processing for Myanmar NLP tasks.  

---

## Features
- Integration with **mmTokenizer** for segmentation support  
- Detects homonyms in Myanmar text using a predefined dictionary  
- Context-based disambiguation using n-gram probability models (unigram, bigram, trigram)

---

## Installation

Clone and install locally:

```bash
git clone https://github.com/zar-zar-hlaing/mmHomonymDisambiguator.git
cd mmHomonymDisambiguator
pip install .
```

---

## Usage

### Homonym Detection && Homonym Disambiguation

```python
from mmHomonymDisambiguator import HomonymDisambiguationSystem

system = HomonymDisambiguationSystem()
input_text = "အတက်ပညာ"
tokenized_text, detected_homonyms = system.process_input(input_text)
print(detected_homonyms)  # e.g., ['တက်', 'ညာ']

final_out_with_correct_homonyms = system.disambiguate_homonyms()
print(final_out_with_correct_homonyms) #အတတ်ပညာ
```
---

## Folder Structure
```
./mmHomonymDisambiguator/
├── LICENSE
├── mmHomonymDisambiguator.py
├── modules
│   ├── __init__.py
│   ├── mmHomonymDetector.py
│   ├── mmTokenizer.py
│   └── rabbit.py
├── myanmar_text_data
│   ├── HomonymWords.txt
│   └── TokenTextCorpus.txt
├── README.md
├── reference
│   ├── A_Rule-based_Syllable_Segmentation_of_Myanmar_Text.pdf
│   └── Myanmar_Homonym_Disambiguation_System.pdf
├── requirements.txt
├── setup.py
└── tests
    ├── test_mmtokenizer.py
    └── test_mmHomonymDisambiguator.py
```

---

## Author
- Zar Zar Hlaing

---

## References
- Z. M. Maung and Y. Mikami, “[A Rule-based Syllable Segmentation of Myanmar Text](https://aclanthology.org/I08-3010/),” *Proceedings of the IJCNLP-08 Workshop on NLP for Less Privileged Languages*, Hyderabad, India, Jan. 2008.
- Z. Z. Hlaing and A. Thida, “[Myanmar Homonym Disambiguation System.](https://meral.edu.mm/records/3488)”

---

## Citation
If you use this repository for research or projects related to Myanmar homonym disambiguation, please cite the paper:

- Z. Z. Hlaing and A. Thida, “[Myanmar Homonym Disambiguation System](https://meral.edu.mm/records/3488)”
