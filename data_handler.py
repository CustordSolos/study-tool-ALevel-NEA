from database_access import Database
from binary_search_tree import BinarySearchTree
from queues import *
from cards import *
from graphs import *
from address_fetcher import AddressSearch
from PIL import Image
from io import BytesIO
import textwrap
import re
import random
import json
import numpy as np
from typing import Dict, Optional, Tuple

"""
Bridges the GUI to other modules.
Handles formatting data for the GUI, and verifying data for other methods.
"""


class DataHandler:
    """
    Handle events and values from the GUI and perform respective operations.
    """

    def __init__(self) -> None:
        """
        Initialise a DataHandler object, additionally instantiating a Database object.
        """
        self.db = Database(Path.cwd() / "database" / "study_tool_db.db")
        # Confirm database state, correcting issues if possible
        self.db.check_database()
        self._topics_dict = self.db.get_topics_rows()
        self._cur_UID = None
        self._cur_first_name = ""
        self._user_library = None
        self._prev_file_path = None
        self._tree = None
        self._queue_max_size = 6
        self._queue = None
        self._adjacency_list = {}
        self._adj_matrix = []
        self._current_card_pack = None
        self._current_card = None
        self._correct_card_ids = []
        self._leaderboard_data = []
        self._topic_id = None
        self._topic_theory_list = []
        self._topic_page = -1

    # Account management
    def _val_create_username(self, username: str) -> List[Union[str, None]]:
        """
        Validate username formatting for account creation. A username is valid if:
            - 3 -> 20 characters in length.
            - Is alphanumeric (with exception to underscores)

        Arguments:
            username (str): Username from user input.

        Returns:
            List[str]: List of strings containing error messages for the user. Return empty list if validation passes.
        """
        err_list = []
        if username == "":
            err_list.append("Please provide a username.")
            return err_list
        # Check username is formatted correctly
        if not (3 <= len(username) <= 20):
            err_list.append("Username must be between 3 and 20 characters.")
        if not (username.replace("_", "").isalnum()):
            err_list.append(
                "Username must be alphanumeric (A-Z, 0-9), with exception to underscores."
            )
        return err_list

    def _val_create_password(self, password: str) -> List[Union[str, None]]:
        """
        Evaluate a passwords strength for account creation. A password is strong/valid if:
            - 8 -> 64 characters in length.
            - 1 digit or more.
            - 1 symbol or more.
            - 1 uppercase character or more.
            - 1 lowercase chracter or more.

        Arguments:
            password (str): Plaintext password from user input.

        Returns:
            List[str]: List of strings containing error messages for the user. Return empty list if validation passes.
        """
        err_list = []
        if password == "":
            err_list.append("Please provide a password.")
            return err_list
        if not (8 <= len(password) <= 64):
            err_list.append("Password must be between 8 and 64 characters.")
        if re.search(r"\d", password) is None:
            err_list.append("Password must contain at least 1 digit")
        if re.search(r"[A-Z]", password) is None:
            err_list.append("Password must contain at least 1 uppercase character.")
        if re.search(r"[a-z]", password) is None:
            err_list.append("Password must contain at least 1 lowercase character.")
        if re.search(r"\W", password) is None:
            err_list.append("Password must contain at least 1 special character.")
        return err_list

    def _val_create_first_name(self, first_name: str) -> List[Union[str, None]]:
        """
        Validate first name formatting for account creation. A first name is valid if:
            - 1 -> 50 characters in length
            - Is alphanumeric

        Arguments:
            first_name (str): First name from user input

        Returns:
            List[str]: List of strings containing error messages for the user. Return empty list if validation passes.
        """
        err_list = []
        if first_name == "":
            err_list.append("Please provide a first name.")
            return err_list
        if not first_name.isalpha():
            err_list.append("First name must be alphanumeric.")
        if not (1 <= len(first_name) <= 50):
            err_list.append("First name must contain between 1-50 characters.")
        return err_list

    def _val_create_email(self, email: str) -> List[Union[str, None]]:
        """
        Validate email formatting for account creation. An email is valid if:
            - Matches a regex pattern to recognise format *@*.*
            - Is between 5 and 254 characters in length.

        Arguments:
            email (str): Email address from user input

        Returns:
            List[str]: List of strings containing error messages for the user. Return empty list if validation passes.
        """
        err_list = []
        if email == "":
            err_list.append("Please provide an email address.")
            return err_list
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        # Checking email for formatting errors
        if not re.match(pattern, email):
            err_list.append("Email address is not valid.")
        if len(email) < 5 or len(email) > 254:
            err_list.append("Email must be between 5 and 254 characters")
        return err_list

    def val_create_address(self, house_number: int, postcode: str) -> dict:
        """
        Validate address for account creation. An address is valid if:
            - Can be used with address_fetcher to retrieve a postcode, town and country

        Arguments:
            house_number (int): House number from user input
            postcode (str): Postcode from user input

        Returns:
            Dict[bool, str, dict]: Dictionary containg the success of the operation (bool), an error (if present) and address if found.
        """
        result = {"result": False, "err_msg": "", "address": {}}
        if house_number == "" or postcode == "":
            result["err_msg"] = "Please provide a house number and postcode"
            return result
        if 1 > len(house_number) > 25 or 1 > len(postcode) > 8:
            result[
                "err_msg"
            ] = "Please ensure to meet the following criteria:\nLength of house number must be between 1 and 25 characters.\nLength of postcode must be between 1 and 8 characters."
            return result
        if self.validate_integer(house_number):
            result = AddressSearch.get_address_details(house_number, postcode)
        else:
            result["err_msg"] = "Please enter an integer house number."
        return result

    def _val_create_credentials(
        self, username: str, password: str, first_name: str, email: str
    ) -> dict:
        """
        Validate the formatting of credentials for account creation by calling internal methods.

        Arguments:
            username (str): Username from user input
            password (str): Password from user input
            first_name (str): First name from user input
            email (str): Email from user input

        Returns:
            dict: A dictionary containing validation outcome.
            - 'result' (bool): True if the account can be created, False if validation fails.
            - 'username_err_list' (list): A list of relevant validation errors for the username.
            - 'password_err_list' (list): A list of relevant validation errors for the password.
            - 'first_name_err_list' (list): A list of relevant validation errors for the first name.
            - 'email_err_list' (list): A list of relevant validation errors for the email.
        """
        # Validating all user inputs from internal methods that return error lists
        err_lists = []  # 2D list for errors respective to each input
        err_lists.extend(
            (
                self._val_create_username(username),
                self._val_create_password(password),
                self._val_create_first_name(first_name),
                self._val_create_email(email),
            )
        )
        results_dict = {
            "result": False,
            "username_err_list": err_lists[0],
            "password_err_list": err_lists[1],
            "first_name_err_list": err_lists[2],
            "email_err_list": err_lists[3],
        }
        # Check if all lists are empty
        if not any(err_lists):
            results_dict["result"] = True
        return results_dict

    def create_account(
        self,
        username: str,
        password: str,
        first_name: str,
        email: str,
        address_dict: dict,
    ) -> Dict[bool, str]:
        """
        Create a new account from user input.

        Arguments:
            username (str): Username from user input.
            password (str): Password from user input.
            first_name (str): First name from user input.
            email (str): Email address from user input.
            house_number (int): House number from user input
            postcode (str): Postcode from user input

        Returns:
            dict: The result of the account creation and error messages.
                - "result" (bool): True if the account was created successfully, otherwise False.
                - "err_msg" (str): Error message if the account creation failed at any point.
        """
        val_results = self._val_create_credentials(
            username, password, first_name, email
        )
        # Formatting validation errors
        if not val_results["result"]:
            return {
                "result": False,
                "err_msg": "\n".join(
                    str(msg)
                    for innerlist in [err for key, err in val_results.items()][1:]
                    for msg in innerlist
                ),
            }
        # Attempt to create account, return result
        val_results = self.db.create_account(
            username, password, first_name, email, address_dict
        )
        return {
            "result": val_results["result"],
            "err_msg": "\n".join(
                str(msg) for msg in [err for key, err in val_results.items()][1:]
            ),
        }

    def authenticate_user(self, username: str, password: str) -> dict:
        """
        Authenticate a user using a username and password.

        Arguments:
            username (str): Username entered by the user.
            password (str): Password entered by the user.

        Returns:
            dict: A dictionary containing authentication result and error message.
                - "auth" (bool): True if the authentication is successful, otherwise False.
                - "err_msg" (str): An error message if authentication fails, otherwise empty if authenticated.
        """
        # Presence check on username and password
        if len(username) == 0 or len(password) == 0:
            return {"auth": False, "err_msg": "Please complete all fields."}
        # Authenticate login with database
        auth_result = self.db.auth_login(username, password)
        if auth_result["auth"]:
            self._cur_UID = auth_result["UID"]
            self._cur_first_name = self.db.get_first_name(self._cur_UID)
        del auth_result["UID"]
        return auth_result

    def clear_user_data(self) -> None:
        """Reset specific data upon logout."""
        self._cur_UID = None
        self._user_library = None
        self._prev_file_path = None
        self._tree = None
        self._adjacency_list = {}
        self._leaderboard_data = []
        self._topic_id = None
        self._topic_theory_list = []

    @property
    def cur_name(self) -> str:
        return self._cur_first_name

    # Study notes management
    @property
    def topics_list(self) -> List[str]:
        """Return a list of topic names"""
        return [topic["topic_name"] for topic in self._topics_dict]

    @property
    def calc_revised_percent(self) -> int:
        """Return the percentage of topics revised by a user."""
        return int(
            len(self.db.get_completed_topics(self._cur_UID))
            / len(self._topics_dict)
            * 100
        )

    def selected_topic_id(self, index: int) -> int:
        """
        Return the topic id of a topic.
        This should be used in conjunction with the topics_list method to provide an accurate index.
        """
        return self._topics_dict[index]["topic_id"]

    def load_topic_id(self, topic_id: int) -> None:
        """Load the topic's theory contents"""
        # Resetting variables
        self._topic_id = topic_id
        self._topic_page = -1
        self._topic_theory_list = []
        # Get directory and read JSON file
        subpath = self.db.get_theory_path(topic_id)
        with open(Path.cwd() / Path(*subpath.split("\\")), "r") as file:
            contents = json.load(file)
        for heading, items in contents.items():
            for item in items:
                self._topic_theory_list.append({heading: item})

    @property
    def topic_name(self) -> Optional[str]:
        """
        Return the name of the active topic.

        Returns:
            Optional[str]: The name of the current topic, otherwise None if not found.
        """
        topic_name = next(
            (
                topic["topic_name"]
                for topic in self._topics_dict
                if topic["topic_id"] == self._topic_id
            ),
            None,
        )
        return topic_name

    @property
    def total_theory_pages(self) -> int:
        """Return total amount of pages in the current topic."""
        return len(self._topic_theory_list)

    def get_next_theory_page(self, next_page: bool = True) -> Union[Dict, bool]:
        """
        Return the next or previous theory page.

        Arguments:
            next_page (bool, optional): If True, retrieves the next page; otherwise the previous page. Defaults to True.

        Returns:
            Union[Dict, bool]:
                - (bool): False if there are no pages in the given direction.
                - (dict): "heading" str: Page heading.
                        "page_number" int: Current page number (for user).
                        "body" str: Text to be displayed.
                        "image_dir" Union[Path, str]: Path if an image is present, otherwise an empty string.
        """
        page_index = self._topic_page + 1 if next_page else self._topic_page - 1
        if page_index not in range(len(self._topic_theory_list)):
            return False
        if page_index == len(self._topic_theory_list) - 1:
            self.db.complete_topic(self._cur_UID, self._topic_id)
        self._topic_page = page_index
        current_page = self._topic_theory_list[self._topic_page]
        key = next(iter(current_page))
        sub_dir = current_page[key]["image_dir"]
        image_dir = Path.cwd() / Path(*sub_dir.split("\\")) if len(sub_dir) != 0 else ""
        lines = current_page[key]["text"].split("\n")
        lines_wrapped = [textwrap.fill(line, width=70) for line in lines]
        return {
            "heading": key,
            "page_number": self._topic_page + 1,
            "body": "\n\n".join(lines_wrapped),
            "image_dir": image_dir,
        }

    # Flashcard study management
    @property
    def user_library_list(self) -> List[str]:
        """Return the list of flashcard packs in a user's library"""
        self._user_library = self.db.get_user_library(self._cur_UID)
        list = [pack["pack_name"] for pack in self._user_library]
        return list

    def selected_pack_id(self, index: int) -> int:
        """
        Return the pack id of a card pack.
        This should be used in conjunction with the user_library_list method to provide an accurate index.
        """
        return self._user_library[index]["pack_id"]

    def load_pack_data(self, pack_id: int) -> None:
        """
        Load a card packs data to objects using a pack id.

        Arguments:
            pack_id (int): The ID of the card pack.
        """
        # Clear correct card ids
        self._correct_card_ids = []
        # Fetch pack data from database module
        pack_name, cards_list = self.db.get_pack_data(pack_id)
        self._current_card_pack = CardPack(pack_name, self._cur_UID)
        for card in cards_list:
            if card["question_type"] == "Reveal":
                new_card = RevealCard()
                new_card.write_to_card(card["question"], card["answer"], card["points"])
            elif card["question_type"] == "Integer":
                new_card = Card()
                new_card.write_to_card(card["question"], card["answer"], card["points"])
            elif card["question_type"] == "Multiple Choice":
                new_card = MultipleChoiceCard()
                # Deserialising json received from database
                answers = json.loads(card["answer"])
                new_card.write_to_card(card["question"], card["points"], answers)
            new_card.set_card_id(card["card_id"])
            self._current_card_pack.add_card(new_card)

    @property
    def current_pack_name(self) -> str:
        return self._current_card_pack.name

    @property
    def pack_cards_count(self) -> int:
        """Return the count of cards in the active card pack."""
        return len(self._current_card_pack.cards_list)

    @property
    def current_card_number(self) -> int:
        """Return the current card number the user is on."""
        return self._current_card_pack._current_card_index + 1

    @property
    def current_card_answer(self) -> str:
        """Return the correct answer for the current card."""
        card_obj = self._current_card_pack.current_card_obj
        return card_obj.answer

    def check_answer(
        self, user_answer: str, use_index: bool = False
    ) -> Union[bool, str]:
        """
        Check the user's answer against the correct answer.

        Args:
            user_answer (str): The user's answer.
            use_index (bool, optional): If user_answer is an index to select from answer choices (multiple choice cards). Defaults to False.

        Returns:
            Union[bool, str]:
                - (bool) If the answer is correct, returns True.
                - (str) If the answer is incorrect or not provided, returns the correct answer.
        """
        if user_answer == "":
            return False
        if use_index:
            card_obj = self._current_card_pack.current_card_obj
            user_answer = card_obj.answer_choices["all"][int(user_answer) - 1]
        card_answer = self.current_card_answer
        if user_answer == str(card_answer):
            self._correct_card_ids.append(
                self._current_card_pack.current_card_obj.card_id
            )
            return True
        else:
            return card_answer

    @property
    def next_card_info(self) -> Union[dict, bool]:
        """
        Move to the next card in the pack and return the card data.

        Returns:
            dict or bool: A dictionary containing the details of the next card, otherwise False if there are no more cards.
        """
        next_card = self._current_card_pack.next_card
        if next_card is False:
            return False
        return next_card

    def format_multiple_choice_options(self, card: dict) -> str:
        """
        Format multiple choice card answeres into a numbered string.

        Arguments:
            card (dict): Multiple choice card "_answer_choices"
        """
        answers = card["answer"]["all"]
        numbered_string = "\n".join(
            [f"{i+1}) {answer}" for i, answer in enumerate(answers)]
        )
        return numbered_string

    def toggle_card_reveal(self) -> bool:
        """Toggle and return the state of a reveal card."""
        card_obj = self._current_card_pack.current_card_obj
        return card_obj.toggle_revealed_state()

    def get_share_id(self, pack_id: int) -> str:
        """Return the share id of a card pack."""
        return self.db.get_share_id(pack_id)

    def download_pack(self, share_id: str) -> Dict[bool, str]:
        """
        Add a card pack to a user's library.

        Arguments:
            share_id (str): Share ID of the pack to be added.

        Returns:
            dict: Contains the result and error message.
                - "result" (bool): True if the pack is added, otherwise False.
                - "err_msg" (str): Error string for user, empty if pack is added.
        """
        if not share_id:
            return {"result": False, "err_msg": "Please provide a share ID"}
        return self.db.download_pack(share_id, self._cur_UID)

    def clear_current_card(self) -> None:
        self._current_card = None

    def delete_card_pack(self, pack_id: int) -> str:
        """Attempt to delete a card pack and return the result message (str)."""
        return self.db.delete_card_pack(pack_id, self._cur_UID)

    # Flashcard creator management
    def validate_pack_name(self, pack_name: str) -> Union[bool, str]:
        """
        Validate a card pack name and create a CardPack object.

        Arguments:
            pack_name (str): Pack name from user input.

        Returns:
            Union[bool, str]: True if CardPack object is created, else appropriate error message as string.
        """
        # creates a card pack object
        # Check if the length is between 3 and 30 characters and alphanumeric
        if 3 <= len(pack_name) <= 30 and re.match("^[a-zA-Z0-9 ]*$", pack_name):
            self._current_card_pack = CardPack(pack_name, self._cur_UID)
            return True
        return "Please ensure pack name is between 3 and 30 alphanumeric characters."

    def add_card_choice(self, answer: str, is_correct_answer: bool) -> Union[str, bool]:
        """
        Add a choice for a multiple-choice card.

        Arguments:
            answer (str): The answer choice to add.
            is_correct_answer (bool): Indicates whether the answer choice is correct.

        Returns:
            Union[str, bool]: True if the choice was added, else a string error message if failed.
        """
        self._current_card = (
            self._current_card
            if self._current_card is not None
            else MultipleChoiceCard()
        )
        if self.get_answer_count() == 4:
            return "Maximum amount of answer submitted."
        if (
            self.get_answer_count() == 3
            and self._current_card.answer_choices["correct"] is None
            and not is_correct_answer
        ):
            return "You must have at least 1 corrct answer."
        if answer in self._current_card.answer_choices["all"]:
            return "You have already added this option."
        if 1 <= len(answer) <= 125:
            if is_correct_answer:
                # System is set up such that a card can only have one correct answer
                if self._current_card.answer is None:
                    self._current_card.set_answer(answer)
                else:
                    return "You have already set a correct answer."
            self._current_card.add_choice(answer)
            return True
        else:
            return "Please ensure the answer is between 1 and 125 characters."

    def get_answer_count(self) -> int:
        """Return the number of choices in the current multiple choice card"""
        return len(self._current_card.answer_choices["all"])

    def duplicate_cards_check(self, question: str) -> bool:
        """Check if a question is duplicate"""
        for card in self._current_card_pack.cards_list:
            if question == card.question:
                return True
        return False

    def add_card(
        self, question_type: str, question: str, answer: str, points: int
    ) -> Union[str, bool]:
        """
        Add a card to the current card pack.

        Arguments:
            question_type (str): The type of question ('Reveal', 'Multiple choice', or 'Numerical').
            question (str): The prompt from user input.
            answer (str): The answer from user input.
            points (int): The points to be associated with the card.

        Returns:
            Union[str, bool]: Either a boolean value True if the card was added successfully, or a string indicating an error message if the operation failed.
        """
        # Check prompt formatting
        if not 1 <= len(question) <= 125:
            return (
                "Please ensure the prompt and answer is between 1 and 125 characters."
            )
        # Check for dupe cards
        if self.duplicate_cards_check(question):
            return "You already have a card with this question."
        # Reveal card
        if question_type == "Reveal":
            if 1 <= len(answer) <= 125:
                self._current_card = RevealCard()
                # Points set to 0 for all reveal cards
                self._current_card.write_to_card(question, answer, 0)
            else:
                return "Please ensure the answer is between 1 and 125 characters."
        # Multiple choice card (answers are set sequentially in the add_card_choice method prior to this)
        elif question_type == "Multiple choice":
            if self._current_card is None:
                return "Please ensure there are at least 2 choices available."
            if (
                len(self._current_card.answer_choices["all"]) >= 2
                and self._current_card.answer_choices["correct"] is not None
            ):
                self._current_card.write_to_card(question, points)
            else:
                return "Please ensure there are at least 2 choices available, inlcuding the correct option."
        # Integer card
        elif question_type == "Numerical":
            if self.validate_integer(answer) and 1 <= len(answer) <= 6:
                self._current_card = Card()
                self._current_card.write_to_card(question, answer, points)
            else:
                return "Please ensure the answer is an integer between 1 and 6 chracters in length."
        # All validation passed, card is added to the pack and current_card is cleared
        self._current_card_pack.add_card(self._current_card)
        self.clear_current_card()
        return True

    def save_card_pack(self) -> Union[bool, str]:
        """
        Save the current card pack to the database.

        Returns:
            Union[bool, str]: True if the card pack was saved, otherwise a string with an error message.
        """
        if len(self._current_card_pack.cards_list) > 0:
            card_list = []
            for card in self._current_card_pack.cards_list:
                # Reformatting for multiple choice (for database compatiblity)
                if card.question_type == "Multiple Choice":
                    answer = json.dumps(card.answer_choices)
                else:
                    answer = card.answer
                card_list.append(
                    {
                        "question": card.question,
                        "answer": answer,
                        "points": card.points,
                        "question_type": card.question_type,
                    }
                )
            self.db.create_flashcard_pack(
                self._current_card_pack.name, card_list, self._cur_UID
            )
            self.clear_current_card()
            self.clear_current_pack()
            return True
        else:
            return "Please save add at least one card"

    def clear_current_pack(self) -> None:
        self._current_card_pack = None
        self._current_card = None
        self._correct_card_ids = []

    # Leaderboard management
    def get_leaderboard_data(self) -> Tuple[List[List], Optional[int]]:
        """
        Return leaderboard data and the position of the current user.

        Returns:
            Tuple[List[List], Optional[int]], Optional[int]]:
                - A 2D list containing leaderboard data, each entry has rank, username, and score.
                - The rank of the current user. Returns None if the user is not found in the leaderboard.
        """
        user_data = self.db.get_leaderboard()
        user_data_2d = [
            [index + 1, entry["username"], entry["score"]]
            for index, entry in enumerate(user_data)
        ]
        self._leaderboard_data = user_data_2d
        user_rank = None
        for index, entry in enumerate(user_data):
            if entry.get("UID") == self._cur_UID:
                user_rank = index + 1
                break
        return user_data_2d, user_rank

    @property
    def leaderboard_data_reverse(self) -> List[List]:
        """Reverse the order of the leaderboard data and return it."""
        self._leaderboard_data = self._leaderboard_data[::-1]
        return self._leaderboard_data

    def push_user_scores(self) -> str:
        """
        Update the user scores and return a string representing the number of correct answers out of the total cards in the pack.

        Returns:
            str: The number of correct answers and revealed cards out of the total cards.
        """
        self.db.update_leaderboard(self._cur_UID, self._correct_card_ids)
        reveal_cards_count = 0
        for card in self._current_card_pack.cards_list:
            if card.question_type == "Reveal":
                reveal_cards_count += 1
        return f"{len(self._correct_card_ids) + reveal_cards_count }/{self.pack_cards_count}"

    # Binary tree demo
    def generate_tree(self, string: str, balanced_bool: bool) -> Dict[bool, str]:
        """
        Generate a binary search tree from a string of integers (seperated by commas).

        Arguments:
            string (str): String of integers, seperated by commas.
            balanced_bool (bool): Indicates whether to balance the tree.

        Returns:
            dict: A dictionary containing the result.
                - 'result' (bool): True if the tree was generated successfully, otherwise False.
                - 'err_msg' (str): Error message if tree was not generated.
        """
        result = {"result": False, "err_msg": ""}
        # Validating data entry
        string_list = string.split(",")
        if 2 <= len(string_list) <= 30:
            if all(self.validate_integer(term) for term in string_list):
                integers = [int(term) for term in string_list]
            else:
                result["err_msg"] = "Please only enter integers"
        else:
            result["err_msg"] = "Please enter betweeen 2 and 30 integers"
        if result["err_msg"]:
            return result
        # If validation passes, attempts to build tree
        try:
            self._tree = BinarySearchTree()
            # Calls to build balanced tree, if balanced_bool is True
            if balanced_bool:
                self._tree.build_balanced_tree(integers)
            else:
                self._tree.build_tree(integers)
            # Updates the most recent file path
            self._prev_file_path = self._tree.render_as_image()
            result["result"] = True
        except Exception as error:
            result["err_msg"] = error
        return result

    def resize_image(self, encode_format: str = "PNG") -> bytes:
        """
        Resize an image and encode it into bytes.

        Arguments:
            encode_format (str, optional): The encoding format for the image. Defaults to "PNG".

        Returns:
            bytes: The byte representation of the resized image.
        """
        image = Image.open(self._prev_file_path)
        image_size = image.size
        multiple = 500 / max(image_size)
        new_image = image.resize([int(size * multiple) for size in image_size])
        with BytesIO() as buffer:
            new_image.save(buffer, format=encode_format)
            data = buffer.getvalue()
        return data

    def add_tree_node(self, new_node: str) -> Union[str, None]:
        """
        Add a node to existing binary tree.
            - Regenerate image if added.
            - Return error message (str) if new_node isn't valid.
        """
        if not new_node or not self.validate_integer(new_node):
            return "Please enter an integer"
        self._tree.add_node(int(new_node))
        self._prev_file_path = self._tree.render_as_image()

    def get_traversal_order(self, order_str: str) -> str:
        """
        Get a specific traversal order of the current binary search tree.

        Args:
            order_str (str): The traversal order ("preorder", "postorder", "inorder").

        Returns:
            str: A string with the traversal order.
        """
        traversal_functions = {
            "preorder": self._tree.pre_order_traversal,
            "postorder": self._tree.post_order_traversal,
            "inorder": self._tree.in_order_traversal,
        }
        traversal_order = traversal_functions[order_str]()
        traversal_order = ", ".join(str(integer) for integer in traversal_order)
        return traversal_order

    # Queues demo
    def initialise_queue(self):
        self._queue = Queue(self._queue_max_size)

    @property
    def queue_max_size(self) -> int:
        """Return the active queues max size."""
        return self._queue_max_size

    def switch_queue(self, queue_type: str) -> List[str]:
        """Updates the queue object, dependent on a string input."""
        if queue_type == "queue":
            self._queue = Queue(self._queue_max_size)
        if queue_type == "priority":
            self._queue = PriorityQueue(self._queue_max_size)
        if queue_type == "circular":
            self._queue = CircularQueue(self._queue_max_size)
        if queue_type == "stack":
            self._queue = Stack(self._queue_max_size)
        return self._queue.screen_elements

    @staticmethod
    def _create_queue_item() -> str:
        """Generate a random string with 3 leading integers."""
        with open("assets/town_names.txt", "r") as file:
            town_names = [line.strip() for line in file]
        name = random.choice(town_names)
        digits = "".join(map(str, [random.randint(0, 9) for _ in range(3)]))
        return f"{digits}-{name}"

    def get_queue(self) -> List[str]:
        """Return the queue contents as a list."""
        queue_contents = self._queue.queue
        if all(isinstance(item, tuple) and len(item) == 2 for item in queue_contents):
            return [item[1] for item in queue_contents]
        return queue_contents

    def queue_enqueue(self) -> Union[bool, T]:
        """
        Enqueue an item to the active queue.

        Returns:
            - False (bool) if failed to enqueue.
            otherwise,
            - item (str) if enqueued.
        """
        item = self._create_queue_item()
        return self._queue.enqueue(item)

    def queue_push(self) -> Union[bool, T]:
        """
        Push an item to the active stack.

        Returns:
            - False (bool) if failed to push.
            otherwise,
            - item (str) if pushed successfully.
        """
        item = self._create_queue_item()
        return self._queue.push(item)

    def queue_dequeue(self) -> Union[bool, T]:
        """
        Dequeue an item from the active queue.

        Returns:
            - False (bool) if failed to dequeue.
            otherwise,
            - (str) of item if dequeued.
        """
        return self._queue.dequeue()

    def queue_pop(self) -> Union[bool, T]:
        """
        Pop an item from the active stack.

        Returns:
            - False (bool) if failed to pop.
            otherwise,
            - (str) of item if popped.
        """
        return self._queue.pop()

    def queue_is_full(self) -> bool:
        """Check if active queue is full."""
        return self._queue.is_full()

    def queue_is_empty(self) -> bool:
        """Check if active queue is empty."""
        return self._queue.is_empty()

    def queue_peek(self) -> Union[bool, T]:
        """
        Get the top item in the active queue.

        Returns:
            - False (bool) if queue is empty.
            otherwise,
            - (str) of top item.
        """
        return self._queue.peek()

    def queue_size(self) -> int:
        """Return the current size of the queue."""
        return self._queue.size()

    def queue_front(self) -> int:
        """Return the value of the front pointer."""
        return self._queue.front

    def queue_rear(self) -> int:
        """Return the value of the rear pointer."""
        return self._queue.rear

    def queue_rear_element(self) -> Union[bool, T]:
        """
        Return the current rear element in a circular queue.

        Returns:
            - False (bool) if the queue is empty.
            otherwise,
            - (str) of rear item.
        """
        return self._queue.rear_item()

    # Graphs demo
    def generate_graph_from_matrix_string(
        self, adj_matrix_str: str, filename: str = "graph_demo"
    ) -> Union[str, bool]:
        """
        Generate a graph visualisation from an adjacency matrix string.

        Arguments:
            adj_matrix_str (str): The adjacency matrix string.
            filename (str, optional): The filename to save the graph visualisation. Defaults to "graph_demo".

        Returns:
            Union[str, bool]: String with an error message, otherwise True if the graph was successfully generated.
        """
        # Check for data input and format to list
        if not adj_matrix_str:
            return "Please fill the input field."
        adj_matrix_str = adj_matrix_str.replace(" ", "")
        values = adj_matrix_str.split(",")
        # Check for non-integer values
        if any(not self.validate_integer(value) for value in values):
            return "Please ensure to follow the suggested formatting, non-integer values were found."
        # Check if the length of values is a perfect square
        side_length = int(np.sqrt(len(values)))
        if side_length**2 != len(values):
            return "Invalid adjacency matrix, number of elements does not form a square"
        # Convert the values to integers
        adj_list = list(map(int, values))
        # Create adjacency matrix
        adj_matrix = [
            adj_list[i : i + side_length] for i in range(0, len(adj_list), side_length)
        ]
        self._prev_file_path = GraphVisualiser.save_graph_from_adjacency_matrix(
            adj_matrix, filename
        )
        self._adj_matrix = adj_matrix
        return True

    def generate_graph_from_adjacency_list(self) -> Union[str, bool]:
        """
        Generate graph image using current adjacency list and store the file path.

        Returns:
            Union[str, bool]: True if graph is generated, string for user if validation fails.
        """
        if not self._adjacency_list:
            return "Please add a node first."
        self._prev_file_path = GraphVisualiser.save_graph_from_adjacency_list(
            self._adjacency_list
        )
        return True

    def add_adjacency_node(self, node: str) -> Union[str, bool]:
        """
        Add a node to the active adjacency list.

        Arguments:
            node (str): Node identifier for new node.

        Returns:
            Union[str, bool]: True if node is added, otherwise string if validation isn't passed (message for user).
        """
        # Validation
        if not node:
            return "Please enter a value for the node."
        if not 1 <= len(node) <= 3:
            return "Please enter a value between 1 and 3 characters in length."
        if node in self._adjacency_list:
            return "A node already exists with this name."
        # Creating the key in adjacency_list
        self._adjacency_list[node] = []
        return True

    def add_edge_adjacency_list(
        self, node1: str, node2: str, directed_graph: bool = False
    ) -> Union[str, bool]:
        """
        Add an edge to the active adjacency list.

        Arguments:
            node1 (str): The first node of the edge.
            node2 (str): The second node of the edge.
            directed_graph (bool, optional): Whether the graph is directed or not. Defaults to False.

        Returns:
            Union[str, bool]: Either a string indicating an error message, or True if the edge was successfully added.
        """
        # Validate node1 and node2 exist
        if node1 not in self._adjacency_list or node2 not in self._adjacency_list:
            return "Please choose two nodes using the dropdown menus."
        # Check that edge won't generate a self-loop
        if node1 == node2:
            return "Graph does not support self-loops"
        # Check if the edge already exists
        if node2 in self._adjacency_list[node1] or (
            not directed_graph and node1 in self._adjacency_list[node2]
        ):
            return "Edge already exists."
        # Add edges
        self._adjacency_list[node1].append(node2)
        if not directed_graph:
            self._adjacency_list[node2].append(node1)
        return True

    @property
    def adjacency_matrix_table_str(self) -> str:
        """Return the current adjacency list or adjacency matrix as a string representation of an adjacency matrix."""
        # Adjacency matrix
        if self._adj_matrix:
            num_rows = len(self._adj_matrix)
            num_cols = len(self._adj_matrix[0]) if num_rows > 0 else 0
            matrix_string = ""
            # Add column headers
            matrix_string += (
                "   " + " ".join([f"N{i+1}" for i in range(num_cols)]) + "\n"
            )
            for i in range(num_rows):
                row = f"N{i+1} "
                for j in range(num_cols):
                    row += str(self._adj_matrix[i][j]) + " "
                # Add row to matrix string
                matrix_string += row.strip() + "\n"
            return matrix_string
        # Adjacency list
        elif self._adjacency_list:  # If adjacency list exists
            nodes = sorted(self._adjacency_list.keys())
            matrix_string = ""
            # Add column headers
            matrix_string += "   " + " ".join(nodes) + "\n"
            for node in nodes:
                row = node + " "
                for adj_node in nodes:
                    if adj_node in self._adjacency_list[node]:
                        row += "1 "
                    else:
                        row += "0 "
                # Add row to matrix string
                matrix_string += row.strip() + "\n"
            return matrix_string

    @property
    def adjacency_node_names(self) -> List[str]:
        """Return a list of all node names in the current adjacency list."""
        return list(self._adjacency_list.keys())

    def clear_adjacency_list(self) -> None:
        self._adjacency_list = {}

    # Universal data validation
    def validate_integer(self, term) -> bool:
        """Validate if a term can be translated to an integer."""
        try:
            int(term)
            return True
        except ValueError:
            return False
