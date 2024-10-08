from pathlib import Path
import sqlite3
import bcrypt
import string
import random
from typing import Union, Dict, List, Tuple

"""
Handles all database requests with parameterised SQL
"""


class Database:
    def __init__(self, path: Path) -> None:
        """
        Initialises a database object, defining it's directory

        Arguments:
            path (Path): Database file path
        """
        self._database_path = path

    # Database management
    def _populate_tables(self) -> None:
        """
        Internal method to ensure the Topics table is correctly populated.

        Reads SQL commands from the 'populate.sql' and compares the number of
        entities in the Topics table with the number of lines in the SQL file.
        If the counts do not match, it re-populates the 'Topics' table.
        """
        # Retrieve SQL commands and line count from populate.sql
        with open(Path.cwd() / "database" / "populate.sql", "r") as sql_file:
            sql_commands = sql_file.read()
            sql_file.seek(
                0
            )  # Cursor needs resetting to start of file, or line_count is incorrect
            line_count = sum(1 for line in sql_file)
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Topics;")
        entity_count = cur.fetchone()[0]
        # If topic count is not accurate to populate.sql
        if entity_count != line_count:
            cur.execute("DELETE FROM Topics;")
            cur.executescript(sql_commands)
        conn.commit()
        cur.close()
        conn.close()

    def check_database(self) -> None:
        """Create database and tables if they don't exist"""
        sql_file_path = Path.cwd() / "database" / "check_study_tool_db.sql"
        try:
            with open(sql_file_path, "r") as sql_file:
                qry = sql_file.read()
            conn = sqlite3.connect(self._database_path)
            cur = conn.cursor()
            cur.executescript(qry)
            cur.close()
            conn.close()
            self._populate_tables()
        except Exception as err:
            print(err.args)
            exit()

    # Account management
    def _hash(self, password: str) -> bytes:
        """
        Hash and salt a password.

        Arguments:
            password (str): Plaintext password.

        Returns:
            bytes: The salted and hashed password, encoded as bytes.
        """
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_password

    def _auth_password(self, inp_password: str, hashed_password: bytes) -> bool:
        """
        Authenticate a password, comparing in with a hashed password.

        Arguments:
            inp_password (str): Plaintext password entered by the user.
            hashed_password (bytes): Hashed and salted password from database.

        Returns:
            bool: True if the password is authenticated, False otherwise.
        """
        if bcrypt.checkpw(inp_password.encode("utf-8"), hashed_password):
            return True
        else:
            return False

    def _val_create_username(self, username: str) -> str:
        """
        Validate that a username is unique in the database.

        Arguments:
            username (str): The username being validated.

        Returns:
            str: An error message indicating whether the username is duplicate.
                If the username is available, returns an empty string.
        """
        err_str = ""
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT Username FROM Users WHERE Username COLLATE NOCASE = ?;",
            (username,),
        )
        if cur.fetchone():
            err_str = "Username is already in use."
        cur.close()
        conn.close()
        return err_str

    def _val_create_email(self, email: str) -> str:
        """
        Validate that an email is unique in the database.

        Arguments:
            email (str): The email being validated.

        Returns:
            str: An error message indicating whether the email is duplicate.
                If the email is available, returns an empty string.
        """
        err_str = ""
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT Email FROM Users WHERE Email = ?;", (email,))
        if cur.fetchone() != None:
            err_str = "Email address is already in use."
        cur.close()
        conn.close()
        return err_str

    def _val_create_credentials(self, username: str, email: str) -> dict:
        """
        Validate account creation by calling class functions.

        Arguments:
            username (str): Username from user input
            email (str): Email from user input

        Returns:
            dict: A dictionary containing validation outcome.
                - 'result' (bool): True if the account can be created, False if validation fails.
                - 'username_err_list' (list): A list of relevant validation errors for the username.
                - 'email_err_list' (list): A list of relevant validation errors for the email.
        """
        err_list = []
        err_list.extend(
            (
                self._val_create_username(username),
                self._val_create_email(email),
            )
        )
        results_dict = {
            "result": False,
            "username_err": err_list[0],
            "email_err": err_list[1],
        }
        if not any(err_list):
            results_dict["result"] = True
        return results_dict

    def get_first_name(self, UID) -> str:
        """Return a user's first name, using a UID"""
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT FirstName FROM Users WHERE UID = ?;", (UID,))
        result = cur.fetchone()
        first_name = result["FirstName"]
        cur.close()
        conn.close()
        return first_name

    def auth_login(
        self, username: str, inp_password: str
    ) -> Dict[str, Union[bool, int, str]]:
        """
        Authenticate user login by comparing user input to entities in the database.

        Arguments:
            username (str): Username entered by the user.
            inp_password (str): Password entered by the user.

        Returns:
            Dictionary containing authentication result and additional information:
                - auth (bool): True if the login is successful, otherwise False.
                - UID (int): The UID associated with the username (if the login is successful, otherwise None).
                - err_msg (str): Error message if a login fails, for displaying to the user.
        """
        auth_result = {"auth": False, "UID": None, "err_msg": ""}
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # Check for existence of username in Users
        cur.execute(
            "SELECT UID FROM Users WHERE Username COLLATE NOCASE = ?;", (username,)
        )
        entity = cur.fetchone()
        # If username doesn't exist for any entity
        if entity == None:
            auth_result["err_msg"] = "Username is not associated\nwith an account."
        # If username belongs to an entity, authenticate password
        else:
            UID = entity["UID"]
            cur.execute("SELECT Password FROM Credentials WHERE UID = ?;", (UID,))
            if self._auth_password(inp_password, cur.fetchone()["Password"]):
                auth_result["auth"], auth_result["UID"] = True, UID
            else:
                auth_result["err_msg"] = "Incorrect password,\nplease try again."
        cur.close()
        conn.close()
        return auth_result

    def create_account(
        self,
        inp_username: str,
        inp_password: str,
        inp_first_name: str,
        inp_email: str,
        address: dict,
    ) -> Dict[str, Union[bool, List[str]]]:
        """
        Insert a new user into database if validation passes.

        Arguments:
            inp_username (str): Username from user input.
            inp_password (str): Password from user input.
            inp_first_name (str): First name from user input.
            inp_email (str): Email from user input.
            address (dict): Address retrieved from address_fetcher through data_handler

        Returns:
            Dictionary containing the outcome of the account creation:
                - Result (bool): True if the account was created successfully, False if validation fails.
                - username_err_list (List[str]): List of relevant validation errors for the username.
                - email_err_list (List[str]): List of relevant validation errors for the email.
        """
        results_dict = self._val_create_credentials(inp_username, inp_email)
        if results_dict["result"]:
            try:
                conn = sqlite3.connect(self._database_path)
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Users (Username, FirstName, Email) VALUES (?,?,?);",
                    (inp_username, inp_first_name, inp_email),
                )
                cur.execute(
                    "INSERT INTO Credentials (UID, Password) VALUES (?,?);",
                    (cur.lastrowid, self._hash(inp_password)),
                )
                cur.execute(
                    "INSERT INTO Addresses (UID, Postcode, City, Country) VALUES (?,?,?,?);",
                    (
                        cur.lastrowid,
                        address["postcode"],
                        address["city"],
                        address["country"],
                    ),
                )
                conn.commit()
                cur.close()
                conn.close()
            except Exception as error:
                results_dict = {"result": False, "err_msg": error}
        return results_dict

    # Study notes management
    def get_topics_rows(self) -> List[Dict[str, Union[str, bool]]]:
        """
        Retrieve a list of dictionaries containing information about all entities in the Topics table.

        Returns:
            List of dictionaries, each containing:
                - 'topic_name' (str): The name of the topic.
                - 'topic_id' (str): The ID of the topic.
                - 'theory_directory' (Path): The directory path to the theory contents.
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Topics;")
        topic_entities = cur.fetchall()
        cur.close()
        conn.close()
        topic_dicts = []
        for entity in topic_entities:
            topic_dicts.append(
                {
                    "topic_name": entity["TopicName"],
                    "topic_id": entity["TopicID"],
                    "theory_directory": Path.cwd()
                    / Path(*entity["TopicContents"].split("/")),
                }
            )
        return topic_dicts

    @property
    def topics_list(self) -> List[str]:
        """
        Property method returning a list of topic names.

        Returns:
            list[str]: List of topic names.
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT TopicName FROM Topics;")
        entities = cur.fetchall()
        cur.close()
        conn.close()
        return [topic for topic in entities]

    def complete_topic(self, UID: int, topic_id: int) -> None:
        """
        Mark a topic as completed for a user by inserting into the CompletedTopics table,
        provided the data isn't duplicate.

        Arguments:
            UID: User's ID.
            topic_id: TopicID.
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # Check if the entity is not duplicate
        cur.execute(
            "SELECT COUNT(*) FROM CompletedTopics WHERE UID = ? AND TopicID = ?;",
            (UID, topic_id),
        )
        # Inserting entity if it's unique
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO CompletedTopics (UID, TopicID) VALUES (? , ?);",
                (UID, topic_id),
            )
            conn.commit()
        cur.close()
        conn.close()

    def get_completed_topics(self, UID: int) -> List[str]:
        """
        Return a list of topic names a user has completed

        Arguments:
            UID: Users ID.

        Returns:
            list[str]: List of topic names
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            """
                    SELECT 
                        Topics.TopicName
                    FROM
                        Topics
                    INNER JOIN
                        CompletedTopics ON Topics.TopicID = CompletedTopics.TopicID
                    WHERE
                        CompletedTopics.UID = ?; """,
            (UID,),
        )
        entities = cur.fetchall()
        cur.close()
        conn.close()
        return [topic["TopicName"] for topic in entities]

    def get_theory_path(self, topic_id: int) -> str:
        """
        Return the subpath for theory contents.

        Arguments:
            topic_id (int): The ID of the topic to search for.

        Returns:
            str: Subpath to the JSON file containing the topic's study pages.
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT TopicContents FROM Topics WHERE TopicID = ?", (topic_id,))
        return cur.fetchone()[0]

    # Flashcard management
    def _gen_share_id(self, length: int) -> str:
        """
        Generate a unique shareID for a flashcard pack.

        Arguments:
            length (int): The length of the generated shareID.

        Returns:
            str: Unique shareID.
        """
        unique = False
        characters = string.ascii_letters + string.digits
        while unique == False:
            share_id = "".join(random.choice(characters) for i in range(length))
            conn = sqlite3.connect(self._database_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM CardPacks WHERE ShareID = ?;", (share_id,)
            )
            if cur.fetchone()[0] == 0:
                unique = True
            cur.close()
            conn.close()
        return share_id

    def get_user_library(self, UID: int) -> List[Dict[str, int]]:
        """
        Retrieves the flashcard library of a user.

        Argumnets:
            UID: User's ID.

        Returns:
            List of dictionaries, each containing:
                - 'pack_name' (str): The name of the flashcard pack.
                - 'pack_id' (int): The ID of the flashcard pack.
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 
                UserLibraries.PackID,
                CardPacks.PackName
            FROM
                UserLibraries
            INNER JOIN
                CardPacks ON UserLibraries.PackID=CardPacks.PackID
            WHERE 
                UserLibraries.UID = ?;
            """,
            (UID,),
        )
        user_library = cur.fetchall()
        cur.close()
        conn.close()
        if not user_library:
            return []
        flashcard_packs_list = []
        for pack in user_library:
            flashcard_packs_list.append(
                {"pack_name": pack["PackName"], "pack_id": pack["PackID"]}
            )
        return flashcard_packs_list

    def download_pack(self, inp_share_id: str, UID: int) -> Dict[bool, str]:
        """
        Add a flashcard pack to a user's library by inserting a new entity in UserLibraries table.

        Arguments:
            inp_share_id (str): ShareID from user input.
            UID (int): User's ID.

        Returns:
            Dictionary with result information:
                - 'result' (bool): False if the ShareID does not exist, True if the pack is added.
                - 'err_msg' (str): Contains appropriate error message for the user.
        """
        result = {"result": False, "err_msg": ""}
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT PackID FROM CardPacks WHERE ShareID = ?;", (inp_share_id,))
        pack_id = cur.fetchone()
        if pack_id:
            pack_id = pack_id[0]
            cur.execute(
                "SELECT COUNT(*) FROM UserLibraries WHERE UID = ? AND PackID = ?;",
                (UID, pack_id),
            )
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO UserLibraries (UID, PackID) VALUES (?, ?);",
                    (UID, pack_id),
                )
                conn.commit()
                result["result"] = True
            else:
                result["err_msg"] = "You already have this pack."
        else:
            result["err_msg"] = "ShareID does not exist."
        cur.close()
        conn.close()
        return result

    def get_share_id(self, PackID: int) -> str:
        """
        Retrieve the ShareID of a card pack.

        Arguemnts:
            PackID (int): PackID of card pack

        Returns:
            str: ShareID of pack
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT ShareID FROM CardPacks WHERE PackID = ?;", (PackID,))
        share_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return share_id

    def create_flashcard_pack(
        self, pack_name: str, cards_list: list[dict], UID: int
    ) -> None:
        """
        Insert entities into CardPacks, Cards and CardLocations tables.

        Arguments:
            pack_name (str): Name of the pack (user input).
            cards_list (list[dict]): List of dictionaries containing card data.
                - Dictionaries formatted as: {"question": str, "answer": str, "points": int, "question_type": str}.
            UID (int): User ID to be linked to the pack.
        """
        share_id = self._gen_share_id(6)
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO CardPacks (UID, PackName, ShareID) VALUES (?, ?, ?);",
            (UID, pack_name, share_id),
        )
        cur.execute("SELECT PackID FROM CardPacks WHERE ShareID = ?;", (share_id,))
        pack_id = cur.fetchone()["PackID"]
        card_id_list = []
        for card in cards_list:
            cur.execute(
                "SELECT CardID FROM Cards WHERE Question = ? AND Answer = ? AND Points = ? AND QuestionType = ?;",
                (
                    card["question"],
                    card["answer"],
                    card["points"],
                    card["question_type"],
                ),
            )
            duplicate_card = cur.fetchone()
            if duplicate_card:
                card_id_list.append(duplicate_card["CardID"])
            else:
                cur.execute(
                    "INSERT INTO Cards (Question, Answer, Points, QuestionType) VALUES (?, ?, ?, ?);",
                    (
                        card["question"],
                        card["answer"],
                        card["points"],
                        card["question_type"],
                    ),
                )
                card_id_list.append(cur.lastrowid)
        for card_id in card_id_list:
            cur.execute(
                "INSERT INTO CardLocations (PackID, CardID) VALUES (?, ?);",
                (pack_id, card_id),
            )
        cur.execute(
            "INSERT INTO UserLibraries (UID, PackID) VALUES (?, ?);", (UID, pack_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def delete_card_pack(self, pack_id: int, UID: int) -> str:
        """
        Delete a card pack and associated entities.
            - Remove entities in Cards when they're not in any other packs.
            - Remove entities in CardLocations for matching PackID.
            - Remove entities in Leaderboard for matching CardIDs
            - Remove entities in UserLibraries for matching PackID.
            - Remove entities in CardPacks for matching PackID

        Arguments:
            pack_id (int): PackID for CardPacks entity to delete.
            UID (int): UID of user for confirming they are the owner of the pack.

        Returns:
            str: Message containing the deletion result
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # Check if user owns card pack
        cur.execute(
            "SELECT COUNT(*) FROM CardPacks WHERE PackID = ? AND UID = ?;",
            (pack_id, UID),
        )
        # If user owns card pack
        if cur.fetchone()[0] == 1:
            _, card_list = self.get_pack_data(pack_id)
            for card in card_list:
                # Check how many packs the card exists in
                cur.execute(
                    "SELECT COUNT(*) FROM CardLocations WHERE CardID = ?;",
                    (card["card_id"],),
                )
                # Delete the card if it only exists in the pack being deleted
                exists_once = False
                if cur.fetchone()[0] == 1:
                    cur.execute(
                        "DELETE FROM Cards WHERE CardID = ?;", (card["card_id"],)
                    )
                    exists_once = True
                # Delete entity in CardLocations, bridging the Card to the CardPack entity
                cur.execute(
                    "DELETE FROM CardLocations WHERE CardID = ? AND PackID = ?;",
                    (card["card_id"], pack_id),
                )
                # Delete entity in Leaderboard if the will no longer exist
                if exists_once:
                    cur.execute(
                        "DELETE FROM Leaderboard WHERE CardID = ?;", (card["card_id"],)
                    )
            # Remove the card pack from all user libraries
            cur.execute("DELETE FROM UserLibraries WHERE PackID = ?;", (pack_id,))
            # Delete the CardPacks entity
            cur.execute("DELETE FROM CardPacks WHERE PackID = ?;", (pack_id,))
            result_str = "Successfully deleted card pack."
        else:
            result_str = "Failed to delete, you are not the owner of this pack."
        conn.commit()
        cur.close()
        conn.close()
        return result_str

    def get_pack_data(
        self, pack_id: int
    ) -> Tuple[str, List[Dict[str, Union[int, str]]]]:
        """
        Retrieve data for a flashcard pack.

        Arguments:
            pack_id (int): PackID of the flashcard pack.

        Returns:
            A tuple containing the pack name and a list of dictionaries representing
            the cards in the pack. Each dictionary contains the following keys:
            - 'card_id': (int) CardID of the card.
            - 'question': (str) Question of the card.
            - 'answer': (str) Answer of the card.
            - 'question_type': (str) Type of the question.
            - 'points': (int) Points assigned to the card.
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT PackName FROM CardPacks WHERE PackID = ?", (pack_id,))
        pack_name = cur.fetchone()[0]
        cur.execute(
            "SELECT Cards.* FROM Cards INNER JOIN CardLocations ON Cards.CardID = CardLocations.CardID WHERE CardLocations.PackID = ?;",
            (pack_id,),
        )
        cards_table = cur.fetchall()
        cur.close()
        conn.close()
        cards_list = []
        for row in cards_table:
            cards_list.append(
                {
                    "card_id": row["CardID"],
                    "question": row["Question"],
                    "answer": row["Answer"],
                    "question_type": row["QuestionType"],
                    "points": row["Points"],
                }
            )
        return pack_name, cards_list

    # Leaderboard management
    def get_leaderboard(self) -> List[Dict[str, Union[int, str]]]:
        """
        Retrieve the leaderboard data.

        Returns:
            A list of dictionaries, each dictionary represents a user on the leaderboard, ordered by total score.
            Each dictionary contains the following keys:
            - 'UID': (int) User ID.
            - 'username': (str) Username.
            - 'score': (int) Total score.
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                U.UID,
                U.Username,
                SUM(C.Points) AS TotalPoints
            FROM 
                Users U
            INNER JOIN
                Leaderboard L ON U.UID = L.UID
            INNER JOIN
                Cards C ON L.CardID = C.CardID
            GROUP BY 
                U.UID, U.Username
            ORDER BY 
                TotalPoints DESC;
            """
        )
        leaderboard = cur.fetchall()
        cur.close()
        conn.close()
        leaderboard_list = []
        for row in leaderboard:
            leaderboard_list.append(
                {
                    "UID": row["UID"],
                    "username": row["Username"],
                    "score": row["TotalPoints"],
                }
            )
        return leaderboard_list

    def update_leaderboard(self, UID: int, card_ids: List[int]) -> None:
        """
        Updates the leaderboard table when new cards are completed.

        Arguments:
            UID (int): The ID of the user completing the cards.
            card_list (list[int]): A list of card IDs completed by the user.
        """
        conn = sqlite3.connect(self._database_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        for card_id in card_ids:
            # If points 0, don't add to leaderboard
            cur.execute(
                "SELECT Count(*) FROM Cards WHERE CardID = ? AND Points = 0;",
                (card_id,),
            )
            if cur.fetchone()[0] == 0:
                pass
            # Check for duplicate entities
            cur.execute(
                "SELECT COUNT(*) FROM Leaderboard WHERE UID = ? AND CardID = ?;",
                (UID, card_id),
            )
            if cur.fetchone()[0] == 0:
                cur.execute(
                    "INSERT INTO Leaderboard (UID, CardID) VALUES (?, ?);",
                    (UID, card_id),
                )
        conn.commit()
        cur.close()
        conn.close()
