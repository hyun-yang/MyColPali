from enum import Enum, auto


class Constants:
    # Application Title
    APPLICATION_TITLE = "MyColPali"

    # Setting file name
    SETTINGS_FILENAME = "settings.ini"

    # App Style
    FUSION = 'Fusion'

    # API Call User Stop
    MODEL_PREFIX = "Model: "
    ELAPSED_TIME = "Elapsed Time: "
    FINISH_REASON = "Finish Reason: "

    FORCE_STOP = "Force Stop"
    NORMAL_STOP = "stop"
    RESPONSE_TIME = " | Response Time : "

    # Database
    DATABASE_NAME = "mycolpali.db"
    SQLITE_DATABASE = "QSQLITE"

    VISION_MAIN_TABLE = "vision_main"
    VISION_DETAIL_TABLE = "vision_detail"
    VISION_FILE_TABLE = "vision_files"

    VISION_DETAIL_TABLE_ID_NAME = "vision_detail_"
    VISION_IMAGE_EXTENSION = "png"

    NEW_VISION = "New Vision"

    RESPONSE_FORMAT_B64_JSON = "b64_json"
    SCALE_RATIO = 1.1

    # Vision
    VISION_MODEL_LIST = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]

    VISION_SIZE_LIST = [
        "1024", "768", "512", "256"
    ]

    VISION_DETAIL_LIST = [
        "auto",
        "high",
        "low"
    ]

    THUMBNAIL_LIST_MAX_COLUMN = 3  # Vision : 3 images per row

    ABOUT_TEXT = (
        "<b>MyColPali</b><br>"
        "Version: 1.0.0<br><br>"
        "Author: Hayden Yang(양 현석)<br>"
        "Github: <a href='https://github.com/hyun-yang'>https://github.com/hyun-yang</a><br><br>"
        "Contact: iamyhs@gmail.com<br>"
    )

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ValueError(f"Cannot reassign constant '{name}'")
        self.__dict__[name] = value


class UI:
    FILE = "File"
    VIEW = "View"
    HELP = "Help"

    UI = "UI"
    FOUNDS = "founds"
    NOT_FOUND = "not found"
    METHOD = "Method "

    COLPALI = "ColPali"
    COLPALI_TIP = "ColPali"
    COLPALI_LIST = "ColPali List"

    VISION = "Vision"
    VISION_TIP = "Vision"
    VISION_LIST = "Vision List"

    SETTING = "Setting"
    SETTING_TIP = "Setting"

    CLOSE = "Close"
    CLOSE_TIP = "Exit App"

    ABOUT = "About..."
    ABOUT_TIP = "About"

    ADD = "Add"
    DELETE = "Delete"
    RENAME = "Rename"
    STOP = "Stop"
    SAVE = "Save"
    COPY = "Copy"
    CLEAR_ALL = "Clear All"
    COPY_ALL = "Copy All"
    RELOAD_ALL = "Reload All"
    OK = "Ok"
    CANCEL = "Cancel"
    SUCCESS = "Success"
    ERROR = "Error"
    COPY_TEXT = "Copy Text"
    SAVE_IMAGES = "Save Images"

    IMAGE_FILTER = "Images (*.png)"
    IMAGE_PNG_EXTENSION = ".png"
    IMAGE_PNG = "PNG"
    IMAGE_SIZE_ERROR_MESSAGE = "It should be a png file and its size should be less than 4MB."

    FILE_READ_IN_BINARY_MODE = 'rb'
    UTF_8 = "utf-8"

    CHAT_PROMPT_PLACEHOLDER = "Enter your prompt here."
    SEARCH_PROMPT_PLACEHOLDER = "Enter your search term."
    SEARCH_PROMPT_DB_PLACEHOLDER = "Search..."

    TITLE = "Title"
    PROMPT = "Prompt"

    EXIT_APPLICATION_TITLE = "Exit Application"
    EXIT_APPLICATION_MESSAGE = "Are you sure you want to exit?"

    WARNING_TITLE = "Warning"
    WARNING_API_KEY_SETTING_MESSAGE = "Please set the API key in Setting->AI Provider."
    WARNING_TITLE_NO_ROW_SELECT_MESSAGE = "No row selected for saving."
    WARNING_TITLE_NO_ROW_DELETE_MESSAGE = "No row selected for deletion."
    WARNING_TITLE_SELECT_FILE_MESSAGE = "Select file first."
    WARNING_COLPALI_INDEX_NAME = "Enter ColPali Index Name."
    WARNING_TITLE_SELECT_FILE_AND_PROMPT_MESSAGE = "Select file and enter your prompt."
    WARNING_TITLE_NO_PROMPT_MESSAGE = "Enter your prompt."

    SAVE_IMAGE_TITLE = "Save Image"
    SAVE_IMAGE_FILTER = "PNG Files (*.png);;All Files (*)"

    TEXT_FILTER = "Text (*.txt)"
    PDF_FILTER = "PDF (*.pdf)"
    WORD_FILTER = "Word (*.docx)"

    CONFIRM_DELETION_TITLE = "Confirm Deletion"
    CONFIRM_DELETION_ROW_MESSAGE = "Are you sure you want to delete the selected row?"
    CONFIRM_DELETION_VISION_MESSAGE = "Are you sure you want to delete this vision?"
    CONFIRM_CHOOSE_VISION_MESSAGE = "Choose vision first to delete"

    LABEL_ENTER_NEW_NAME = "Enter new name:"

    FAILED_TO_OPEN_FILE = "Failed to open file: "
    FILE_NOT_EXIST = "File does not exist: "
    MEDIA_NOT_LOADED = "Media is not loaded yet."

    SELECT_FOLDER = "Select Folder"
    FILE_COPY_SUCCESS = "Files copied successfully!"
    FILE_COPY_ERROR = "An error occurred: "

    UNSUPPORTED_FILE_TYPE = "Unsupported file type"

    SETTINGS = "Settings"
    SETTINGS_PIXEL = "px"

    ICON_FILE_ERROR = "Error: The icon file"
    ICON_FILE_NOT_EXIST = "does not exist."

    ITEM_ICON_SIZE = 32
    ITEM_EXTRA_SIZE = 20
    ITEM_PADDING = 5

    QSPLITTER_LEFT_WIDTH = 200
    QSPLITTER_RIGHT_WIDTH = 800
    QSPLITTER_HANDLEWIDTH = 3

    PROGRESS_BAR_STYLE = """
            QProgressBar{
                border: 1px grey;
                border-radius: 5px;            
            }
    
            QProgressBar::chunk {
                background-color: lightgreen;
                width: 10px;
                margin: 1px;
            }
            """

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ValueError(f"Cannot reassign constant '{name}'")
        self.__dict__[name] = value


