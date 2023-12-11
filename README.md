Code for the paper **"Automated anonymization of radiology reports: comparison of publicly available natural language processing and large language models"** by MC Langenbach et al.

## Models

Model names correspond to the ones in the paper. Each model contains a separate folder with the code used to run it.

- [x] LLM - Llama2 Chat 13b model. We used [llama.cpp](https://github.com/ggerganov/llama.cpp) and [LangChain](https://github.com/langchain-ai/langchain).
- [ ] NLP<sub>ac</sub> - Info and code to be added post-publication.
- [ ] NLP<sub>sp</sub> - Info and code to be added post-publication.

## Usage

### LLM model

1. Set up the environment:
```bash
conda create -n llama-cpp python=3.10.12 pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
conda activate llama-cpp

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

conda install -c "nvidia/label/cuda-11.7.1" cuda-toolkit
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 VERBOSE=1 pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --verbose
pip install langchain
```

2. Inspect `LLM/anonymization_prompt.py`. Note that the one-shot example used in our prompt is censored, please provide your own example(s).

3. Download the model. We used [TheBloke/Llama-2-13B-chat-GGUF](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF) (specifically, `llama-2-13b-chat.Q5_K_M`). Feel free to use any other GGUF format model.

4. Ensure that `--column` is set to the correct column name where reports are located in your input CSV file and run:
```bash
python main.py --model <PATH_TO_DOWNLOADED_MODEL> --input <PATH_TO_INPUT_CSV> --output <PATH_TO_OUTPUT_CSV> --column <REPORT_COLUMN_NAME>
```

### NLP<sub>ac</sub> model
To be added.

### NLP<sub>sp</sub> model
To be added.

## Citation
To be added.
