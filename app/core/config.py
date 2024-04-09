from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str = 'BOT_TOKEN'
    payment_token: str = 'PAYMENT_TOKEN'
    database_url: str = 'DATABASE_URL'
    group_id: str = 'GROUP_ID'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
