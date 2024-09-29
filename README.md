# MyColPali
This application utilizes the ColPali vision language model and OpenAI capabilities to implement various document processing features.

### Introduction to ColPali 
- ColPali is a groundbreaking document retrieval model that utilizes Vision Language Models (VLM).
- arxiv link [ColPali: Efficient Document Retrieval with Vision Language Models](https://arxiv.org/abs/2407.01449)

### ColPali Features
- Efficient document indexing using Vision Language Models.
- Capable of handling various document types, including text, tables, and images.
- No need for processes such as OCR, Layout Parsing, Chunking, Captioning, or text embedding models.
- Relatively fast response processing compared to other RAG systems.

![colpali_archtecture](https://github.com/user-attachments/assets/d29d3c4a-959e-4c4d-ad48-01fcf253e513)

## Prerequisites
Before you begin, ensure you have met the following requirements:

1. Python:

    Make sure you have Python 3.10 or later installed. You can download it from the official Python website.

```bash
  python --version
```    

2. pip:

   Ensure you have pip installed, which is the package installer for Python.


3. Git:

   Ensure you have Git installed for version control. You can download it from the official Git website.


4. Virtual Environment:

    It is recommended to use a virtual environment to manage your project dependencies.

    You can create a virtual environment using venv:

```bash
  python -m venv venv
```    

```bash
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

5. IDE/Code Editor:

   Use an IDE or code editor of your choice. Popular options include PyCharm, VSCode, and Eclipse.


6. PlantUML: 

    PlantUML is used for generating UML diagrams. 

    Download PlantUML from the official PlantUML website or PyCharm plugin, Xcode extension.


## Quick Install

1. Clone repository

```bash
git clone https://github.com/hyun-yang/MyColPali
```

2. With pip:

```bash
pip install -r requirements.txt
```
Or virtual environment(venv), use this command

```bash
python -m pip install -r requirements.txt
```

3. Run main.py

```bash
python main.py
```

4. Configure API Key
   * Open 'Setting' menu and set API key.  


5. Re-run main.py

```bash
python main.py
```

## ColPali Model Download

Make sure to download the ColPali model prior to using the application.

The total file size to be downloaded over 5GB. Depending on your current network speed, this may take some time.

Choose one of the two methods below to download:

1) Use the download tool from Hugging Face [vidore/colpali-v1.2](https://huggingface.co/vidore/colpali-v1.2) to download.
2) Open the Jupyter notebook file **download_model/download_colpali_model.ipynb** and run it.

## PyTorch Installation

To utilize the GPU, you need to install a version of [PyTorch](https://pytorch.org/) that is compatible with your operating system and the CUDA version supported by your GPU.

If the PyTorch version is not installed correctly or if you do not have a GPU, it will operate in CPU mode, which is slower.

Please refer to the **Utility.get_torch_device** method in the util folder for more information.


## Screenshots

* First Run

![mycolpali_first_run_2](https://github.com/user-attachments/assets/ed3a99fa-53c3-4865-8c50-ffec44ef4fe1)

* Setting
![mycolpali_first_run_1](https://github.com/user-attachments/assets/5652b8f6-6c76-4ad6-8120-3cc4089fb576)

### UML Diagram

* Main Class Diagram

![MyColPali-UML-3](https://github.com/user-attachments/assets/4f14ec14-7d32-49ea-8cc1-537ac8a42d7d)

* Vision Presenter / ColPaliVLMModel Diagram

![MyColPali-UML-2](https://github.com/user-attachments/assets/ab066554-f05f-48ff-b186-8d659ade4656)


## ColPali Question/Answer Test

This is the system information used for this test.
- OS : Windows 11
- CPU : Ryzen 7 7800X3D 
- RAM : 64GB DDR5 Corsair 6000MT/s
- GPU : Nvidia GeForce RTX 4070 Ti Super - 16GB VRAM
- CUDA : 12.1

### 1) ColPali  Efficient Document Retrieval with Vision Language Models Question/Answer

The document referenced in the question/answer below is the [ColPali: Efficient Document Retrieval with Vision Language Models](https://arxiv.org/abs/2407.01449).

This document is 20 pages long and includes text, graphs, and images.

- File indexing time : 17 seconds
- Total pages : 20 pages
- File size : 8.9 mb

![colpai_pdf_time](https://github.com/user-attachments/assets/62d9f81f-2405-4f6e-9eeb-2d9c3fa448de)

### English Questions
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

*When answering the question "What evaluation metrics does the ViDoRe benchmark use?", please note that the quality of response differs when answering to using 5 images versus 10 images.*

### Korean Questions
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

### Q/A Result

1) Summarize this document.

![colpai_summarize this document](https://github.com/user-attachments/assets/d694329f-b5db-4af7-9cf5-03b93f5b3588)


2) What is the purpose of the ViDoRe benchmark?

![colpai_What is the purpose of the ViDoRe benchmark2](https://github.com/user-attachments/assets/9d6da452-014f-46a7-816b-b56768d59cab)


3) Why is the ColPali model superior to existing document retrieval systems?

![colpai_Why is the ColPali model superior to existing document retrieval systems](https://github.com/user-attachments/assets/8de82a80-0f1b-4c5d-88e3-e0eba0e88ee6)


4) What is the importance of visual cues in document retrieval systems?

![colpai_What is the importance of visual cues in document retrieval systems](https://github.com/user-attachments/assets/2fb4f352-f94e-45f9-a859-ab7eb2362832)

5) What evaluation metrics does the ViDoRe benchmark use?

- Using 5 images
![colpai_What evaluation metrics does the ViDoRe benchmark use](https://github.com/user-attachments/assets/5f16471b-f663-47ce-98e8-6af53018c291)

- Using 10 images   
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


### 2) Data and AI Trends Report 2024 Question/Answer

The document referenced in the question/answer below is the [Data and AI Trends Report 2024](https://services.google.com/fh/files/misc/data_ai_trends_report.pdf).

This report is 44 pages long and includes text, graphs, and images.

- File indexing time : 242 seconds
- Total pages : 44 pages
- File size : 23.7 mb

![ai_trend_report_44pages](https://github.com/user-attachments/assets/e1e6b773-5189-43f3-aee2-9642eac3238e)

### English Questions
1) Explain the Top 5 trends.
2) What is RAG, and how can it be utilized?
3) Explain why we should learn AI.

### Korean Questions
1) 우리가 AI를 배워야  하는 이유를 설명해줘.
2) AI를 사용해서 데이터 통합을 하려고 하는 기업의 비율은 얼마나 될까?
3) RAG와 같은 AI 모델을 활용한 기술을 사용하여 데이터베이스 관리에 사용하고 싶은 기업의 비율은 얼마나 될까?
4) RAG가 어떤 기술이고 어떻게 활용할 수 있어?


### Q/A Result

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

* Question/Answer List

![mycolpali_list](https://github.com/user-attachments/assets/1c0f5373-3752-48d5-9f87-4e658933acba)

## Important Notes

- When selecting a size in the **Image Size** settings, the app adjusts the size of the returned images from ColPali, according to the selected image size (the longer side of width/height).
- If the **Image Size** checkbox is selected, the app uses returned images from ColPali, without resizing it. 
- The larger the image size, the more tokens will be used.

## License
Distributed under the MIT License.