class FILE_INDEX_MESSAGE:
    THREAD_RUNNING = "Indexing File : Previous thread is still running!"
    THREAD_FINISHED = "Indexing File : Thread has been finished"
    INVALID_CREATION_TYPE = "Invalid creation type: "
    UNEXPECTED_ERROR = "An unexpected error occurred: "

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ValueError(f"Cannot reassign constant '{name}'")
        self.__dict__[name] = value


class MODEL_MESSAGE:
    MODEL_UNSUPPORTED = "Unsupported LLM:"
    MODEL_UNSUPPORTED_TYPE = "Unsupported model type"
    THREAD_RUNNING = "Previous thread is still running!"
    THREAD_FINISHED = "Thread has been finished"
    INVALID_CREATION_TYPE = "Invalid creation type: "
    UNEXPECTED_ERROR = "An unexpected error occurred: "
    AUTHENTICATION_FAILED_OPENAI = "Authentication failed. The OpenAI API key is not valid."

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ValueError(f"Cannot reassign constant '{name}'")
        self.__dict__[name] = value


class DATABASE_MESSAGE:
    DATABASE_TITLE_ERROR = "Database Error"
    DATABASE_FETCH_ERROR = "Failed to fetch prompt from the database."
    DATABASE_ADD_ERROR = "Failed to add new row from the database."
    DATABASE_DELETE_ERROR = "Failed to delete row from the database."
    DATABASE_UPDATE_ERROR = "Failed to update row from the database."

    DATABASE_VISION_CREATE_TABLE_ERROR = "Failed to create vision_main table: "
    DATABASE_VISION_ADD_ERROR = "Failed to add vision main: "
    DATABASE_VISION_UPDATE_ERROR = "Failed to update vision main: "
    DATABASE_VISION_MAIN_ENTRY_SUCCESS = "Successfully deleted vision main entry with id: "
    DATABASE_VISION_MAIN_ENTRY_FAIL = "Failed to delete vision main entry with id "

    DATABASE_VISION_DETAIL_CREATE_TABLE_ERROR = "Failed to create vision_detail table: "
    DATABASE_VISION_DETAIL_INSERT_ERROR = "Failed to insert vision detail: "
    DATABASE_VISION_DETAIL_DELETE_ERROR = "Failed to delete vision detail table "
    DATABASE_VISION_DETAIL_FETCH_ERROR = "Failed to fetch vision details for vision_main_id"

    DATABASE_VISION_DETAIL_FILE_CREATE_TABLE_ERROR = "Failed to create vision detail file table: "
    DATABASE_VISION_DETAIL_FILE_INSERT_ERROR = "Failed to insert vision detail file: "
    DATABASE_VISION_DETAIL_FILE_DELETE_ERROR = "Failed to delete vision detail file table "
    DATABASE_VISION_DETAIL_FILE_FETCH_ERROR = "Failed to fetch vision detail file for vision_detail_id "
    DATABASE_VISION_DETAIL_FILE_NO_RECORD_ERROR = "No record found for vision_detail_id "

    DATABASE_RETRIEVE_DATA_FAIL = "Failed to retrieve data from "
    DATABASE_DELETE_DETAIL_TABLE_SUCCESS = "Successfully deleted detail table: "
    DATABASE_DELETE_DETAIL_TABLE_ERROR = "Failed to delete main entry with id "
    DATABASE_EXECUTE_QUERY_ERROR = "Failed to execute query: "

    DATABASE_FAILED_OPEN = "Failed to open database."
    DATABASE_ENABLE_FOREIGN_KEY = "Failed to enable foreign key: "
    DATABASE_PRAGMA_FOREIGN_KEYS_ON = "PRAGMA foreign_keys = ON;"

    NEW_TITLE = "New Title"
    NEW_PROMPT = "New Prompt"


class AIProviderName(Enum):
    OPENAI = 'OpenAI'
    CLAUDE = 'Claude'
    GEMINI = 'Gemini'
    OLLAMA = 'Ollama'


class MainWidgetIndex(Enum):
    VISION_WIDGET = auto()


def get_ai_provider_names():
    return [ai_provider.value for ai_provider in AIProviderName]
