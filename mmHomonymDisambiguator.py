import os
from collections import defaultdict
from typing import List
from modules.rabbit import Rabbit
from modules.mmHomonymDetector import detect_homonyms
from modules.mmTokenizer import syllableSegment


class HomonymDisambiguationSystem:
    def __init__(self, homo_file: str = None):
        """Initialize the system and set homonym file path."""
        if homo_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            homo_file = os.path.join(base_dir, "myanmar_text_data", "HomonymWords.txt")
        self.homo_file = homo_file

        # Core state
        self.input_text = ""
        self.tokenizedLst: List[str] = []
        self.mustResolveHomoLst: List[str] = []
        self.mustResolveHomoPos: List[int] = []
        self.homonymTotalTokenlst: List[List[str]] = []
        self.finalResultString: str = ""

        # N-gram probability data
        self.unigram_counts = defaultdict(int)
        self.bigram_counts = defaultdict(int)
        self.trigram_counts = defaultdict(int)
        self.total_token_count = 0

        # Full corpus as tokenized sentences
        self.corpus_data: List[List[str]] = []

        # Load corpus into memory
        self._load_corpus_data()

    def _load_corpus_data(self):
        """Load corpus data and build n-gram counts."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        corpus_file = os.path.join(base_dir, "myanmar_text_data", "TokenTextCorpus.txt")

        if not os.path.exists(corpus_file):
            print(f"[WARN] Corpus file not found: {corpus_file}")
            return

        with open(corpus_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                tokenized_line = syllableSegment(line)
                tokens = [tok.strip() for tok in tokenized_line.split("|") if tok.strip()]

                if not tokens:
                    continue

                self.corpus_data.append(tokens)
                self.total_token_count += len(tokens)

                # Count unigrams
                for w in tokens:
                    self.unigram_counts[w] += 1

                # Count bigrams
                for i in range(len(tokens) - 1):
                    bigram = f"{tokens[i]} {tokens[i+1]}"
                    self.bigram_counts[bigram] += 1

                # Count trigrams
                for i in range(len(tokens) - 2):
                    trigram = f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}"
                    self.trigram_counts[trigram] += 1

        # print(f"___word___ {self.total_token_count}")

    def process_input(self, input_text: str, is_zawgyi: bool = False):
        """Process input text: tokenize and detect homonyms."""
        if is_zawgyi:
            input_text = self.zg12uni51(input_text)

        self.input_text = input_text
        tokenized_text = syllableSegment(input_text)
        self.tokenizedLst = tokenized_text.split("|") if tokenized_text else []

        homonyms = detect_homonyms(tokenized_text)
        if homonyms:
            self.mustResolveHomoLst = homonyms

        return tokenized_text, homonyms

    def add_homo_list_from_file(self):
        """Load homonym groups from the homonym file."""
        try:
            with open(self.homo_file, "r", encoding="utf-8") as f:
                for line in f:
                    tokens = line.strip().split()
                    if tokens:
                        self.homonymTotalTokenlst.append(tokens)
        except FileNotFoundError:
            print(f"[WARN] Homonym file not found: {self.homo_file}")

    def calculate_token_probability(self, w1: str, w2: str) -> float:
        """Bigram probability P(w2|w1)."""
        bigram = f"{w1} {w2}"
        if self.bigram_counts[bigram] and self.unigram_counts[w1]:
            return self.bigram_counts[bigram] / self.unigram_counts[w1]
        return 0.0

    def calculate_trigram_probability(self, w1: str, w2: str, w3: str) -> float:
        """Trigram probability P(w3|w1,w2)."""
        trigram = f"{w1} {w2} {w3}"
        bigram = f"{w1} {w2}"
        if self.trigram_counts[trigram] and self.bigram_counts[bigram]:
            return self.trigram_counts[trigram] / self.bigram_counts[bigram]
        return 0.0

    def disambiguate_homonyms(self):
        """Replace ambiguous homonyms with best candidates."""
        if not self.mustResolveHomoLst:
            return "".join(self.tokenizedLst)

        self.add_homo_list_from_file()

        for i, homo in enumerate(self.mustResolveHomoLst):
            pos = self.find_homonym_position(homo)
            if pos == -1:
                continue

            candidate = self.find_best_candidate(homo, pos)
            if candidate:
                self.tokenizedLst[pos] = candidate

        self.finalResultString = "".join(self.tokenizedLst)
        return self.finalResultString

    def find_homonym_position(self, token: str) -> int:
        """Find the position of a homonym token in the tokenized list."""
        try:
            return self.tokenizedLst.index(token)
        except ValueError:
            return -1

    def find_best_candidate(self, homo_token: str, index: int) -> str:
        """Select the best homonym candidate using context probability."""
        candidates = next(
            (group for group in self.homonymTotalTokenlst if homo_token in group), []
        )
        if not candidates:
            return homo_token

        best, best_prob = homo_token, -1.0
        for cand in candidates:
            prob = self.calculate_context_probability(cand, index)
            if prob > best_prob:
                best, best_prob = cand, prob
        return best

    def calculate_context_probability(self, candidate: str, index: int) -> float:
        """Compute probability of candidate in context using n-grams."""
        probs = []

        if index > 0:  # left bigram
            probs.append(self.calculate_token_probability(self.tokenizedLst[index - 1], candidate))
        if index < len(self.tokenizedLst) - 1:  # right bigram
            probs.append(self.calculate_token_probability(candidate, self.tokenizedLst[index + 1]))
        if index > 1:  # left trigram
            probs.append(self.calculate_trigram_probability(self.tokenizedLst[index - 2], self.tokenizedLst[index - 1], candidate))
        if index < len(self.tokenizedLst) - 2:  # right trigram
            probs.append(self.calculate_trigram_probability(candidate, self.tokenizedLst[index + 1], self.tokenizedLst[index + 2]))

        return sum(probs) / len(probs) if probs else 0.0

    def zg2uni(self, text: str) -> str:
        """Convert Zawgyi to Unicode."""        
        return Rabbit.zg2uni(text)

    def uni2zg(self, text: str) -> str:
        """Convert Unicode to Zawgyi."""        
        return Rabbit.zg2uni(text)

def main():
    system = HomonymDisambiguationSystem()
    text = "လူတိုင်းသည် တူညီ လွတ်လတ်သော ဂုဏ်သိက္ခာဖြင့်..."
    print("Input:\t", text)


    tokenized, homonyms = system.process_input(text)
    print("Tokenized Text:\t", tokenized)
    print("Homonyms:\t", homonyms)

    result = system.disambiguate_homonyms()
    print("\nResult:\t", result)


if __name__ == "__main__":
    main()
