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

The total file size to be downloaded exceeds 5GB. Depending on your current network speed, this may take some time.

Choose one of the two methods below to download:

1) Use the download tool from Hugging Face [vidore/colpali-v1.2](vidore/colpali-v1.2) to download.
2) Open the Jupyter notebook file download_model/download_colpali_model.ipynb and download from there.

## PyTorch Installation

To utilize the GPU, you need to install a version of [PyTorch](https://pytorch.org/) that is compatible with your operating system and the CUDA version supported by your GPU.

If the PyTorch version is not installed correctly or if you do not have a GPU, it will operate in CPU mode, which is slower.

Please refer to the Utility.get_torch_device method in the util folder for more information.

## Quick Demo
[MyColPali Demo-ENG] - In Progress

[MyColPali Demo-KOR] - In Progress


## Screenshots

* First Run

![mycolpali_first_run_2](https://github.com/user-attachments/assets/ed3a99fa-53c3-4865-8c50-ffec44ef4fe1)

* Setting
![mycolpali_first_run_1](https://github.com/user-attachments/assets/5652b8f6-6c76-4ad6-8120-3cc4089fb576)


## Question/Answer 

The document referenced in the question/answer below is the [Data and AI Trends Report 2024](https://services.google.com/fh/files/misc/data_ai_trends_report.pdf).

It took 242 seconds to index this document, which contains 44 pages filled with text, graphics, and images.

Here are the system specifications used for this test:
- CPU: Ryzen 7 7800X3D
- RAM: 64GB DDR5 Corsair 6000MT/s
- GPU: Nvidia GeForce RTX 4070 Ti Super - 16GB VRAM
- CUDA: 12.1

![ai_trend_report_44pages](https://github.com/user-attachments/assets/e1e6b773-5189-43f3-aee2-9642eac3238e)

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

* Question/Answer List

![mycolpali_list](https://github.com/user-attachments/assets/1c0f5373-3752-48d5-9f87-4e658933acba)


## License
Distributed under the MIT License.