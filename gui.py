import PySimpleGUI as sg
from pathlib import Path
from data_handler import DataHandler
from typing import List, Any, Union

"""
Displays the GUI
"""


class GUI:
    def __init__(self) -> None:
        """
        Initialise a GUI object, creating the DataHandler object for supporting
        functions and define variables for styling.
        """
        sg.theme("LightBlue3")
        # Styling
        self.font = "Minecraft"
        self.heading_size = 28
        self.heading_styling = (self.font, self.heading_size, "bold")
        self.body_size = 17
        self.button_text_size = 14
        self.small_text_size = 13
        self.text_error_colour = "DarkRed"
        self.text_success_colour = "green"
        self.large_sizer = 60
        self.medium_sizer = 20
        self.small_sizer = 15
        self.xsmall_sizer = 5
        self.medium_button_size = (30, 1)
        self.small_button_size = (14, 1)
        self.xsmall_button_size = (11, 1)
        self.drop_size = (28, 1)
        self.small_drop_size = (23, 1)
        self.multiline_size = (32, 5)
        self.data_handler = DataHandler()
        # Layout containing all screens within column elements
        self.layout = [
            [sg.VPush()],
            [
                sg.Column(
                    self.login_layout,
                    key="-login_layout-",
                    visible=True,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.create_account_layout,
                    key="-create_account_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.study_menu_layout,
                    key="-study_menu_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.flashcard_menu_layout,
                    key="-flashcard_menu_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.flashcard_creator_title_layout,
                    key="-flashcard_creator_title_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.flashcard_creator_cards_layout,
                    key="-flashcard_creator_cards_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.flashcard_viewer_layout,
                    key="-flashcard_viewer_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.trees_demo_layout,
                    key="-trees_demo_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.trees_view_layout,
                    key="-trees_view_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.queues_demo_layout,
                    key="-queues_demo_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.graphs_demo_layout,
                    key="-graphs_demo_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.graphs_view_layout,
                    key="-graphs_view_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.leaderboard_layout,
                    key="-leaderboard_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    self.topics_layout,
                    key="-topics_layout-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
            ],
            [sg.VPush()],
        ]
        self.window = sg.Window(
            "Study Tool",
            self.layout,
            resizable=True,
            element_justification="c",
            icon=Path.cwd() / "assets" / "cccc.ico",
            size=(950, 950),
        )

    """
    Individual screen layouts.
        - Element keys are formatted as: "-<screen_name>_<element_name>-".
    """

    @property
    def login_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Sign In", font=(self.heading_styling))],
            [sg.Sizer(0, self.large_sizer)],
            [sg.Text("Username", font=(self.font, self.body_size)), sg.Push()],
            [
                sg.InputText(
                    key="-login_username-",
                    size=self.medium_button_size,
                    font=(self.font, self.body_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [sg.Text("Password", font=(self.font, self.body_size)), sg.Push()],
            [
                sg.InputText(
                    key="-login_password-",
                    size=self.medium_button_size,
                    font=(self.font, self.body_size),
                    do_not_clear=False,
                    password_char="*",
                )
            ],
            [
                sg.Text(
                    "",
                    key="-login_error_message-",
                    text_color=self.text_error_colour,
                    enable_events=True,
                    font=(self.font, self.body_size),
                    justification="center",
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [
                sg.Button(
                    "Login",
                    key="-login_login-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.xsmall_sizer)],
            [
                sg.Button(
                    "Create account",
                    key="-login_create_account-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [
                sg.Button(
                    "Exit",
                    key="-login_exit-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def create_account_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Create Account", font=(self.heading_styling))],
            [sg.Sizer(0, self.large_sizer)],
            [sg.Text("Username", font=(self.font, self.body_size))],
            [
                sg.InputText(
                    key="-create_account_username-",
                    size=self.medium_button_size,
                    font=(self.font, self.body_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [sg.Text("Password", font=(self.font, self.body_size))],
            [
                sg.InputText(
                    key="-create_account_password-",
                    size=self.medium_button_size,
                    font=(self.font, self.body_size),
                    do_not_clear=False,
                    password_char="*",
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [sg.Text("First Name", font=(self.font, self.body_size))],
            [
                sg.InputText(
                    key="-create_account_first_name-",
                    size=self.medium_button_size,
                    font=(self.font, self.body_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [sg.Text("Email", font=(self.font, self.body_size))],
            [
                sg.InputText(
                    key="-create_account_email-",
                    size=self.medium_button_size,
                    font=(self.font, self.body_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [
                sg.Text("House number: ", font=(self.font, self.body_size)),
                sg.Sizer(70, 0),
                sg.InputText(
                    key="-create_account_house_number-",
                    size=self.xsmall_button_size,
                    font=(self.font, self.body_size),
                ),
            ],
            [
                sg.Text("Postcode: ", font=(self.font, self.body_size)),
                sg.Sizer(125, 0),
                sg.InputText(
                    key="-create_account_postcode-",
                    size=self.xsmall_button_size,
                    font=(self.font, self.body_size),
                ),
            ],
            [sg.Sizer(0, self.xsmall_sizer)],
            [
                sg.Text(
                    "",
                    key="-create_account_error_message-",
                    text_color=self.text_error_colour,
                    enable_events=True,
                    font=(self.font, self.small_text_size),
                    justification="center",
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [
                sg.Button(
                    "Create Account",
                    key="-create_account_create_account-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.xsmall_sizer)],
            [
                sg.Button(
                    "Back to login",
                    key="-create_account_login-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [
                sg.Button(
                    "Exit",
                    key="-create_account_exit-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def study_menu_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Study Topics", font=(self.heading_styling))],
            [
                sg.Text(
                    "Welcome back!",
                    key="-study_menu_greeting-",
                    font=(self.font, self.small_text_size),
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Text("Choose a Topic", font=(self.font, self.body_size)),
                sg.Sizer(80, 0),
                sg.Text(
                    "0% Revised",
                    key="-study_menu_revised_percent-",
                    enable_events=True,
                    font=(self.font, self.small_text_size),
                ),
            ],
            [
                sg.Drop(
                    self.data_handler.topics_list,
                    key="-study_menu_topics_drop-",
                    size=self.drop_size,
                    font=(self.font, self.body_size),
                    default_value="Queues",
                    readonly=True,
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Button(
                    "Study topic",
                    key="-study_menu_study-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.xsmall_sizer)],
            [
                sg.Button(
                    "Launch demo",
                    key="-study_menu_launch_demo-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [sg.Text("OR", font=(self.font, self.body_size))],
            [sg.Sizer(0, self.small_sizer)],
            [
                sg.Button(
                    "Flashcards",
                    key="-study_menu_flashcards-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.xsmall_sizer)],
            [
                sg.Button(
                    "Leaderboard",
                    key="-study_menu_leaderboard-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Logout",
                    key="-study_menu_logout-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def flashcard_menu_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Flashcards", font=(self.heading_styling))],
            [sg.Sizer(0, self.large_sizer)],
            [sg.Text("Choose a pack", font=(self.font, self.body_size))],
            [
                sg.Combo(
                    [],
                    key="-flashcard_menu_packs_drop-",
                    size=self.drop_size,
                    font=(self.font, self.body_size),
                    readonly=True,
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Button(
                    "Study pack",
                    key="-flashcard_menu_study_pack-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.xsmall_sizer)],
            [
                sg.Button(
                    "Share",
                    key="-flashcard_menu_share-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                ),
                sg.Button(
                    "Download",
                    key="-flashcard_menu_download-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                ),
            ],
            [sg.Sizer(0, self.xsmall_sizer)],
            [
                sg.Button(
                    "Delete pack",
                    key="-flashcard_menu_delete_pack-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [sg.Text("OR", font=(self.font, self.body_size))],
            [sg.Sizer(0, self.small_sizer)],
            [
                sg.Button(
                    "Create",
                    key="-flashcard_menu_create-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Button(
                    "Back",
                    key="-flashcard_menu_back-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def trees_demo_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Binary Tree Demo", font=(self.heading_styling))],
            [
                sg.Text(
                    "Please enter a list of integers, seperated with commas",
                    font=(self.font, self.small_text_size),
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [sg.Text("Integers for tree", font=(self.font, self.body_size)), sg.Push()],
            [
                sg.Multiline(
                    default_text="1,2,3,4,5,6",
                    key="-trees_demo_input-",
                    size=self.multiline_size,
                    font=(self.font, self.body_size),
                )
            ],
            [
                sg.Checkbox(
                    "Balanced tree",
                    key="-trees_demo_balanced_check-",
                    font=(self.font, self.small_text_size),
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Button(
                    "Generate",
                    key="-trees_demo_generate-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Button(
                    "Exit",
                    key="-trees_demo_exit-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def trees_view_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Binary Tree Demo", font=(self.heading_styling))],
            [
                sg.Text(
                    "Tree generated below! Try using the traversal menu and button",
                    font=(self.font, self.small_text_size),
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Frame(
                    "",
                    [
                        [
                            sg.Image(
                                key="-trees_view_image-",
                                background_color="white",
                                size=(530, 530),
                                pad=(5, 5),
                            )
                        ]
                    ],
                    background_color="black",
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Combo(
                    ["Inorder", "Preorder", "Postorder"],
                    default_value="Traversals",
                    key="-trees_view_traversals_drop-",
                    size=self.small_drop_size,
                    font=(self.font, self.body_size),
                    readonly=True,
                ),
                sg.Button(
                    "View traversal",
                    key="-trees_view_traverse-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                ),
            ],
            [sg.Sizer(0, self.xsmall_sizer)],
            [
                sg.Button(
                    "Add node",
                    key="-trees_view_add_node-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Back",
                    key="-trees_view_back-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def queues_demo_layout(self) -> List[List[Any]]:
        max_queue_size = self.data_handler.queue_max_size
        queue_column = [
            [
                sg.Frame(
                    layout=[
                        [
                            sg.Image(
                                "assets/blank_pointer.png",
                                key=f"-queue_demo_front_pointer_{i}-",
                                size=(16, 16),
                            ),
                            sg.Text(
                                "",
                                key=f"-queue_demo_queue_elem_{i}-",
                                size=(18, 1),
                                font=(self.font, self.body_size),
                                text_color="black",
                                enable_events=True,
                                background_color="white",
                            ),
                            sg.Image(
                                "assets/blank_pointer.png",
                                key=f"-queue_demo_rear_pointer_{i}-",
                                size=(16, 16),
                            ),
                        ]
                        for i in range(max_queue_size)
                    ],
                    title="Queue",
                    title_location="n",
                    border_width=2,
                    element_justification="c",
                    size=(310, 250),
                )
            ],
        ]
        queue_buttons_column = [
            [
                sg.Button(
                    "Enqueue",
                    key="-queue_demo_enqueue-",
                    font=(self.font, self.small_text_size),
                    size=(self.xsmall_button_size),
                ),
                sg.Button(
                    "Push",
                    key="-queue_demo_push-",
                    visible=False,
                    font=(self.font, self.small_text_size),
                    size=(self.xsmall_button_size),
                ),
            ],
            [
                sg.Button(
                    "Dequeue",
                    key="-queue_demo_dequeue-",
                    font=(self.font, self.small_text_size),
                    size=(self.xsmall_button_size),
                ),
                sg.Button(
                    "Pop",
                    key="-queue_demo_pop-",
                    visible=False,
                    font=(self.font, self.small_text_size),
                    size=(self.xsmall_button_size),
                ),
            ],
            [
                sg.Button(
                    "Peek",
                    key="-queue_demo_peek-",
                    font=(self.font, self.small_text_size),
                    size=(self.xsmall_button_size),
                )
            ],
            [
                sg.Button(
                    "isFull",
                    key="-queue_demo_isfull-",
                    font=(self.font, self.small_text_size),
                    size=(self.xsmall_button_size),
                )
            ],
            [
                sg.Button(
                    "isEmpty",
                    key="-queue_demo_isempty-",
                    font=(self.font, self.small_text_size),
                    size=(self.xsmall_button_size),
                )
            ],
            [
                sg.Button(
                    "Size",
                    key="-queue_demo_size-",
                    font=(self.font, self.small_text_size),
                    size=(self.xsmall_button_size),
                )
            ],
            [
                sg.Button(
                    "Rear",
                    key="-queue_demo_rear-",
                    visible=False,
                    font=(self.font, self.small_text_size),
                    size=(self.xsmall_button_size),
                )
            ],
        ]
        return [
            [sg.Text("Queues Demo", font=(self.heading_styling))],
            [
                sg.Text(
                    "Below is your queue!\nDropdown for queue types, use buttons for operations, and see full log at the base!",
                    font=(self.font, self.small_text_size),
                    justification="c",
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Text("Queue type: ", font=(self.font, self.body_size)),
                sg.Combo(
                    ["Circular", "Priority", "Stack", "Queue"],
                    default_value="Queue",
                    key="-queue_demo_queue_type_combo-",
                    size=self.small_button_size,
                    font=(self.font, self.body_size),
                    enable_events=True,
                    readonly=True,
                ),
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Column(queue_column, element_justification="c"),
                sg.Column(queue_buttons_column, element_justification="c"),
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Frame(
                    layout=[[sg.Output(size=(60, 5))]],
                    title="Log",
                    title_location="n",
                    border_width=2,
                    element_justification="c",
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Exit",
                    key="-queue_demo_exit-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def graphs_demo_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Graphs Demo", font=(self.heading_styling))],
            [
                sg.Text(
                    "Select an input format to create your graph",
                    font=(self.font, self.small_text_size),
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Text(
                    "Input format:",
                    font=(self.font, self.small_text_size),
                ),
                sg.Combo(
                    ["Adjacency matrix", "Adjacency list"],
                    default_value="Adjacency matrix",
                    key="-graphs_demo_input_type-",
                    size=self.small_drop_size,
                    font=(self.font, self.body_size),
                    readonly=True,
                    enable_events=True,
                ),
            ],
            [
                sg.Checkbox(
                    "Directed graph (effects new edges)",
                    key="-graphs_demo_directed_check-",
                    font=(self.font, self.small_text_size),
                    disabled=True,
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Text(
                    "Adjacency matrix",
                    font=(self.font, self.small_text_size),
                ),
                sg.Push(),
            ],
            [
                sg.Multiline(
                    default_text="0, 1, 0, 1, 0, 0, 0, 1, 0",
                    key="-graphs_demo_matrix_input-",
                    size=self.multiline_size,
                    font=(self.font, self.body_size),
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Frame(
                    "Nodes",
                    layout=[
                        [sg.VPush()],
                        [
                            sg.InputText(
                                key="-graphs_demo_node_input-",
                                size=self.medium_button_size,
                                font=(self.font, self.body_size),
                                disabled=True,
                            ),
                        ],
                        [sg.Sizer(0, self.small_sizer)],
                        [
                            sg.Button(
                                "Add node",
                                key="-graphs_demo_add_node-",
                                font=(self.font, self.button_text_size),
                                size=(self.small_button_size),
                                disabled=True,
                            ),
                        ],
                        [sg.VPush()],
                    ],
                    element_justification="c",
                    size=(250, 200),
                ),
                sg.Frame(
                    "Edges",
                    layout=[
                        [sg.VPush()],
                        [
                            sg.Combo(
                                [],
                                default_value="First node",
                                key="-graphs_demo_node_1-",
                                size=self.small_drop_size,
                                font=(self.font, self.body_size),
                                readonly=True,
                                disabled=True,
                            ),
                        ],
                        [sg.Sizer(0, self.small_sizer)],
                        [
                            sg.Combo(
                                [],
                                default_value="Second node",
                                key="-graphs_demo_node_2-",
                                size=self.small_drop_size,
                                font=(self.font, self.body_size),
                                readonly=True,
                                disabled=True,
                            )
                        ],
                        [sg.Sizer(0, self.small_sizer)],
                        [
                            sg.Button(
                                "Add edge",
                                key="-graphs_demo_add_edge-",
                                font=(self.font, self.button_text_size),
                                size=(self.small_button_size),
                                disabled=True,
                            ),
                        ],
                        [sg.VPush()],
                    ],
                    element_justification="c",
                    size=(250, 200),
                ),
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Generate graph",
                    key="-graphs_demo_generate_graph-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                ),
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Back",
                    key="-graphs_demo_back-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def graphs_view_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Graphs Demo", font=(self.heading_styling))],
            [
                sg.Text(
                    "Graph generated below!",
                    font=(self.font, self.small_text_size),
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Frame(
                    "",
                    [
                        [
                            sg.Image(
                                key="-graphs_view_image-",
                                background_color="white",
                                size=(530, 530),
                                pad=(5, 5),
                            )
                        ]
                    ],
                    background_color="black",
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "View adjacency matrix",
                    key="-graphs_view_matrix-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                ),
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Back",
                    key="-graphs_view_back-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def flashcard_creator_title_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Flashcard Creator", font=(self.heading_styling))],
            [
                sg.Text(
                    "Name your flashcard pack",
                    font=(self.font, self.small_text_size),
                    justification="c",
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [sg.Text("Pack name", font=(self.font, self.body_size)), sg.Push()],
            [
                sg.InputText(
                    key="flashcard_creator_title_name-",
                    size=self.medium_button_size,
                    font=(self.font, self.body_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [
                sg.Button(
                    "Set name",
                    key="-flashcard_creator_title_set_name-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.xsmall_sizer)],
            [
                sg.Button(
                    "Cancel",
                    key="-flashcard_creator_title_cancel-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
        ]

    @property
    def flashcard_creator_cards_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Card Creator", font=(self.heading_styling))],
            [
                sg.Text(
                    "Create your cards, selecting the question type from the drop-down box.\nWhen you are finished, press 'Save' to upload your pack!",
                    font=(self.font, self.small_text_size),
                    justification="c",
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Text("Question type", font=(self.font, self.body_size)),
                sg.Push(),
                sg.Text("Points", font=(self.font, self.body_size)),
            ],
            [
                sg.Combo(
                    ["Reveal", "Multiple choice", "Numerical"],
                    default_value="Multiple choice",
                    key="-flashcard_creator_cards_question_type-",
                    size=self.small_button_size,
                    font=(self.font, self.body_size),
                    enable_events=True,
                    readonly=True,
                ),
                sg.Push(),
                sg.Combo(
                    [0, 1, 2, 3],
                    default_value="0",
                    key="-flashcard_creator_cards_points-",
                    size=self.small_button_size,
                    font=(self.font, self.body_size),
                    enable_events=True,
                    readonly=True,
                ),
            ],
            [sg.Sizer(0, self.small_sizer)],
            [sg.Text("Prompt", font=(self.font, self.body_size)), sg.Push()],
            [
                sg.Multiline(
                    key="-flashcard_creator_cards_prompt-",
                    size=(45, 3),
                    font=(self.font, self.body_size),
                )
            ],
            [sg.Sizer(0, self.small_sizer)],
            [sg.Text("Answer", font=(self.font, self.body_size)), sg.Push()],
            [
                sg.Multiline(
                    key="-flashcard_creator_cards_answer-",
                    size=(45, 3),
                    font=(self.font, self.body_size),
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Text(
                    "Add answer [0/4]",
                    font=(self.font, self.small_text_size),
                    text_color="black",
                    key="-flashcard_creator_cards_total_choices-",
                ),
                sg.Button(
                    "+",
                    font=(self.font, self.small_text_size),
                    size=(self.small_button_size),
                    key="-flashcard_creator_cards_add_choice-",
                ),
            ],
            [
                sg.Checkbox(
                    "Correct answer?",
                    font=(self.font, self.small_text_size),
                    key="-flashcard_creator_cards_is_correct-",
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Add card",
                    key="-flashcard_creator_cards_add_card-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                ),
                sg.Button(
                    "Save",
                    key="-flashcard_creator_cards_save-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                ),
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Cancel",
                    key="-flashcard_creator_cards_cancel-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
        ]

    @property
    def flashcard_viewer_layout(self) -> List[List[Any]]:
        reveal_column = [
            [
                sg.Multiline(
                    default_text="",
                    key="-flashcard_viewer_reveal_field-",
                    size=(44, 5),
                    font=(self.font, self.body_size),
                    disabled=True,
                    do_not_clear=False,
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Toggle reveal",
                    key="-flashcard_viewer_reveal-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                ),
                sg.Button(
                    "Next",
                    key="-flashcard_viewer_next-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                ),
            ],
        ]
        numerical_column = [
            [
                sg.Multiline(
                    default_text="",
                    key="-flashcard_viewer_numerical_field-",
                    size=(44, 5),
                    font=(self.font, self.body_size),
                    do_not_clear=False,
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Submit",
                    key="-flashcard_viewer_submit_numerical-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]
        multiple_choice_column = [
            [
                sg.Frame(
                    "Options",
                    layout=[
                        [
                            sg.Text(
                                "[Answers]",
                                key="-flashcard_viewer_multiple_choice_field-",
                                font=(self.font, self.small_text_size),
                            )
                        ]
                    ],
                    size=(630, 150),
                    pad=(5, 5),
                )
            ],
            [
                sg.Text("Answer", font=(self.font, self.body_size)),
                sg.Combo(
                    [],
                    key="-flashcard_viewer_choice_drop-",
                    size=self.drop_size,
                    font=(self.font, self.body_size),
                    default_value=1,
                    readonly=True,
                ),
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Submit",
                    key="-flashcard_viewer_submit_multiple_choice-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]
        return [
            [
                sg.Text(
                    "Pack Name",
                    key="-flashcard_viewer_pack_name-",
                    font=(self.heading_styling),
                )
            ],
            [
                sg.Text(
                    "Card [-/Total]",
                    key="-flashcard_viewer_card_counter-",
                    font=(self.font, self.small_text_size),
                    justification="c",
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Frame(
                    "Prompt",
                    layout=[
                        [sg.VPush()],
                        [
                            sg.Text(
                                "[Prompt]",
                                key="-flashcard_viewer_prompt-",
                                font=(self.font, self.small_text_size),
                            )
                        ],
                        [sg.VPush()],
                    ],
                    size=(630, 150),
                    pad=(5, 5),
                    element_justification="c",
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Column(
                    reveal_column,
                    key="-flashcard_viewer_reveal_column-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    numerical_column,
                    key="-flashcard_viewer_numerical_column-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
                sg.Column(
                    multiple_choice_column,
                    key="-flashcard_viewer_multiple_choice_column-",
                    visible=False,
                    justification="c",
                    element_justification="c",
                ),
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Exit",
                    key="-flashcard_viewer_exit-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                )
            ],
        ]

    @property
    def leaderboard_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("Leaderboard", font=(self.heading_styling))],
            [
                sg.Text(
                    "Your current position: -",
                    font=(self.font, self.small_text_size),
                    justification="c",
                    key="-leaderboard_user_position-",
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Table(
                    values=[],
                    headings=["Rank", "Username", "Score"],
                    display_row_numbers=False,
                    auto_size_columns=False,
                    col_widths=[20, 35, 20],
                    justification="c",
                    key="-leaderboard_table-",
                    font=(self.font, self.small_text_size),
                    size=(10, 20),
                )
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Reverse order",
                    key="-leaderboard_reverse_order-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Button(
                    "Back",
                    key="-leaderboard_back-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
        ]

    @property
    def topics_layout(self) -> List[List[Any]]:
        return [
            [sg.Text("", font=(self.heading_styling), key="-topics_heading-")],
            [
                sg.Text(
                    "Current page: [1/-]",
                    font=(self.font, self.small_text_size),
                    justification="c",
                    key="-topics_page_number-",
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.pin(
                    sg.Frame(
                        "",
                        layout=[
                            [
                                sg.Image(
                                    key="-topics_image-",
                                    background_color="black",
                                    size=(0, 0),
                                    pad=(0, 0),
                                )
                            ]
                        ],
                        border_width=3,  # Adjust border width as needed
                        background_color="black",
                        pad=(5, 5),
                        key="-topics_image_border-",
                    )
                )
            ],
            [
                sg.Text(
                    "",
                    font=(self.font, self.small_text_size),
                    justification="l",
                    key="-topics_body-",
                    relief="ridge",
                    border_width=5,
                )
            ],
            [sg.Sizer(0, self.large_sizer)],
            [
                sg.Button(
                    "Previous",
                    key="-topics_previous-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                ),
                sg.Button(
                    "Next",
                    key="-topics_next-",
                    font=(self.font, self.button_text_size),
                    size=(self.small_button_size),
                ),
            ],
            [sg.Sizer(0, self.medium_sizer)],
            [
                sg.Button(
                    "Exit",
                    key="-topics_exit-",
                    font=(self.font, self.button_text_size),
                    size=(self.medium_button_size),
                )
            ],
        ]

    def _screen_switch(self, cur_screen_key: str, new_screen_key: str) -> None:
        """Change displayed layout, loading data when needed."""
        # Load % revised for study menu and greeting with first name
        if new_screen_key == "-study_menu_layout-":
            self.window["-study_menu_revised_percent-"].update(
                str(self.data_handler.calc_revised_percent) + "% Revised"
            )
            self.window["-study_menu_greeting-"].update(
                f"Welcome back {self.data_handler.cur_name}!"
            )
        # Load user library to combo box
        elif new_screen_key == "-flashcard_menu_layout-":
            self.window["-flashcard_menu_packs_drop-"].update(
                values=self.data_handler.user_library_list
            )
        # Load binary tree image
        elif new_screen_key == "-trees_view_layout-":
            self.window["-trees_view_image-"].update(
                data=self.data_handler.resize_image()
            )
        # Initialise a queue
        elif new_screen_key == "-queues_demo_layout-":
            self.data_handler.initialise_queue()
        # Load graph image
        elif new_screen_key == "-graphs_view_layout-":
            self.window["-graphs_view_image-"].update(
                data=self.data_handler.resize_image()
            )
        # Load card to flashcard viewer
        elif new_screen_key == "-flashcard_viewer_layout-":
            self.window["-flashcard_viewer_pack_name-"].update(
                self.data_handler.current_pack_name
            )
            self.window["-flashcard_viewer_card_counter-"].update(
                f"Card [1/{self.data_handler.pack_cards_count}]"
            )
            self.show_new_flashcard()
        # Load leaderboard
        elif new_screen_key == "-leaderboard_layout-":
            leaderboard_data, user_rank = self.data_handler.get_leaderboard_data()
            self.window["-leaderboard_table-"].update(values=leaderboard_data)
            self.window["-leaderboard_user_position-"].update(
                f"Your current position: {user_rank}"
            )
        # Load topic theory
        elif new_screen_key == "-topics_layout-":
            self.update_topic_page()
        # Switch screen
        self.window[cur_screen_key].update(visible=False)
        self.window[new_screen_key].update(visible=True)

    def show_queue_buttons(self, visible_keys: List[str]) -> None:
        """
        Update element visiblity for the queue demonstration screen.

        Arguments:
            visible_keys (List[str]): List of element keys to display.
        """
        all_keys = [
            "-queue_demo_enqueue-",
            "-queue_demo_dequeue-",
            "-queue_demo_push-",
            "-queue_demo_pop-",
            "-queue_demo_peek-",
            "-queue_demo_isfull-",
            "-queue_demo_isempty-",
            "-queue_demo_size-",
            "-queue_demo_rear-",
        ]
        # Hides elements not in visible_keys and vice versa
        for key in all_keys:
            if key in visible_keys:
                self.window[key].update(visible=True)
            else:
                self.window[key].update(visible=False)

    def show_new_flashcard(self) -> None:
        """
        Display a new flashcard to the user.

        Display the appropriate elements for the flashcard type and necessary information for the card.

        If the pack is finished:
            - Display the final score to the user.
            - Update the user's leaderboard scores in the database.
            - Return the user to the flashcard menu.
        """
        # Hide card-specific elements
        elements_to_hide = [
            "-flashcard_viewer_reveal_column-",
            "-flashcard_viewer_numerical_column-",
            "-flashcard_viewer_multiple_choice_column-",
        ]
        for element_key in elements_to_hide:
            self.window[element_key].update(visible=False)
        # Retrieve info on next card
        top_card = self.data_handler.next_card_info
        # If all cards have been answered
        if top_card is False:
            score = self.data_handler.push_user_scores()
            sg.Popup(
                f"You finished the pack!\nFinal score: {score}",
                title="Pack complete!",
                font=(self.font, self.small_text_size),
                text_color=self.text_success_colour,
            )
            self._screen_switch("-flashcard_viewer_layout-", "-flashcard_menu_layout-")
            return
        self.window["-flashcard_viewer_prompt-"].update(top_card["question"])
        # Displaying screen elements dependent on card type
        if top_card["question_type"] == "Reveal":
            self.window["-flashcard_viewer_reveal_column-"].update(visible=True)
        elif top_card["question_type"] == "Integer":
            self.window["-flashcard_viewer_numerical_column-"].update(visible=True)
        elif top_card["question_type"] == "Multiple Choice":
            # Updating choices drop (answering)
            numbered_answers = [
                f"{i+1}" for i, answer in enumerate(top_card["answer"]["all"])
            ]
            self.window["-flashcard_viewer_choice_drop-"].update(
                values=numbered_answers
            )
            # Displaying answer options (text)
            self.window["-flashcard_viewer_multiple_choice_field-"].update(
                self.data_handler.format_multiple_choice_options(top_card)
            )
            self.window["-flashcard_viewer_multiple_choice_column-"].update(
                visible=True
            )
        # Update card counter
        self.window["-flashcard_viewer_card_counter-"].update(
            f"Card [{self.data_handler.current_card_number}/{self.data_handler.pack_cards_count}]"
        )

    def flashcard_answer_result(self, result: Union[bool, str]) -> None:
        """
        Display the result of the users flashcard answer.

        Arguments:
            result (Union[bool, str]): The result of the flashcard answer.
        """
        if result == True:
            sg.Popup(
                "Correct!",
                title="Answer",
                font=(self.font, self.small_text_size),
                text_color=self.text_success_colour,
            )
        else:
            sg.Popup(
                f"Incorrect, the correct answer was:\n{result}",
                title="Answer",
                font=(self.font, self.small_text_size),
                text_color=self.text_error_colour,
            )

    def update_topic_page(self, next_page: bool = True) -> bool:
        """
        Update the topic page elements displayed contents.

        Parameters:
            next_page (bool, optional): Indicates whether to move to the next page. False will request the previous page. Defaults to True.

        Returns:
            bool: Returns True if the page is successfully updated (if there is a next/previous page), otherwise False.
        """
        page_data = self.data_handler.get_next_theory_page(next_page)
        # Returns False if there is no next/previous page
        if not page_data:
            return False
        # Updating GUI
        heading = page_data["heading"]
        page_number = page_data["page_number"]
        body = page_data["body"]
        image_dir = page_data.get("image_dir")
        self.window["-topics_heading-"].update(heading)
        self.window["-topics_page_number-"].update(
            f"Current page: [{page_number}/{self.data_handler.total_theory_pages}]"
        )
        self.window["-topics_body-"].update(body)
        # Displays an image, if a directory is present
        if not image_dir:
            self.window["-topics_image-"].update(visible=False)
            self.window["-topics_image_border-"].update(visible=False)
        else:
            self.window["-topics_image-"].update(filename=image_dir, visible=True)
            self.window["-topics_image_border-"].update(visible=True)
        return True

    def update_queue_display(
        self,
        queue_elements: List[Union[str, None]],
        front_index: int = 0,
        rear_index: int = -1,
    ) -> None:
        """
        Update the queue elements display in the GUI.

        Arguments:
            queue_elements (List[Union[str, None]]): The elements in the queue.
            front_index (int): The index of the front pointer. Defaults to 0.
            rear_index (int): The index of the rear pointer. Defaults to -1.
        """
        max_queue_size = self.data_handler.queue_max_size
        # Update the display for each element in the queue
        for i in range(max_queue_size):
            try:
                # Update the text for the queue element
                if queue_elements[i]:
                    self.window[f"-queue_demo_queue_elem_{i}-"].update(
                        queue_elements[i]
                    )
                else:
                    self.window[f"-queue_demo_queue_elem_{i}-"].update("")
            except:
                # If an exception occurs (index out of range), update with an empty string
                self.window[f"-queue_demo_queue_elem_{i}-"].update("")
            # Clear the front and rear pointers
            self.window[f"-queue_demo_front_pointer_{i}-"].update(
                filename="assets/blank_pointer.png"
            )
            self.window[f"-queue_demo_rear_pointer_{i}-"].update(
                filename="assets/blank_pointer.png"
            )
        # Display the front and rear pointers
        if front_index in range(max_queue_size):
            self.window[f"-queue_demo_front_pointer_{front_index}-"].update(
                filename="assets/right_arrow.png"
            )
        if rear_index in range(max_queue_size):
            self.window[f"-queue_demo_rear_pointer_{rear_index}-"].update(
                filename="assets/left_arrow.png"
            )

    def run(self) -> None:
        """Display the GUI, responding to events and passing values."""
        while True:
            event, values = self.window.read()

            # Close the GUI
            if (
                event == sg.WINDOW_CLOSED
                or event == "-login_exit-"
                or event == "-create_account_exit-"
            ):
                break

            # Login screen
            if self.window["-login_layout-"].Widget.winfo_ismapped():
                # Go to create account screen
                if event == "-login_create_account-":
                    self.window["-login_error_message-"].update("")
                    self._screen_switch("-login_layout-", "-create_account_layout-")
                # Attempt to login
                elif event == "-login_login-":
                    auth_result = self.data_handler.authenticate_user(
                        values["-login_username-"], values["-login_password-"]
                    )
                    if auth_result["auth"]:
                        self.window["-login_error_message-"].update("")
                        self._screen_switch("-login_layout-", "-study_menu_layout-")
                    else:
                        self.window["-login_error_message-"].update(
                            auth_result["err_msg"]
                        )

            # Create account screen
            elif self.window["-create_account_layout-"].Widget.winfo_ismapped():
                # Return to login screen
                if event == "-create_account_login-":
                    self.window["-create_account_error_message-"].update("")
                    self._screen_switch("-create_account_layout-", "-login_layout-")
                # Attempt to create account
                elif event == "-create_account_create_account-":
                    account_creation = False
                    result = self.data_handler.val_create_address(
                        values["-create_account_house_number-"],
                        values["-create_account_postcode-"],
                    )
                    if result["result"]:
                        address_label = result["address"]["label"]
                        confirm_address = sg.popup_yes_no(
                            f"Is this your address?\n{address_label}",
                            title="Confirm your address",
                            font=(self.font, self.small_text_size),
                        )
                        address_dict = result["address"]
                        if confirm_address == "Yes":
                            result = self.data_handler.create_account(
                                values["-create_account_username-"],
                                values["-create_account_password-"],
                                values["-create_account_first_name-"],
                                values["-create_account_email-"],
                                address_dict,
                            )
                            account_creation = result["result"]
                    if account_creation:
                        self.window["-create_account_error_message-"].update(
                            "Account successfully created!", text_color="green"
                        )
                    else:
                        self.window["-create_account_error_message-"].update(
                            result["err_msg"],
                            text_color=self.text_error_colour,
                        )

            # Study menu
            elif self.window["-study_menu_layout-"].Widget.winfo_ismapped():
                # Log out
                if event == "-study_menu_logout-":
                    self.data_handler.clear_user_data()
                    self._screen_switch("-study_menu_layout-", "-login_layout-")
                # Go to leaderboard screen (unfinished)
                elif event == "-study_menu_leaderboard-":
                    self._screen_switch("-study_menu_layout-", "-leaderboard_layout-")
                # Go to flashcard menu
                elif event == "-study_menu_flashcards-":
                    self._screen_switch(
                        "-study_menu_layout-", "-flashcard_menu_layout-"
                    )
                # Study topic from drop
                elif event == "-study_menu_study-":
                    if (
                        values["-study_menu_topics_drop-"]
                        in self.data_handler.topics_list
                    ):
                        # Load topic data to data handler
                        topic_id = self.data_handler.selected_topic_id(
                            self.window["-study_menu_topics_drop-"].widget.current()
                        )
                        self.data_handler.load_topic_id(topic_id)
                        self._screen_switch("-study_menu_layout-", "-topics_layout-")
                    else:
                        sg.popup_error(
                            "Please select a topic from the dropdown.",
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Launch demo
                elif event == "-study_menu_launch_demo-":
                    if (
                        values["-study_menu_topics_drop-"]
                        in self.data_handler.topics_list
                    ):
                        self._screen_switch(
                            "-study_menu_layout-",
                            "-{0}_demo_layout-".format(
                                values["-study_menu_topics_drop-"].lower()
                            ),
                        )
                    else:
                        sg.popup_error(
                            "Please select a topic from the dropdown.",
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )

            # Topic pages
            elif self.window["-topics_layout-"].Widget.winfo_ismapped():
                # Next page
                if event == "-topics_next-":
                    if not self.update_topic_page():
                        launch_demo = sg.popup_yes_no(
                            "No pages this way! Launch demo?",
                            title="Launch demo",
                            font=(self.font, self.small_text_size),
                        )
                        if launch_demo == "Yes":
                            self._screen_switch(
                                "-topics_layout-",
                                f"-{self.data_handler.topic_name.lower()}_demo_layout-",
                            )
                # Previous page
                elif event == "-topics_previous-":
                    if not self.update_topic_page(next_page=False):
                        launch_demo = sg.popup_yes_no(
                            "No pages this way! Launch demo?",
                            title="Launch demo",
                            font=(self.font, self.small_text_size),
                        )
                        if launch_demo == "Yes":
                            self._screen_switch(
                                "-topics_layout-",
                                f"-{self.data_handler.topic_name.lower()}_demo_layout-",
                            )
                # Return to study menu
                elif event == "-topics_exit-":
                    self._screen_switch("-topics_layout-", "-study_menu_layout-")

            # Flashcard menu
            elif self.window["-flashcard_menu_layout-"].Widget.winfo_ismapped():
                # Open flashcard pack
                if event == "-flashcard_menu_study_pack-":
                    if (
                        values["-flashcard_menu_packs_drop-"]
                        in self.data_handler.user_library_list
                    ):
                        pack_id = self.data_handler.selected_pack_id(
                            self.window["-flashcard_menu_packs_drop-"].widget.current()
                        )
                        # Load data for pack then switch screen
                        self.data_handler.load_pack_data(pack_id)
                        self._screen_switch(
                            "-flashcard_menu_layout-", "-flashcard_viewer_layout-"
                        )
                    else:
                        sg.popup_error(
                            "Please select a pack from the dropdown",
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Share pack (get share id)
                elif event == "-flashcard_menu_share-":
                    if (
                        values["-flashcard_menu_packs_drop-"]
                        in self.data_handler.user_library_list
                    ):
                        pack_id = self.data_handler.selected_pack_id(
                            self.window["-flashcard_menu_packs_drop-"].widget.current()
                        )
                        sg.popup(
                            "Your Share ID for {0} is:\n> {1}".format(
                                values["-flashcard_menu_packs_drop-"],
                                self.data_handler.get_share_id(pack_id),
                            ),
                            title="Share ID",
                            font=(self.font, self.small_text_size),
                        )
                    else:
                        sg.popup_error(
                            "Please select a pack from the dropdown",
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Download pack
                elif event == "-flashcard_menu_download-":
                    download_result = self.data_handler.download_pack(
                        sg.popup_get_text(
                            "Please enter the share ID: ",
                            title="Download Pack",
                            font=(self.font, self.small_text_size),
                        )
                    )
                    if download_result["result"]:
                        sg.popup_auto_close(
                            "Pack added successfully!",
                            title="Download pack",
                            font=(self.font, self.small_text_size),
                        )
                        self._screen_switch(
                            "-flashcard_menu_layout-", "-flashcard_menu_layout-"
                        )
                    else:
                        sg.popup_error(
                            download_result["err_msg"],
                            title="Download pack",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Delete pack
                elif event == "-flashcard_menu_delete_pack-":
                    # If pack not selected
                    if not values["-flashcard_menu_packs_drop-"]:
                        sg.popup_error(
                            "Please select a card pack.",
                            title="Pack deletion",
                            font=(self.font, self.small_text_size),
                        )
                    else:
                        pack_id = self.data_handler.selected_pack_id(
                            self.window["-flashcard_menu_packs_drop-"].widget.current()
                        )
                        # Confirm user would like to delete card pack
                        confirmed_delete = sg.popup_yes_no(
                            "Deleting is irreversible, are you sure?",
                            title="Warning",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                        if confirmed_delete == "Yes":
                            result = self.data_handler.delete_card_pack(pack_id)
                            sg.popup(
                                result,
                                title="Pack deletion",
                                font=(self.font, self.small_text_size),
                            )
                            self._screen_switch(
                                "-flashcard_menu_layout-", "-flashcard_menu_layout-"
                            )
                # Start creating a pack
                elif event == "-flashcard_menu_create-":
                    self._screen_switch(
                        "-flashcard_menu_layout-", "-flashcard_creator_title_layout-"
                    )
                # Return to study menu
                elif event == "-flashcard_menu_back-":
                    self._screen_switch(
                        "-flashcard_menu_layout-", "-study_menu_layout-"
                    )

            # Flashcard creator (title)
            elif self.window[
                "-flashcard_creator_title_layout-"
            ].Widget.winfo_ismapped():
                # Set name
                if event == "-flashcard_creator_title_set_name-":
                    result = self.data_handler.validate_pack_name(
                        values["flashcard_creator_title_name-"]
                    )
                    if result != True:
                        sg.popup_error(
                            result,
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                    else:
                        self._screen_switch(
                            "-flashcard_creator_title_layout-",
                            "-flashcard_creator_cards_layout-",
                        )
                # Return to flashcard menu
                elif event == "-flashcard_creator_title_cancel-":
                    self._screen_switch(
                        "-flashcard_creator_title_layout-", "-flashcard_menu_layout-"
                    )

            # Flashcard creator (cards)
            elif self.window[
                "-flashcard_creator_cards_layout-"
            ].Widget.winfo_ismapped():
                # Updating question type
                if event == "-flashcard_creator_cards_question_type-":
                    self.data_handler.clear_current_card()
                    if (
                        values["-flashcard_creator_cards_question_type-"]
                        == "Multiple choice"
                    ):
                        self.window["-flashcard_creator_cards_add_choice-"].update(
                            disabled=False
                        )
                        self.window["-flashcard_creator_cards_total_choices-"].update(
                            "Add answer [0/4]", text_color="black"
                        )
                        self.window["-flashcard_creator_cards_is_correct-"].update(
                            disabled=False
                        )
                    else:
                        self.window["-flashcard_creator_cards_add_choice-"].update(
                            disabled=True
                        )
                        self.window["-flashcard_creator_cards_total_choices-"].update(
                            "Add answer [-/4]", text_color="gray"
                        )
                        self.window["-flashcard_creator_cards_is_correct-"].update(
                            disabled=True
                        )
                # Save card
                elif event == "-flashcard_creator_cards_add_card-":
                    result = self.data_handler.add_card(
                        values["-flashcard_creator_cards_question_type-"],
                        values["-flashcard_creator_cards_prompt-"],
                        values["-flashcard_creator_cards_answer-"],
                        values["-flashcard_creator_cards_points-"],
                    )
                    if result == True:
                        self.window["-flashcard_creator_cards_total_choices-"].update(
                            "Add answer [0/4]"
                        )
                        sg.Popup(
                            "Card added successfully!",
                            title="New card",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_success_colour,
                        )
                    else:
                        sg.popup_error(
                            result,
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Add answer (multiple choice)
                elif event == "-flashcard_creator_cards_add_choice-":
                    result = self.data_handler.add_card_choice(
                        values["-flashcard_creator_cards_answer-"],
                        values["-flashcard_creator_cards_is_correct-"],
                    )
                    if result == True:
                        choice_count = self.data_handler.get_answer_count()
                        self.window["-flashcard_creator_cards_total_choices-"].update(
                            f"Add answer [{choice_count}/4]"
                        )
                        sg.Popup(
                            "Choice added successfully!",
                            title="New choice",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_success_colour,
                        )
                    else:
                        sg.popup_error(
                            result,
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Save pack
                elif event == "-flashcard_creator_cards_save-":
                    result = self.data_handler.save_card_pack()
                    if result == True:
                        self._screen_switch(
                            "-flashcard_creator_cards_layout-",
                            "-flashcard_menu_layout-",
                        )
                        sg.Popup(
                            "Pack saved successfully!",
                            title="New pack",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_success_colour,
                        )
                    else:
                        sg.popup_error(
                            result,
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Cancel (return to flashcard menu)
                elif event == "-flashcard_creator_cards_cancel-":
                    confirmed_cancel = sg.popup_yes_no(
                        "Cancelling will delete your progress, are you sure?",
                        title="Warning",
                        font=(self.font, self.small_text_size),
                    )
                    if confirmed_cancel == "Yes":
                        self.data_handler.clear_current_card()
                        self.data_handler.clear_current_pack
                        self._screen_switch(
                            "-flashcard_creator_cards_layout-",
                            "-flashcard_menu_layout-",
                        )

            # Flashcard viewer
            elif self.window["-flashcard_viewer_layout-"].Widget.winfo_ismapped():
                # Reveal cards
                if event == "-flashcard_viewer_reveal-":
                    visible = self.data_handler.toggle_card_reveal()
                    text = self.data_handler.current_card_answer if visible else ""
                    self.window["-flashcard_viewer_reveal_field-"].update(text)
                elif event == "-flashcard_viewer_next-":
                    self.show_new_flashcard()
                # Numerical cards
                elif event == "-flashcard_viewer_submit_numerical-":
                    if self.data_handler.validate_integer(
                        values["-flashcard_viewer_numerical_field-"]
                    ):
                        result = self.data_handler.check_answer(
                            values["-flashcard_viewer_numerical_field-"]
                        )
                        self.flashcard_answer_result(result)
                        self.show_new_flashcard()
                    else:
                        sg.popup_error(
                            "Please ensure your answer is an integer",
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Multiple choice cards
                elif event == "-flashcard_viewer_submit_multiple_choice-":
                    # Selecting answer from users input
                    result = self.data_handler.check_answer(
                        values["-flashcard_viewer_choice_drop-"], use_index=True
                    )
                    if not result:
                        sg.popup_error(
                            "Please provide an answer",
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                    else:
                        self.flashcard_answer_result(result)
                        self.show_new_flashcard()
                # Exit (to flashcard menu)
                elif event == "-flashcard_viewer_exit-":
                    self._screen_switch(
                        "-flashcard_viewer_layout-", "-flashcard_menu_layout-"
                    )

            # Binary tree input screen
            elif self.window["-trees_demo_layout-"].Widget.winfo_ismapped():
                # Return to study menu
                if event == "-trees_demo_exit-":
                    self._screen_switch("-trees_demo_layout-", "-study_menu_layout-")
                # Generate binary tree from list
                elif event == "-trees_demo_generate-":
                    generate_result = self.data_handler.generate_tree(
                        values["-trees_demo_input-"],
                        values["-trees_demo_balanced_check-"],
                    )
                    if generate_result["result"]:
                        self._screen_switch(
                            "-trees_demo_layout-", "-trees_view_layout-"
                        )
                    else:
                        sg.popup_error(
                            generate_result["err_msg"],
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )

            # Binary tree viewer
            elif self.window["-trees_view_layout-"].Widget.winfo_ismapped():
                # View traversal order
                if event == "-trees_view_traverse-":
                    if values["-trees_view_traversals_drop-"] in [
                        "Inorder",
                        "Preorder",
                        "Postorder",
                    ]:
                        sg.popup(
                            "{0} traversal: {1}".format(
                                values["-trees_view_traversals_drop-"],
                                self.data_handler.get_traversal_order(
                                    values["-trees_view_traversals_drop-"].lower()
                                ),
                            ),
                            title="Traversal",
                            font=(self.font, self.small_text_size),
                        )
                    else:
                        sg.popup_error(
                            "Please select a traversal from the dropdown",
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Add node
                elif event == "-trees_view_add_node-":
                    add_node_result = self.data_handler.add_tree_node(
                        sg.popup_get_text(
                            "Integer for new node: ",
                            title="Add Node",
                            font=(self.font, self.small_text_size),
                        )
                    )
                    if not add_node_result:
                        self.window["-trees_view_image-"].update(
                            data=self.data_handler.resize_image()
                        )
                    else:
                        sg.popup_error(
                            add_node_result,
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                # Back (to trees demo)
                elif event == "-trees_view_back-":
                    self._screen_switch("-trees_view_layout-", "-trees_demo_layout-")

            # Queues demo
            elif self.window["-queues_demo_layout-"].Widget.winfo_ismapped():
                # Queue - enqueue
                if event == "-queue_demo_enqueue-":
                    enqueue = self.data_handler.queue_enqueue()
                    if enqueue:
                        print(f"Enqueued: {enqueue}")
                        queue_elements = self.data_handler.get_queue()
                        front_index, rear_index = (
                            self.data_handler.queue_front(),
                            self.data_handler.queue_rear(),
                        )
                        self.update_queue_display(
                            queue_elements, front_index, rear_index
                        )
                    else:
                        print("Queue is full!")
                # Queue - dequeue
                elif event == "-queue_demo_dequeue-":
                    dequeue = self.data_handler.queue_dequeue()
                    if dequeue:
                        print(f"Dequeued: {dequeue}")
                        queue_elements = self.data_handler.get_queue()
                        front_index, rear_index = (
                            self.data_handler.queue_front(),
                            self.data_handler.queue_rear(),
                        )
                        self.update_queue_display(
                            queue_elements, front_index, rear_index
                        )
                    else:
                        print("Queue is empty!")
                # Queue - peek
                elif event == "-queue_demo_peek-":
                    peek = self.data_handler.queue_peek()
                    if peek:
                        print(f"The front element is {peek}")
                    else:
                        print("The queue is empty!")
                # Queue - isfull
                elif event == "-queue_demo_isfull-":
                    if self.data_handler.queue_is_full():
                        print("True; Queue is full")
                    else:
                        print("False; Queue is not full")
                # Queue - isempty
                elif event == "-queue_demo_isempty-":
                    if self.data_handler.queue_is_empty():
                        print("True; Queue is empty")
                    else:
                        print("False; Queue is not empty")
                # Queue - size
                elif event == "-queue_demo_size-":
                    print(f"Current size: {self.data_handler.queue_size()}")
                # Change queue type
                elif event == "-queue_demo_queue_type_combo-":
                    screen_elements = self.data_handler.switch_queue(
                        values["-queue_demo_queue_type_combo-"].lower()
                    )
                    self.show_queue_buttons(screen_elements)
                    front_index = self.data_handler.queue_front()
                    self.update_queue_display(
                        ["" for _ in range(self.data_handler.queue_max_size)],
                        front_index,
                    )
                # Stack - push
                elif event == "-queue_demo_push-":
                    push = self.data_handler.queue_push()
                    if push:
                        print(f"Pushed: {push}")
                        stack_elements = self.data_handler.get_queue()
                        front_index = self.data_handler.queue_front()
                        self.update_queue_display(stack_elements, front_index)
                    else:
                        print("Stack is full!")
                # Stack - pop
                elif event == "-queue_demo_pop-":
                    pop = self.data_handler.queue_pop()
                    if pop:
                        print(f"Popped: {pop}")
                        stack_elements = self.data_handler.get_queue()
                        front_index = self.data_handler.queue_front()
                        self.update_queue_display(stack_elements, front_index)
                    else:
                        print("Stack is empty!")
                # Queue - rear
                elif event == "-queue_demo_rear-":
                    rear = self.data_handler.queue_rear_element()
                    if rear:
                        print(f"Rear points to: {rear}")
                    else:
                        print("Queue is empty!")
                # Exit (to study menu)
                elif event == "-queue_demo_exit-":
                    self._screen_switch("-queues_demo_layout-", "-study_menu_layout-")

            # Graphs demo
            elif self.window["-graphs_demo_layout-"].Widget.winfo_ismapped():
                # Change input type
                if event == "-graphs_demo_input_type-":
                    graphs_display_map = {
                        "Adjacency matrix": {
                            "node_input": True,
                            "add_node": True,
                            "node_1": True,
                            "node_2": True,
                            "add_edge": True,
                            "directed_check": True,
                            "matrix_input": False,
                        },
                        "Adjacency list": {
                            "node_input": False,
                            "add_node": False,
                            "node_1": False,
                            "node_2": False,
                            "add_edge": False,
                            "directed_check": False,
                            "matrix_input": True,
                        },
                    }
                    state = graphs_display_map.get(values["-graphs_demo_input_type-"])
                    for key, value in state.items():
                        self.window[f"-graphs_demo_{key}-"].update(disabled=value)
                    self.data_handler.clear_adjacency_list()
                    self.window["-graphs_demo_node_1-"].update(values=[])
                    self.window["-graphs_demo_node_2-"].update(values=[])
                # Add node to adjacency list
                elif event == "-graphs_demo_add_node-":
                    result = self.data_handler.add_adjacency_node(
                        values["-graphs_demo_node_input-"]
                    )
                    if result != True:
                        sg.popup_error(
                            result,
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                    else:
                        # Updating drops (for adding edge) with new node
                        adjacency_node_names = self.data_handler.adjacency_node_names
                        self.window["-graphs_demo_node_1-"].update(
                            values=adjacency_node_names
                        )
                        self.window["-graphs_demo_node_2-"].update(
                            values=adjacency_node_names
                        )
                # Add edge to adjacency list
                elif event == "-graphs_demo_add_edge-":
                    result = self.data_handler.add_edge_adjacency_list(
                        values["-graphs_demo_node_1-"],
                        values["-graphs_demo_node_2-"],
                        values["-graphs_demo_directed_check-"],
                    )
                    if result != True:
                        sg.popup_error(
                            result,
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                    else:
                        sg.popup_auto_close(
                            "Edge added!",
                            title="New edge",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_success_colour,
                        )
                # Generate graph image
                elif event == "-graphs_demo_generate_graph-":
                    if values["-graphs_demo_input_type-"] == "Adjacency matrix":
                        result = self.data_handler.generate_graph_from_matrix_string(
                            values["-graphs_demo_matrix_input-"]
                        )
                    else:
                        result = self.data_handler.generate_graph_from_adjacency_list()
                    if result != True:
                        sg.popup_error(
                            result,
                            title="Error",
                            font=(self.font, self.small_text_size),
                            text_color=self.text_error_colour,
                        )
                    else:
                        self._screen_switch(
                            "-graphs_demo_layout-", "-graphs_view_layout-"
                        )
                # Return to study menu
                elif event == "-graphs_demo_back-":
                    self._screen_switch("-graphs_demo_layout-", "-study_menu_layout-")

            # Graphs viewer
            elif self.window["-graphs_view_layout-"].Widget.winfo_ismapped():
                # Display adjacency matrix
                if event == "-graphs_view_matrix-":
                    sg.popup(
                        self.data_handler.adjacency_matrix_table_str,
                        title="Adjacency matrix",
                        font=(self.font, self.small_text_size),
                    )
                # Back (to graphs demo)
                elif event == "-graphs_view_back-":
                    self._screen_switch("-graphs_view_layout-", "-graphs_demo_layout-")

            # Leaderboard
            elif self.window["-leaderboard_layout-"].Widget.winfo_ismapped():
                # Back to study menu
                if event == "-leaderboard_back-":
                    self._screen_switch("-leaderboard_layout-", "-study_menu_layout-")
                # Reverse leaderboard order
                elif event == "-leaderboard_reverse_order-":
                    self.window["-leaderboard_table-"].update(
                        values=self.data_handler.leaderboard_data_reverse
                    )

        self.window.close()


# Initialises and displays the GUI if the module is executed directly
if __name__ == "__main__":
    app = GUI()
    app.run()
