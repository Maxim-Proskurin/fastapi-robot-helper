import re


class ScriptTextAnalyzer:
    """
    Сервис для анализа и валидации текста
    скрипта с помощью регулярных выражений.
    """

    @staticmethod
    def extract_emails(text: str) -> list[str]:
        """
        Извлечь все email-адреса из текста скрипта.

        Args:
            text (str): Текст скрипта.

        Returns:
            list[str]: Список найденных email-адресов.
        """
        return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

    @staticmethod
    def validate_script_pattern(text: str, pattern: str) -> bool:
        """
        Проверить, соответствует ли текст
        скрипта заданному регулярному выражению.

        Args:
            text (str): Текст скрипта.
            pattern (str): Регулярное выражение.

        Returns:
            bool: True, если текст соответствует паттерну, иначе False.
        """
        return bool(re.fullmatch(pattern, text))

    @staticmethod
    def extract_variables(text: str) -> list[str]:
        """
        Извлечь переменные вида {{variable}} из текста скрипта.

        Args:
            text (str): Текст скрипта.

        Returns:
            list[str]: Список имён переменных.
        """
        return re.findall(r"\{\{(\w+)\}\}", text)
