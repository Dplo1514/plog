from document_loader import PDFLoaderAdapter


adapter = PDFLoaderAdapter("file_path")
documents: list(documents.base.Document) = adapter.load("")

for document in documents:
    print(document)