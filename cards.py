from typing import Union

"""
Contains card packs and card variants
"""


class Card:
    def __init__(self) -> None:
        """Initialise a Card object."""
        self._question = None
        self._answer = None
        self._points = 0
        self._question_type = "Integer"
        self._card_id = 0

    @property
    def question(self) -> str:
        """Get the question of the card."""
        return self._question

    @property
    def answer(self) -> str:
        """Get the answer of the card."""
        return self._answer

    @property
    def points(self) -> int:
        """Get the points of the card."""
        return self._points

    @property
    def question_type(self) -> str:
        """Get the question type of the card."""
        return self._question_type

    def write_to_card(self, question: str, answer: str, points: int) -> None:
        """
        Write data to the card.

        Arguments:
            question (str): The question of the card.
            answer (str): The answer of the card.
            points (int): The points of the card.
        """
        self._question = question
        self._answer = answer
        self._points = points

    def set_answer(self, answer: str) -> None:
        """Set the answer of the card."""
        self._answer = answer

    def set_card_id(self, card_id: int) -> None:
        """Set the card ID of the card."""
        self._card_id = card_id

    @property
    def card_id(self) -> int:
        """Get the card ID of the card."""
        return self._card_id


class MultipleChoiceCard(Card):
    def __init__(self) -> None:
        """Initialise a MultipleChoiceCard object."""
        super().__init__()
        self._answer_choices = {
            "correct": None,
            "all": [],
        }
        self._question_type = "Multiple Choice"

    @property
    def answer_choices(self) -> dict:
        """
        Return the answer choices of the multiple-choice card.

        Returns:
            dict: The answer choices of the multiple-choice card (all answers and correct answer).
        """
        return self._answer_choices

    @property
    def answer(self) -> str:
        """Return the correct answer of the multiple-choice card."""
        return self._answer_choices["correct"]

    def add_choice(self, answer: str) -> None:
        """Add an answer choice to the multiple-choice card."""
        self._answer_choices["all"].append(answer)

    def set_answer(self, answer: str) -> None:
        """Set the correct answer of the multiple-choice card."""
        self._answer_choices["correct"] = answer

    def write_to_card(self, question: str, points: int, answers: dict = None) -> None:
        """
        Write data to the multiple-choice card.

        Arguments:
            question (str): The question of the multiple-choice card.
            points (int): The points of the multiple-choice card.
            answers (dict): Optional. The answers dictionary of the multiple-choice card.
                            Defaults to None.
        """
        self._question = question
        self._points = points
        self._answer_choices = answers if answers is not None else self._answer_choices


class RevealCard(Card):
    def __init__(self) -> None:
        """Initialise a RevealCard object."""
        super().__init__()
        self._revealed_state = False
        self._question_type = "Reveal"

    def toggle_revealed_state(self) -> bool:
        """Toggle the revealed state of the reveal card and return it."""
        self._revealed_state = not self._revealed_state
        return self._revealed_state


class CardPack:
    def __init__(self, name: str, UID: int) -> None:
        """
        Initialise a CardPack object.

        Arguments:
            name (str): The name of the card pack.
            UID (int): The unique identifier of the user.
        """
        self._cards_list = []
        self._name = name
        self._UID = UID
        self._current_card_index = -1

    @property
    def name(self) -> str:
        """Return the name of the card pack."""
        return self._name
    
    @property
    def cards_list(self) -> list:
        """Return the list of card objects in the card pack."""
        return self._cards_list
    
    def add_card(self, card: Card) -> None:
        """
        Add a card to the card pack.

        Arguments:
            card (Card): The card object to be added to the card pack.
        """
        self._cards_list.append(card)

    @property
    def next_card(self) -> Union[dict, bool]:
        """
        Move to the next card in the pack and return the cards data.

        Returns:
            dict or bool: A dictionary containing the details of the next card,
                          or False if there are no more cards.
        """
        self._current_card_index += 1
        if self._current_card_index == len(self._cards_list):
            return False
        card_obj = self._cards_list[self._current_card_index]
        if card_obj.question_type == "Multiple Choice":
            answer = card_obj.answer_choices
        else:
            answer = card_obj.answer
        card_dict = {
            "question": card_obj.question,
            "answer": answer,
            "question_type": card_obj.question_type,
            "points": card_obj.points,
        }
        return card_dict

    @property
    def current_card_index(self) -> int:
        """Get the index of the current card in the card pack."""
        return self._current_card_index

    @property
    def current_card_obj(self) -> Card:
        """Get the current card object in the card pack."""
        return self._cards_list[self._current_card_index]
