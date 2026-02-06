from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "sqlite:///./vader_todos.db"
    mysql_host: str = "mysql"
    mysql_port: int = 3306
    mysql_user: str = "vader"
    mysql_password: str = "deathstar"
    mysql_database: str = "empire_todos"
    mysql_root_password: str = "emperor"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api"
    frontend_url: str = "http://localhost:3000"
    allowed_origins: List[str] = ["http://localhost:3000", "http://frontend:3000"]

    # Security Configuration
    secret_key: str = "execute-order-66-the-empire-strikes-back"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    # Application Configuration
    debug: bool = False
    log_level: str = "info"
    app_name: str = "Order 66: Execute the Query - CTF Challenge"
    app_version: str = "1.0.0-CTF"

    # Performance Configuration
    worker_processes: int = 1
    worker_connections: int = 1000
    keepalive_timeout: int = 2
    max_request_size: int = 16777216  # 16MB
    request_timeout: int = 30

    # CORS Configuration
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]

    # CTF Configuration
    ctf_flag: str = "SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}"
    ctf_flag_description: str = "Execute Order 66 - The hidden Imperial intelligence"
    enable_sample_data: bool = True
    enable_ctf_endpoints: bool = True

    # Health Check Configuration
    health_check_interval: int = 30
    health_check_timeout: int = 5
    health_check_retries: int = 3

    # Environment Detection
    environment: str = "development"

    @property
    def is_mysql(self) -> bool:
        """Check if using MySQL database"""
        return self.database_url.startswith(("mysql://", "mysql+pymysql://"))

    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite database"""
        return self.database_url.startswith("sqlite://")

    @property
    def mysql_connection_url(self) -> str:
        """Generate MySQL connection URL"""
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"

    def get_database_url(self) -> str:
        """Get the appropriate database URL based on configuration"""
        if os.getenv("DATABASE_URL"):
            return self.database_url
        elif os.getenv("MYSQL_HOST") or self.mysql_host != "mysql":
            return self.mysql_connection_url
        else:
            return self.database_url

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
