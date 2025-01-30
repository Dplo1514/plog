from abc import ABC, abstractmethod

from langchain.text_splitter import (CharacterTextSplitter,
                                     RecursiveCharacterTextSplitter,
                                     Language)


class AbstractTextSplitter(ABC):
    def __init__(
        self,
        _chunk_size: int,
        _chunk_overlap: int,
        _length_function=len
    ):
        self.chunk_size = _chunk_size
        self.chunk_overlap = _chunk_overlap
        self.length_function = _length_function

    @abstractmethod
    def split(self, _content: str) -> list[str]:
        pass

    @abstractmethod
    def create_documents(self, _contents: list[str]) -> list:
        pass


class CharacterTextSplitterAdapter(AbstractTextSplitter):
    def __init__(
        self,
        _separator: str,
        _chunk_size: int,
        _chunk_overlap: int,
        _length_function=len
    ):
        super().__init__(_chunk_size, _chunk_overlap, _length_function)
        self.splitter = CharacterTextSplitter(
            separator=_separator,
            chunk_size=_chunk_size,
            chunk_overlap=_chunk_overlap,
            length_function=_length_function
        )

    def split(self, content: str) -> list[str]:
        return self.splitter.split_text(content)

    def create_documents(self, contents: list[str]) -> list:
        return self.splitter.create_documents(contents)


class RecursiveTextSplitterAdapter(AbstractTextSplitter):
    def __init__(
        self,
        _chunk_size: int,
        _chunk_overlap: int,
        _length_function=len
    ):
        super().__init__(_chunk_size, _chunk_overlap, _length_function)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=_chunk_size,
            chunk_overlap=_chunk_overlap,
            length_function=_length_function
        )

    def split(self, content: str) -> list[str]:
        return self.splitter.split_text(content)

    def create_documents(self, contents: list[str]) -> list:
        return self.splitter.create_documents(contents)

    def from_language(self,
        _language: Language) -> RecursiveCharacterTextSplitter:
        return RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
