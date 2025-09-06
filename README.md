# mmHomonymDisambiguator

**mmHomonymDisambiguator** is a Python library for detecting and disambiguating Myanmar (Burmese) homonyms. It provides **homonym detection** and **context-based disambiguation** to improve the accuracy of text processing for Myanmar NLP tasks.  

---

## 📖 Homonyms  

A **homonym** is a word that shares the same pronunciation or spelling with another word but has a different meaning.  
Homonyms exist in many languages, including **English** and **Myanmar**.  

Understanding homonyms is important for **natural language processing (NLP)** because correct interpretation always depends on **context**.  

---

### English Homonyms (for clarity)  

In English, the words **two**, **to**, and **too** are pronounced the same in the sentence:  

> *“The two boys want to play too.”*  

Although they sound alike, their spellings and meanings are different. These are **homonyms**.  

**Examples of English Homonyms:**  

| Word 1 | Meaning 1 | Word 2 | Meaning 2 |
|--------|-----------|--------|-----------|
| **Accept** | to take something that is given to you | **Except** | to leave out |
| **Aid** | help | **Aide** | one who helps |
| **Complement** | something that makes a thing whole or perfect | **Compliment** | to praise |
| **Discrete** | separate | **Discreet** | modest, prudent, unobtrusive |
| **Forth** | forward | **Fourth** | an ordinal number |

---

### Myanmar Homonyms (main focus)  

In the **Myanmar language**, homonyms are especially common due to the rich phonetic system and script.  
Many words may look or sound the same but carry very different meanings depending on **context**.  

**Examples of Myanmar Homonyms:**  

| Word 1 | Meaning 1 | Word 2 | Meaning 2 |
|--------|-----------|--------|-----------|
| **ကျိုး** | to break, fracture; consequence | **ကြိုး** | rope, string; to attempt |
| **ကျား** | tiger | **ကြား** | to hear; between (in the middle of) |
| **စီ** | to arrange, to line up | **စည်** | prosperous, lively; drum |
| **တန်း** | line, row; class/level | **တမ်း** | draft, note, informal record |
| **ခမ်း** | ceremonial; formal occasion | **ခန်း** | section, stanza, room |

---

## Homonyms and Ambiguous Homonyms Detection and Disambiguation

This section describes the algorithm used to detect **homonym words** in a given text and resolve ambiguous cases using a **Corpus-Based N-Gram Model**.

### Steps

1. Take tokenized text as input.  
2. Convert the tokenized text into a string array `tokens[]`.  
3. Read the text file containing homonym words and convert it into a string array `textWords[]`.  
4. For each value in `tokens[]`:  
   - If the value exists in `textWords[]`, mark it as a homonym.  
   - Append this homonym word to the string `tempHomonyms`.  
5. Apply a **Corpus-Based N-Gram Model** on `tempHomonyms` to disambiguate homonyms:  
   - The model calculates the **probability of each possible homonym** based on its context.  
   - Select the homonym with the **highest probability** as the correct one.  
   - Replace ambiguous homonyms in the text with the **most probable correct homonym**.  
   - If no homonyms are found, retain the original text.  

### Pseudocode

```
Begin
  1. Take tokenized text as input
  2. Convert the tokenized text into string array tokens[]
  3. Read the text file containing homonym words into string array textWords[]
  4. For each value in tokens[]:
       if (value ∈ textWords[])
           mark value as homonym
           append value to tempHomonyms
  5. Apply Corpus-Based N-Gram Model on tempHomonyms:
       for each homonym in tempHomonyms:
           calculate probability for all possible meanings
           select the homonym with the highest probability
           replace in text with the most probable homonym
       if no homonyms are found:
           retain original text
End
```

### 📌 Summary  

- Homonyms are words that **look or sound alike but have different meanings**.  
- In **English**, homonyms include pairs like *accept/except* or *discrete/discreet*.  
- In **Myanmar**, homonyms such as *ကျိုး/ကြိုး* or *ကျား/ကြား* show how the same sound or spelling can represent very different concepts.  
- Correctly handling homonyms is essential in **Myanmar NLP tasks** such as translation, speech recognition, and text classification.  



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
If you use the library or data from this repository in research or projects related to Myanmar homonym disambiguation, please cite the following paper:

- Z. Z. Hlaing and A. Thida, “[Myanmar Homonym Disambiguation System](https://meral.edu.mm/records/3488)”
