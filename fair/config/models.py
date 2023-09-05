from dataclasses import dataclass
from typing import Literal, Optional, Union


@dataclass
class LoggerConfig:
    name: str
    level: Literal['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']  # Log level
    stream: Optional[Literal['stdout', 'stderr']] = None  # Log stream if any
    file_path: Optional[str] = None  # Log file path if any
    format: Optional[str] = None  # Log format if any


@dataclass
class RedisConfig:
    host: str
    port: int
    db: Optional[int] = 0
    password: Optional[str] = None
    prefix: Optional[str] = 'telebot_'


@dataclass
class BotStateStorageConfig:
    type: Literal['redis', 'memory']  # State storage type, I don't recommend using pickle, thus leave it out
    redis: Optional[RedisConfig] = None  # Redis config if any


@dataclass
class BotWebhookConfig:
    url: str  # Webhook url to send updates to
    secret_token: str  # Secret token to verify the webhook, strongly recommended
    cert_path: Optional[str] = None  # Path to the public key SSL certificate if self-signed
    ip_address: Optional[str] = None  # IP address to use instead of one resolved via DNS
    max_connections: Optional[int] = None  # Maximum allowed number of simultaneous HTTPS connections to the webhook


@dataclass
class BotConfig:
    owner_tg_id: int  # Bot owner telegram id
    token: str  # Telegram bot token
    drop_pending: bool  # Drop pending updates on startup
    use_webhook: bool  # Use webhook, otherwise long polling
    use_class_middlewares: bool  # Use class middlewares if any
    actions_timeout: float  # Timeout between user's actions in seconds
    logger: LoggerConfig  # Logger config for the bot
    allowed_updates: Optional[Union[list[str], Literal['ALL']]] = None  # by default all except chat_member
    state_storage: Optional[BotStateStorageConfig] = None  # Bot state storage config if any
    webhook: Optional[BotWebhookConfig] = None  # Webhook config if any
    telegram_api_url: Optional[str] = None  # Custom Telegram API url for Local Bot API Server if any


@dataclass
class DBConfig:
    host: str  # DBMS host
    port: int  # DBMS port
    user: str  # DBMS user
    password: str  # DBMS user password
    database: str  # Database name
    logger: LoggerConfig  # Logger config for database


@dataclass
class MessagesConfig:
    welcome: str
    unregistered_help: str
    player_help: str
    manager_help: str
    anti_flood: str
    manager_registration_forbidden: str
    manager_registration_disabled: str
    get_manager_password: str
    get_manager_name: str
    invalid_manager_name: str
    manager_name_already_taken: str
    add_manager_error: str
    manager_registered: str
    unknown_error: str


@dataclass
class ButtonsConfig:
    reg_player: str
    reg_manager: str
    list_all_players: str
    list_all_locations: str
    add_balance: str
    subtract_balance: str
    choose_location: str
    help: str
    cancel: str


@dataclass
class Config:
    bot: BotConfig
    db: DBConfig
    # Extra configs if any
    logger: LoggerConfig  # Logger config for the app
    messages: MessagesConfig  # Messages text config
    buttons: ButtonsConfig  # Buttons text config
