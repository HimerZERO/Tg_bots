from dataclasses import dataclass
import random
import json
import logging
import os

logger = logging.getLogger(__name__)

class PairWords:
  word: str
  explanation: str
  progress: float = 0
  last_time: int

  def __init__(self, word: str, args: dict[str, str | float | int]) -> None:
    self.word = word
    self.explanation = args["explanation"]
    self.progress = args["progress"]
    self.last_time = args["last_time"]

  def GetJSON(self) -> tuple[str, dict[str, str | float | int]]:
    return (self.word, {
      "explanation": self.explanation,
      "progress": self.progress,
      "last_time": self.last_time,
      })

  def CheckAnswer(self, answer: str) -> bool:
    # update tame
    return self.Update(answer.lower() == self.explanation)

  def GetExplanation(self) -> str:
    return self.explanation

  def GetWord(self) -> str:
    return self.word

  def GetWeight(self) -> float:
    return 1 - self.progress


  def GetProgress(self) -> float:
    return self.progress

  def Update(self, check: bool) -> bool:
    self.progress /= 2
    self.progress += check / 2
    return check


class MemoryCards:
  my_words: list[PairWords]
  path: str

  def __init__(self, path: str = "/home/ignat/Documents/tg_bots/database/MyEng.json") -> None:
    self.path = path
    if not os.path.exists(path):
      self.my_words = []
      return
    my_dict: dict[str, dict[str, str | float | int]]
    with open(path) as fp:
      my_dict = json.load(fp)
    self.my_words = [PairWords(*word) for word in my_dict.items()]

  def GetPair(self, word: str) -> PairWords | None:
    for pair in self.my_words:
      if pair.GetWord() == word:
        return pair

  def GetSize(self) -> int:
    return len(self.my_words)

  def AlphabetOrder(self, head: int | None = None) -> list[PairWords]:
    if head is None:
      head = self.GetSize()
    head = min(head, self.GetSize())
    return sorted(self.my_words, key=lambda pair: pair.GetWord())[:head]

  def NegativeProgressOrder(self, head: int | None = None) -> list[PairWords]:
    if head is None:
      head = self.GetSize()
    head = min(head, self.GetSize())
    return sorted(self.my_words, key=lambda pair: pair.GetProgress())[:head]

  def GetWeightRandom(self, k: int = 1) -> list[PairWords]:
    return random.choices(self.my_words,
                          weights=(pair.GetWeight() for pair in self.my_words),
                          k=k)

  def GetExplanation(self, word: str) -> str | None:
    for pair in self.my_words:
      if pair.GetWord() == word:
        return pair.GetExplanation()

  def GetRandom(self, k: int = 1) -> list[PairWords]:
    return random.choices(self.my_words, k=k)

  def GetDataBase(self) -> str:
    return self.path

  def NewWord(self, word: str, explanation: str) -> None:
    if (old := self.GetExplanation(word)) is not None:
      logger.error(f"THe word \"{word}\" already have explanation: {old}")
      return
    new_word = (word, {
      "explanation": explanation,
      "progress": 0.0,
      "last_time": 0,
    })
    self.my_words.append(PairWords(*new_word))

  def Close(self) -> None:
    to_json: dict[str, dict[str | float | int]] = dict([pair.GetJSON() for pair in self.my_words])
    with open(self.path, 'w') as fp:
      json.dump(to_json, fp, sort_keys=True, indent=2)


if __name__ == "__main__":
  words = MemoryCards()
  word = words.GetRandom()[0]
  print(word is words.my_words[0])
  # word.CheckAnswer(word.explanation)
  new_word = words.GetPair(word.word)
  print(new_word is words.my_words[0])
  print(word.GetProgress())
  words.Close()
