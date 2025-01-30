import os

import numpy as np
from numpy import dot
from numpy.linalg import norm
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from sklearn.cluster import KMeans
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


class OpenAIEmbedder:
    def __init__(self):
        load_dotenv()
        self.llm = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])


class HuggingFaceEmbedder:
    """
    HuggingFace BGE Embeddings 클래스를 래핑한 유틸리티 클래스.
    - 다양한 모델 이름과 매개변수를 지원하여 임베딩 생성.
    """

    def __init__(
        self,
        _model_name: str,
        _model_kwargs: dict,
        _encode_kwargs: dict
    ):
        self.llm = HuggingFaceBgeEmbeddings(
            model_name=_model_name,
            model_kwargs=_model_kwargs,
            encode_kwargs=_encode_kwargs
        )


def cosine_similarity(vector_a, vector_b):
    """
    코사인 유사도를 계산하는 함수
    :param vector_a: 첫 번째 벡터 (list 또는 numpy array)
    :param vector_b: 두 번째 벡터 (list 또는 numpy array)
    :return: 두 벡터 간의 코사인 유사도 (float)
    """
    # 벡터의 크기가 0인지 확인 (예외 처리)
    if norm(vector_a) == 0 or norm(vector_b) == 0:
        raise ValueError("입력 벡터 중 하나가 크기 0입니다.")

    # 코사인 유사도 계산
    return dot(vector_a, vector_b) / (norm(vector_a) * norm(vector_b))
