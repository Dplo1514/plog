from abc import ABC, abstractmethod


class AbstractLoader(ABC):
    def __init__(self, _sources):
        self.sources = _sources

    @abstractmethod
    def load(self) -> list[documents.base.Document]:
        """Document를 로드하는 추상 메서드"""
        pass


class WebBaseLoaderAdapter(AbstractLoader):
    def __init__(self, _url: str):
        super().__init__([_url])
        self.loader = WebBaseLoader(_url)

    def load(self) -> list[documents.base.Document]:
        return self.loader.load()


class UnstructuredURLLoaderAdapter(AbstractLoader):
    def __init__(self, _urls: list):
        super().__init__(_urls)
        self.loader = UnstructuredURLLoader(_urls)

    def load(self) -> list[documents.base.Document]:
        return self.loader.load()


class PDFLoaderAdapter(AbstractLoader):
    def __init__(self, _file_path: str):
        super().__init__([_file_path])
        self.loader = PyPDFLoader(_file_path)

    def load(self) -> list[documents.base.Document]:
        return self.loader.load()


class CSVLoaderAdapter(AbstractLoader):
    def __init__(self, _file_path: str, _csv_args: dict):
        super().__init__([_file_path])
        self.loader = CSVLoader(_file_path, csv_args=_csv_args)

    def load(self) -> list[documents.base.Document]:
        return self.loader.load()
