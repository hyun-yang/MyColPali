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

## ColPali 모델 다운로드
어플리케이션 사용하기 전에 ColPali 모델을 미리 다운로드 합니다. 

다운로드 할 전체 파일 크기가 5GB가 넘습니다. 현재 사용하고 있는 네트워크 속도에 따라 시간이 걸릴 수도 있습니다.

아래 두가지 방법 중 하나를 선택해서 다운로드 합니다.

1) 허깅 페이스 [vidore/colpali-v1.2](vidore/colpali-v1.2) 에서 다운로드 툴을 사용해서 다운로드 합니다. 
2) download_model/download_colpali_model.ipynb 주피터 노트북 파일을 열고 다운로드 합니다.

## PyTorch 설치

GPU를 활용하기 위해서는 현재 사용하는 운영체제와 GPU가 지원하는 cuda 버전과 맞는 [PyTorch](https://pytorch.org/) 버전을 설치해야 합니다.

만일, pytorch 버전이 설치가 제대로 되지 않거나, GPU가 없다면 cpu 모드로 작동합니다. 그리고 cpu 모드는 속도가 느립니다. 

util 폴더 아래에 Utility.get_torch_device 메소드를 참고하세요. 

## 데모
[MyColPali Demo-ENG] - 작업 중

[MyColPali Demo-KOR] - 작업 중


## 실행 화면

* 처음 실행

![mycolpali_first_run_2](https://github.com/user-attachments/assets/ed3a99fa-53c3-4865-8c50-ffec44ef4fe1)

* 설정
![mycolpali_first_run_1](https://github.com/user-attachments/assets/5652b8f6-6c76-4ad6-8120-3cc4089fb576)


* 질문/답변 
1) Engish Q/A - 1

![mycolpali_eng_qa_1](https://github.com/user-attachments/assets/edd694cd-dc8b-478a-a833-e6e63241c55d)

2) Engish Q/A - 2

![mycolpali_eng_qa_2](https://github.com/user-attachments/assets/f364ee13-bee0-4c26-94fa-39ae97910f94)

3) Engish Q/A - 3

![mycolpali_eng_qa_3](https://github.com/user-attachments/assets/80898ae2-d92f-495a-9ed4-4030b26f883a)

4) Korean Q/A - 1

![mycolpali_han_qa_1](https://github.com/user-attachments/assets/75ce1539-c9be-412e-a949-22af86db063a)

5) Korean Q/A - 2

![mycolpali_han_qa_2](https://github.com/user-attachments/assets/106abf31-fe95-4522-99f5-3242eaf1d8ed)

6) Korean Q/A - 3

![mycolpali_han_qa_3](https://github.com/user-attachments/assets/9ebcdb8d-fef2-429b-950b-5cdfc8847621)

* 질문/답변 리스트

![mycolpali_list](https://github.com/user-attachments/assets/1c0f5373-3752-48d5-9f87-4e658933acba)


## 라이센스
MIT 라이센스에 따라 배포됩니다.