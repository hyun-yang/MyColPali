# MyColPali
이 어플리케이션은 ColPali 비전 언어 모델과 OpenAI 기능을 활용하여 다양한 문서 처리 기능을 제공합니다.

### ColPali 소개
- ColPali는 비전 언어 모델(VLM)을 활용한 혁신적인 문서 검색 모델입니다.
- 관련 링크 [ColPali: Efficient Document Retrieval with Vision Language Models](https://arxiv.org/abs/2407.01449)

### ColPali 특징
- 비전 언어 모델을 사용한 효율적인 문서 인덱싱.
- 텍스트, 표, 그림 등 다양한 문서 유형 처리 가능.
- OCR, Layout Parser, Chunking, Captioning, 텍스트 임베딩 모델 등의 과정이 필요 없음.
- 다른 RAG 시스템에 비해 상대적으로 빠른 답변 처리.

![colpali_archtecture](https://github.com/user-attachments/assets/d29d3c4a-959e-4c4d-ad48-01fcf253e513)

## 업데이트
- ColQwen2 모델 추가 [ColQwen2](https://huggingface.co/vidore/colqwen2-v0.1) 
- 아래 명령어로 관련된 라이브러리를 업데이트 합니다. 

```bash
pip install -r requirements.txt
```


## 필수 조건
시작하기 전에 다음 요구 사항을 확인하세요:

1. Python:

    Python 3.10 이상이 설치되어 있는지 확인하세요. 공식 Python 웹사이트에서 다운로드 할 수 있습니다. 

```bash
  python --version
```    

2. pip:

   Python의 패키지 설치 도구인 pip가 설치되어 있는지 확인하세요.


3. Git:

   버전 관리를 위해 Git이 설치되어 있는지 확인하세요. 공식 Git 웹사이트에서 다운로드 할 수 있습니다.


4. 가상 환경:

   프로젝트 의존성을 관리하기 위해 가상 환경을 사용하는 것을 권장합니다.
   
   venv를 사용하여 가상 환경을 생성할 수 있습니다:

```bash
  python -m venv venv
```    

```bash
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

5. IDE/코드 편집기:

   원하는 IDE 또는 코드 편집기를 사용하세요. PyCharm, VSCode, Eclipse 등이 있습니다.


6. PlantUML(선택 사항): 

    PlantUML은 UML 다이어그램을 생성하는 데 사용합니다. 

    공식 PlantUML 웹사이트 또는 PyCharm 플러그인, Xcode 확장에서 PlantUML을 다운로드하세요.


## 빠른 설치

1. 저장소 복사

```bash
git clone https://github.com/hyun-yang/MyColPali
```

2. pip를 사용하여 설치:

```bash
pip install -r requirements.txt
```
가상 환경(venv)을 사용하는 경우, 다음 명령어를 사용하세요

```bash
python -m pip install -r requirements.txt
```

3. main.py 실행

```bash
python main.py
```

4. API Key 설정하기
   * 'Setting' 메뉴를 열고 API Key를 설정합니다.  

  
5. 재 실행

```bash
python main.py
```

## ColPali/ColQwen2 모델 다운로드
어플리케이션 사용하기 전에 ColPali 모델을 미리 다운로드 합니다. 

다운로드 할 전체 파일 크기가 5GB(ColPali), 8GB(ColQwen2)가 넘습니다. 현재 사용하고 있는 네트워크 속도에 따라 시간이 걸릴 수도 있습니다.

아래 두가지 방법 중 하나를 선택해서 다운로드 합니다.

1) 허깅 페이스 [vidore/colpali-v1.2](https://huggingface.co/vidore/colpali-v1.2) 에서 다운로드 툴을 사용해서 다운로드 합니다. 
2) 허깅 페이스 [vidore/colqwen2-v0.1](https://huggingface.co/vidore/colqwen2-v0.1) 에서 다운로드 툴을 사용해서 다운로드 합니다.
3) **download_model/download_colpali_model.ipynb** 주피터 노트북 파일을 열고 다운로드 합니다.

## PyTorch 설치

GPU를 활용하기 위해서는 현재 사용하는 운영체제와 GPU가 지원하는 cuda 버전과 맞는 [PyTorch](https://pytorch.org/) 버전을 설치해야 합니다.

만일, pytorch 버전이 설치가 제대로 되지 않거나, GPU가 없다면 cpu 모드로 작동합니다. 그리고 cpu 모드는 속도가 느립니다. 

util 폴더 아래에 **Utility.get_torch_device** 메소드를 참고하세요. 


## 실행 화면

* 처음 실행

![mycolpali_first_run_2](https://github.com/user-attachments/assets/ed3a99fa-53c3-4865-8c50-ffec44ef4fe1)

* 설정
![mycolpali_first_run_1](https://github.com/user-attachments/assets/5652b8f6-6c76-4ad6-8120-3cc4089fb576)


### UML Diagram

* Main Class Diagram

![MyColPali-UML-3](https://github.com/user-attachments/assets/f967c0cd-88ca-411d-93af-23121f2d0e31)

* Vision Presenter / ColPaliVLMModel Diagram

![MyColPali-UML-2](https://github.com/user-attachments/assets/ab066554-f05f-48ff-b186-8d659ade4656)


## ColPali 질문/답변 테스트 

이 테스트에 사용한 시스템 정보 입니다.
- OS : Windows 11
- CPU : Ryzen 7 7800X3D 
- RAM : 64GB DDR5 Corsair 6000MT/s
- GPU : Nvidia GeForce RTX 4070 Ti Super - 16GB VRAM
- CUDA : 12.1

### 1) ColPali  Efficient Document Retrieval with Vision Language Models 질문/답변

아래 질문 답변에 사용한 파일은 [ColPali: Efficient Document Retrieval with Vision Language Models](https://arxiv.org/abs/2407.01449) 입니다.

이 문서 20페이지로 이루어져 있고, 글, 그래프, 이미지가 함께 포함되어 있습니다.

- 파일 인덱싱 시간 : 17초
- 총 페이지 : 20 페이지
- 파일 사이즈 : 8.9 mb

![colpai_pdf_time](https://github.com/user-attachments/assets/62d9f81f-2405-4f6e-9eeb-2d9c3fa448de)

### 영문 질문
1) Summarize this document.
2) What is the purpose of the ViDoRe benchmark?
3) Why is the ColPali model superior to existing document retrieval systems?
4) What is the importance of visual cues in document retrieval systems?
5) How is the training dataset for the ColPali model composed?
6) How does the late interaction mechanism of the ColPali model work?
7) What evaluation metrics does the ViDoRe benchmark use?
8) What comparative models were used to evaluate the performance of the ColPali model?
9) How has the indexing speed of the ColPali model been improved?
10) What methods are used to reduce the memory usage of the ColPali model?

*이 중에서 What evaluation metrics does the ViDoRe benchmark use? 질문에 대해서 답변할 때, 이미지 5개를 참고할 때 와 10개를 참고할 때 답변의 수준이 다르다는 걸 확인하세요.*

### 한글 질문
1) 이 문서를 요약해주세요.
2) ViDoRe 벤치마크의 목적은 무엇인가요?
3) ColPali 모델이 기존 문서 검색 시스템보다 우수한 이유는 무엇인가요?
4) 문서 검색 시스템에서 시각적 단서의 중요성은 무엇인가요?
5) ColPali 모델의 학습 데이터셋은 어떻게 구성되었나요?
6) ColPali 모델의 늦은 상호작용 메커니즘은 어떻게 작동하나요?
7) ViDoRe 벤치마크는 어떤 평가 메트릭을 사용하나요?
8) ColPali 모델의 성능을 평가하기 위해 어떤 비교 모델이 사용되었나요?
9) ColPali 모델의 인덱싱 속도는 어떻게 개선되었나요?
10) ColPali 모델의 메모리 사용량을 줄이기 위한 방법은 무엇인가요?

### 질문/답변 결과

1) Summarize this document.

![colpai_summarize this document](https://github.com/user-attachments/assets/d694329f-b5db-4af7-9cf5-03b93f5b3588)


2) What is the purpose of the ViDoRe benchmark?

![colpai_What is the purpose of the ViDoRe benchmark2](https://github.com/user-attachments/assets/9d6da452-014f-46a7-816b-b56768d59cab)


3) Why is the ColPali model superior to existing document retrieval systems?

![colpai_Why is the ColPali model superior to existing document retrieval systems](https://github.com/user-attachments/assets/8de82a80-0f1b-4c5d-88e3-e0eba0e88ee6)


4) What is the importance of visual cues in document retrieval systems?

![colpai_What is the importance of visual cues in document retrieval systems](https://github.com/user-attachments/assets/2fb4f352-f94e-45f9-a859-ab7eb2362832)

5) What evaluation metrics does the ViDoRe benchmark use?

- 5개의 이미지를 사용
![colpai_What evaluation metrics does the ViDoRe benchmark use](https://github.com/user-attachments/assets/5f16471b-f663-47ce-98e8-6af53018c291)

- 10개의 이미지를 사용   
![colpai_What evaluation metrics does the ViDoRe benchmark use-10images](https://github.com/user-attachments/assets/3a1a374f-b274-464e-8828-9c0fee38a788)

6) What methods are used to reduce the memory usage of the ColPali model?

![colpai_What methods are used to reduce the memory usage of the ColPali model](https://github.com/user-attachments/assets/18f44522-3552-4bad-bc64-fc1da8613faf)

7) How has the indexing speed of the ColPali model been improved?

![colpai_How has the indexing speed of the ColPali model been improved](https://github.com/user-attachments/assets/dc8ad9c4-7fb7-4505-8faf-3bfb5b170ef6)

8) What comparative models were used to evaluate the performance of the ColPali model?

![colpai_What comparative models were used to evaluate the performance of the ColPali model](https://github.com/user-attachments/assets/3133e055-dec6-44ff-b7de-3c39fd5d0abf)

9) ColPali 모델이 기존 문서 검색 시스템보다 우수한 이유는 무엇인가요?

![colpai_Why is the ColPali model superior to existing document retrieval systems-kor](https://github.com/user-attachments/assets/78132e4b-c623-47c7-82ac-bcbb07a02fb6)

10) 문서 검색 시스템에서 시각적 단서의 중요성은 무엇인가요?

![colpai_What is the importance of visual cues in document retrieval systems-kor](https://github.com/user-attachments/assets/5ae3c6a4-9d71-4a91-9652-0eb273e85034)

11) ColPali 모델의 학습 데이터셋은 어떻게 구성되었나요?

![colpai_How is the training dataset for the ColPali model composed2-kor](https://github.com/user-attachments/assets/4fe1fb7a-59bd-491f-92d2-1dfd304e8f99)


### 2) Data and AI Trends Report 2024 질문/답변

아래 질문 답변에 사용한 파일은 [Data and AI Trends Report 2024](https://services.google.com/fh/files/misc/data_ai_trends_report.pdf) 입니다.

이 리포트는 44페이지로 이루어져 있고, 글, 그래프, 이미지가 함께 포함되어 있습니다.

- 파일 인덱싱 시간 : 242초
- 총 페이지 : 44 페이지
- 파일 사이즈 : 23.7 mb

![ai_trend_report_44pages](https://github.com/user-attachments/assets/e1e6b773-5189-43f3-aee2-9642eac3238e)

### 영문 질문
1) Explain Top 5 trends.
2) What is RAG, and how can it be utilized?
3) Explain why we should learn AI.

### 한글 질문
1) 우리가 AI를 배워야  하는 이유를 설명해줘.
2) AI를 사용해서 데이터 통합을 하려고 하는 기업의 비율은 얼마나 될까?
3) RAG와 같은 AI 모델을 활용한 기술을 사용하여 데이터베이스 관리에 사용하고 싶은 기업의 비율은 얼마나 될까?
4) RAG가 어떤 기술이고 어떻게 활용할 수 있어?

### 질문/답변 결과

1) Explain Top 5 trends.

![mycolpali_eng_qa_1](https://github.com/user-attachments/assets/edd694cd-dc8b-478a-a833-e6e63241c55d)

2) What is RAG, and how can it be utilized?

![mycolpali_eng_qa_2](https://github.com/user-attachments/assets/f364ee13-bee0-4c26-94fa-39ae97910f94)

3) Explain why we should learn AI.

![mycolpali_eng_qa_3](https://github.com/user-attachments/assets/80898ae2-d92f-495a-9ed4-4030b26f883a)

4) 우리가 AI를 배워야  하는 이유를 설명해줘.

![mycolpali_han_qa_1](https://github.com/user-attachments/assets/75ce1539-c9be-412e-a949-22af86db063a)

5) AI를 사용해서 데이터 통합을 하려고 하는 기업의 비율은 얼마나 될까?
6) RAG와 같은 AI 모델을 활용한 기술을 사용하여 데이터베이스 관리에 사용하고 싶은 기업의 비율은 얼마나 될까?

![mycolpali_han_qa_2](https://github.com/user-attachments/assets/106abf31-fe95-4522-99f5-3242eaf1d8ed)

7) RAG가 어떤 기술이고 어떻게 활용할 수 있어?

![mycolpali_han_qa_3](https://github.com/user-attachments/assets/9ebcdb8d-fef2-429b-950b-5cdfc8847621)

* 질문/답변 리스트

![mycolpali_list](https://github.com/user-attachments/assets/1c0f5373-3752-48d5-9f87-4e658933acba)


## 알아둘 점

- Image Size 설정에서 크기를 선택하면, ColPali가 반환하는 이미지의 크기를 설정한 기준(가로/세로 중 긴 쪽)에 맞춰 조정합니다.
- Image Size 체크박스를 선택하면, ColPali가 제공하는 이미지 크기를 변환하지 않고 그대로 사용합니다. 
- 이미지 크기가 클수록 토큰 사용량이 더 많아집니다.

## 라이센스
MIT 라이센스에 따라 배포됩니다.